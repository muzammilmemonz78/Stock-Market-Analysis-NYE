#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 11:06:43 2020

@author: Muzammil Memon
"""

import yfinance as yf
import sys
import matplotlib.style
import matplotlib as mpl
import matplotlib.pyplot as plt
from Errors import Errors as e
from Errors import Warnings as w
import pandas as pd
import pprint
mpl.style.use('ggplot')

    
def export_data(symbol, start, end):
    # Download stock data then export as CSV
    data_df = yf.download(symbol, start=start, end=end)
    data_df.to_csv(symbol.lower() + '.csv')
    yf.prepost = True
    yf.threads = True
    yf.proxy = None
    return data_df
    
def get_ticker_data(symbol, period):
    if(period in ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')):
        ticker_info = yf.Ticker(symbol)
        company_name = ticker_info.info['longName']
        print(company_name)
        #Cleanly print the Stock Details
        pprint.pprint(ticker_info.info)
        
        hist = ticker_info.history(period=period)
        hist['Close'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Closing Price"),plt.title("Closing price for: "+company_name) 
        plt.legend()
        plt.show()
        hist.to_csv=(symbol.lower() + '.csv')
        print("\nA graph for "+company_name+"'s closing price has been plotted for your reference.")
        return hist
    else:
        print("Please enter a valid time period from the list.")
        get_ticker_data(symbol, period)
        sys.exit(0)
        
    
def process_search_choice(company_list):
    search_choice = ''
    while search_choice != 3:
        search_choice = input("\nKindly select an option:\n1. Search by Ticker Symbol \n2. Search by Name \n3. Exit\nSelect: ")
        if search_choice in ('1,2,3'):
            if search_choice == "1": 
                symbol = input("Please enter company ticker symbol: (3 to exit) ")
                filtered_companies = company_list[(company_list.Symbol.str.lower().str.contains(symbol.lower()))]
                # filtered_info=filtered_companies['Symbol','Name','MarketCap','IPOyear']
                if(filtered_companies.empty) or None:
                    print("\nCompany ticker not found in the NASDAQ extract, please fetch yFinance details\n")
                    break
                    process_search_choice()            
                else:
                    print("\n")
                    print(filtered_companies)
            elif search_choice == "2":
                comp_name = input("Please enter company name: (3 to exit) ")
                filtered_companies = company_list[(company_list.Name.str.lower().str.contains(comp_name.lower()))]
                if(filtered_companies.empty):
                    print("\nCompany name not found in the NASDAQ extract, please fetch yFinance details\n")
                    break
                    process_search_choice()
                else:
                        print("\n",filtered_companies)
            elif search_choice == "3":
                    break
            else:
                print("\n"+e.INVALID_CHOICE)
                break
        else:
            print("\n"+e.NUMBERS_ONLY)
            break