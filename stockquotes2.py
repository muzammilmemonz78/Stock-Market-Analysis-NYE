# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 16:02:27 2020

@author: Muzammil Memon
"""


###Do your thing!###
import pandas as pd
from ticker_plot import export_data,get_ticker_data,process_search_choice
from DescriptiveVisualizations import get_descriptive_choice,gD_MACD,gD_MA,gD_WMA,get_quartiles,get_stock_range,get_coeff_var,get_standard_deviation,get_stock_details,get_linearTrendLine
from ARIMASecondaryTry import predict_ARIMA
from LinReg import predict_LinReg
import yfinance as yf
from datetime import datetime
from Errors import Errors as e
from Errors import Warnings as w

#Setting DF max display
pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)


def get_company_list():
    return pd.read_csv('companylist.csv')

def t_and_c():
    """Display terms and conditions from 'terms.txt'"""
    for line in open("terms.txt"):
        print(line, end="\n")

def display_welcome():
    print('\nWelcome to the Muzammil\'s'' StockPredictor Application')

def display_menu():
    print('\n''+' + '*' * 49 + '+')
    print("|1. Search Local Stocks"+' '*27+"|\n|2. Analytics on YFinance Stocks"+' '*18+"|\n|3. Quick Flash Online Stocks"+' '*21+"|\n|4. Export Data"+' '*35+"|\n|5. Read T&C"+' '*38+"|\n|6. Unit Testing"+' '*34+"|\n|10. Quit"+' '*41+"|")
    print('+' + '*' * 49 + '+')
    
def get_choice():
    return input("\nPlease enter your choice: ")


def search_stocks(company_list):
    print('Search Stocks')
    search_choice = ''
    process_search_choice(company_list)
    
def search_display_yFinance_stocks():
    stocks = None
    while stocks is None:
        try:
            print("\nYou chose to search yFinance stocks.\n")
            symbol = input("Please choose ticker symbol: ")
            if len(symbol) <= 1 or symbol.isdigit() == True:
                print("\n"+e.TYPE_MISMATCH)
                break
            print('\nSearching yFinance stocks for: ' +symbol)
            start = input("Please choose start period(YYYY-MM-DD): ")
            validate_period(start)
            end = input("Please choose end period(YYYY-MM-DD): ")
            validate_period(end)
            print('\nSearching yFinance stocks for: ' +symbol+" from "+start+" to "+end)
            stocks = yf.download(symbol, start, end)
            specified_stock_data = (stocks.apply(pd.DataFrame.describe, axis=1))
            print("\nStock Data for the first 10 days:\n")
            print(stocks.head())
            print("\nStock Data for the last 10 days:\n")
            print(stocks.tail())
            if(stocks.empty):
                print("\n"+w.DATA_NOT_FOUND)
            else:
                print("\nStock details found, what do you want to do?\n")
                process_online_choice(stocks,symbol,start,end)
                break
        except KeyError as e3:
            print("Invalid ticker - Please try again",e3)
        except ValueError as e4:
            print("Invalid Values - Please try again",e4)
            
def validate_period(date_input):
    try:
        #Convert date string to datetime
        date_input = datetime.strptime(date_input,"%Y-%m-%d").date()
    except ValueError as date_value:
        print("\n"+e.TYPE_MISMATCH)
    finally:
        return date_input
    
def get_stock_history():
    print('Query Time Range For Stock Details.')
    data = None
    while data is None:
        try:
            symbol = input("Please choose ticker symbol: ")
            if len(symbol) <= 1 or symbol.isdigit() == True:
                print("\n"+e.TYPE_MISMATCH)
                break
            else:
                period = input("Please choose period: (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")
                if(period  in ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')):
                    data = get_ticker_data(symbol, period)
                    print("\n Data has also been exported, predictions can use this dataset.")
                    break
                else:
                    print("\n"+e.INVALID_CHOICE)
                    break
                    get_stock_history()
        except KeyError as e2:
                print('\nInvalid Symbol - Please try again.',e2)


            
def process_online_choice(stocks,symbol,start,end):
    print("\n1. Download data for offline use.\n2. Descriptive Statistics.\n3. Predictive Analytics using ARIMA\n4. Predictive Analytics using Linear Regression.\n10. Quit")    
    online_choice = input("Please enter your choice: ")
    while(online_choice != "10"):
        if online_choice in ('1,2,3,4'):
            try:
                if(online_choice == '1'):
                    print("\n Downloading data for offline use in this directory.")
                    export_data(symbol,start,end)
                    print("\n Data has been exported, please find the CSV in this directory")
                    process_online_choice(stocks,symbol,start,end)
                    break
                elif(online_choice == '2'):
                    get_descriptive_choice(symbol, stocks)
                    process_online_choice(stocks,symbol,start,end)
                    break
                elif(online_choice == '3'):
                    predict_ARIMA(symbol,stocks)
                    process_online_choice(stocks,symbol,start,end)
                    break
                elif(online_choice == '4'):
                    predict_LinReg(symbol,stocks)
                    process_online_choice(stocks,symbol,start,end)
                    break
                else:
                    print("\n"+e.INVALID_CHOICE)
                    process_online_choice(stocks,symbol,start,end)
            except KeyError as e1:
                print("KeyError found",e1)
            except ValueError as e2:
                print("ValueError found",e2)
        else:
            print("\n"+e.INVALID_CHOICE)
            break

def download_data():
    print('Export Data')
    data = None
    while data is None:
        try:
            symbol = input("Please choose ticker symbol: ")
            if len(symbol) <= 1:
                print("\n"+e.TYPE_MISMATCH)
                break
            start = input("Please choose start period: (YYYY-MM-DD)")
            validate_period(start)
            end = input("Please choose end period: (YYYY-MM-DD)")
            validate_period(start)
            data = export_data(symbol, start, end)
        except KeyError:
            print('Invalid Symbol - Please try again.')


    
def process_choice(choice, company_list):
    while choice != "10":
        if choice == "1":
            search_stocks(company_list)
        elif choice == "2":
            search_display_yFinance_stocks()
        elif choice == "3":
            get_stock_history()
        elif choice == "4":
            download_data()
        elif choice == "5":
            t_and_c()
        elif choice == "6":
            print("\nUnit testing has been developed for a tester, please run the file independently. Please read the user guide for more information.")
        else:
            print("\n"+e.INVALID_CHOICE)
        display_menu()
        choice = get_choice()

def main():
    company_list = get_company_list()
    # Create a menu for the stock quotes app
    display_welcome()
    display_menu()
    # ask the user for their choice
    choice = get_choice()
    # process the choice
    process_choice(choice, company_list)
    
if __name__ == '__main__':
    main()

    