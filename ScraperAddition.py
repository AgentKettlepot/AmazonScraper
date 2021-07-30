'''
Credits given to Izzy Analytics for the tutorial and resources. 
https://www.youtube.com/watch?v=_AeudsbKYG8&ab_channel=IzzyAnalytics
'''
import csv
import pandas as pd
import tkinter as tk
from tkinter import *

def GetCSV(File_Path):
    global data
    data = pd.read_csv(File_Path)
    pd.set_option('display.max_rows', data.shape[0]+1)
    pd.set_option('display.max_colwidth', 100)

def Retrieve(Field):
    global UserSortChoice
    UserSortChoice = Field.get()
    if UserSortChoice=='PRICE':
        print(SortByPrice(data))
    if UserSortChoice=='REVIEW':
        print(SortByReview(data))

def GetTypeOfSort():
    global GetSort
    GetSort = tk.Tk()
    GetType = tk.Label(text="How Would You Like To Sort the List? (price or review)")
    GetType.pack()
    global TextField
    TextField = tk.Entry()
    TextField.pack() 
    B = tk.Button(GetSort, text = "OK", command = Retrieve(TextField))
    B.pack()
    GetSort.mainloop()


def SortByPrice(frame):
    frame['price']=frame['price'].astype(str).str.replace(',','')
    frame.price = frame.price.astype(float)
    global SortByPrices
    SortByPrices = frame.sort_values('price') 
    return SortByPrices

def SortByReview(frame):
    frame["review_count"]=frame["review_count"].astype(str).str.replace(',','.')
    frame.review_count = frame.review_count.astype(float)
    frame['rating'] = frame['rating'].str.slice(0, 4)
    frame.rating = frame.rating.astype(float)
    global SortByReview
    SortByReview = frame.sort_values(['review_count'], ascending=False) 
    SortByReview = frame.sort_values([ 'rating'], ascending = False)
    return SortByReview

def FindBestOptions(frame):
    frame['price']=frame['price'].astype(str).str.replace(',','')
    frame.price = frame.price.astype(float)
    frame["review_count"]=frame["review_count"].astype(str).str.replace(',','.')
    frame.review_count = frame.review_count.astype(float)
    frame['rating'] = frame['rating'].astype(str).str.slice(0, 4)
    frame.rating = frame.rating.astype(float)
    frame['total'] =(frame['rating'] + frame['review_count'] - frame['price']) 
    pd.options.display.max_colwidth = 200
    global BestFrame
    BestFrame = frame.sort_values('total', ascending=False) 


    return BestFrame[['description', 'price']].head().to_string(index=False, header=False)

def PrintBestOptions():
    global BestOptions
    BestOptions = tk.Tk()
    Label = tk.Label(text="Best Options")
    Label.pack()
    Objects = tk.Label(text=FindBestOptions(data))
    Objects.pack()
    pd.options.display.max_colwidth = 200
    Text = tk.Label(text="\nYour Best Option Is: \n")
    Text.pack()
    FinalBestOption = tk.Label(text=BestFrame['description'].head(1).to_string(index=False, header=False) + "\nPrices: " + BestFrame['price'].head(1).to_string(index=False))
    FinalBestOption.pack()
    GetSort.mainloop()