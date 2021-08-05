'''
Credits given to Izzy Analytics for the tutorial and resources. 
https://www.youtube.com/watch?v=_AeudsbKYG8&ab_channel=IzzyAnalytics
'''
import csv
from time import sleep
from datetime import datetime
from random import random
from selenium.common import exceptions
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
import pandas as pd
import tkinter as tk
from tkinter import *
from ScraperAddition import *

def generate_filename(search_term):
    stem = path = '_'.join(search_term.split(' '))
    global filename
    filename = stem + '.csv'
    return filename

def save_data_to_csv(record, filename, new_file=False):
    header = ['description', 'price', 'rating', 'review_count']
    if new_file:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    else:
        with open(filename, 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(record)

def CreateGUI():
    global MainFrame
    MainFrame = tk.Tk()
    GetProduct = tk.Label(text='What Product Do You Want to View?')
    GetProduct.pack()
    global TextField
    TextField = tk.Entry()
    TextField.pack() 
    B = tk.Button(MainFrame, text = "OK", command = Functions)
    B.pack()
    MainFrame.mainloop()

def create_webdriver():
    driver  = webdriver.Chrome(executable_path='chromedriver.exe')
    return driver

def generate_url(search_term, page):
    base_template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')
    stem = base_template.format(search_term)
    url_template = stem + '&page={}'
    if page == 1:
        return stem
    else:
        return url_template.format(page)

def extract_card_data(card):
    description = card.find_element_by_xpath('.//h2/a').text.strip()
    try:
        price = card.find_element_by_xpath('.//span[@class="a-price-whole"]').text
    except exceptions.NoSuchElementException:
        return
    try:
        temp = card.find_element_by_xpath('.//span[contains(@aria-label, "out of")]')
        rating = temp.get_attribute('aria-label')
    except exceptions.NoSuchElementException:
        rating = ""
    try:
        temp = card.find_element_by_xpath('.//span[contains(@aria-label, "out of")]/following-sibling::span')
        review_count = temp.get_attribute('aria-label')
    except exceptions.NoSuchElementException:
        review_count = ""
    return description, price, rating, review_count

def collect_product_cards_from_page(driver):
    cards = driver.find_elements_by_xpath('//div[@data-component-type="s-search-result"]')
    return cards

def sleep_for_random_interval():
    time_in_seconds = random() * 2
    sleep(time_in_seconds)

def run(search_term):
    """Run the Amazon webscraper"""
    filename = generate_filename(search_term)
    save_data_to_csv(None, filename, new_file=True)  # initialize a new file
    driver = create_webdriver()
    num_records_scraped = 0

    for page in range(1, 3):  # max of 20 pages
        # load the next page
        search_url = generate_url(search_term, page)
        print(search_url)
        driver.get(search_url)
        print('TIMEOUT while waiting for page to load')

        # extract product data
        cards = collect_product_cards_from_page(driver)
        print("Cards:")
        print(cards)
        print("End of Cards")
        for card in cards:
            record = extract_card_data(card)
            if record:
                save_data_to_csv(record, filename)
                num_records_scraped += 1
        sleep_for_random_interval()

    # shut down and report results
    driver.quit()
    print(f"Scraped {num_records_scraped:,d} for the search term: {search_term}")

def PrintCSVFileInGUI():
    global data
    data = pd.read_csv(filename)
    pd.set_option('display.max_rows', data.shape[0]+1)
    pd.set_option('display.max_colwidth', 100)
    global FinalResult
    FinalResult = tk.Tk()
    FinalResult.geometry("1000x1000")
    text = Text(FinalResult)
    text.insert(INSERT, "Here Are Your Results: \n")
    text.insert(INSERT, data)
    text.insert(INSERT, "\n")
    text.pack(expand=True, fill=BOTH)
    CloseGUI = tk.Button(FinalResult, text = "Close This Frame", command = FinalResult.destroy)
    CloseGUI.pack()
    MainFrame.mainloop()

def Functions():
    term = TextField.get()
    run(term)
    PrintCSVFileInGUI()
    MainFrame.destroy


if __name__ == '__main__':
    CreateGUI()
    GetCSV(filename)
    GetTypeOfSort()
    PrintBestOptions()
    print("Finished")

    