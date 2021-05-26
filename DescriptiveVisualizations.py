# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:02:27 2020

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
from Errors import Errors as e

def get_descriptive_choice(symbol,stocks):
    specified_stock_data = (stocks.apply(pd.DataFrame.describe, axis=1))
    print("\nYou've chosen Descriptive Statistics\n")
    print("For "+symbol+",What do you want to drill down into today?")
    print("\n1. Quartiles.\n2. Range.\n3. CoEfficient of variation.\n4. Standard Deviation.\n5. Stock Prices\n6. Moving Averages Convergence Divergence.\n7. Moving Averages.\n8. Weighted Moving Averages.\n9. Linear Trend Line.\n10. Quit")
    choice_query = input("Please enter your choice: ")
    print("\n You chose: " +choice_query)    
    has_Printed = False
    if choice_query in ("1,2,3,4,5,6,7,8,9,10"):
        
        while (choice_query != "10" and stocks.empty == False and has_Printed == False):
            try:
                
                if stocks.empty == False and choice_query == "1" and has_Printed == False:
                    quartile_Details = get_quartiles(stocks,symbol)
                    print(quartile_Details)
                    print("\nThe quartile graph has been plotted for your reference.")
                    get_descriptive_choice(symbol,stocks)
                    break
                elif stocks.empty == False and choice_query == "2" and has_Printed == False:
                    range_Details = get_stock_range(stocks,symbol)
                    print(range_Details)
                    print("\nThe range graph has been plotted for your reference.")
                    get_descriptive_choice(symbol,stocks)
                    break
                elif stocks.empty == False and choice_query == "3" and has_Printed == False:
                    get_coeff_var(stocks,symbol)
                    get_descriptive_choice(symbol,stocks)
                    break
                elif stocks.empty == False and choice_query == "4" and has_Printed == False:
                    std_Dev = get_standard_deviation(stocks,symbol)
                    print(std_Dev)
                    print("\nThe Standard Deviation graph has been plotted for your reference.")
                    get_descriptive_choice(symbol,stocks)
                    break
                elif stocks.empty == False and choice_query == "5" and has_Printed == False:
                    stock_Det = get_stock_details(stocks,symbol)
                    print(stock_Det)
                    print("\nThe detailed stock graph has been plotted for your reference.")
                    get_descriptive_choice(symbol,stocks)
                 
                    break
                elif stocks.empty == False and choice_query == "6" and has_Printed == False:
                    mcD_data=gD_MACD(stocks)
                    print (mcD_data)
                    print("\nThe MACD graph has been plotted for your reference.")
                    get_descriptive_choice(symbol,stocks)
                    break
                elif stocks.empty == False and choice_query == "7" and has_Printed == False:
                    mA_data=gD_MA(stocks)
                    print (mA_data)
                    print("\nThe Moving Average graph has been plotted for your reference.")
                    get_descriptive_choice(symbol,stocks)
                    break
                elif stocks.empty == False and choice_query == "8" and has_Printed == False:
                    wmA_data=gD_WMA(stocks)
                    print("\nThe Weighted Moving Average graph has been plotted for your reference.")
                    get_descriptive_choice(symbol,stocks)
                    print (wmA_data)
                    break
                elif stocks.empty == False and choice_query == "9" and has_Printed == False:
                    linear_tl = get_linearTrendLine(stocks)
                    print (linear_tl)
                    print("\nLinear Trend Line has been plotted for your reference.")
                    get_descriptive_choice(symbol,stocks)
                    break
                else:
                    print("Wrong choice, please try again.")
                    print ("Graph for opening and closing prices plotted.")
                    stocks['Open'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price"),plt.title("Opening and Closing Prices for "+symbol)
                    stocks['Close'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price"),plt.title("Opening and Closing Prices for "+symbol)
                    plt.legend()
                    plt.show()
                    break
            except KeyError as e1:
                print("Invalid ticker - Please try again",e1)
                break
            except ValueError as e2:
                print("Invalid Values - Please try again",e2)
    else:
        print("\n"+e.INVALID_CHOICE)
        get_descriptive_choice(symbol,stocks)

def get_quartiles(stocks,symbol):
        described_quart = (stocks.apply(pd.DataFrame.describe, axis=1))
        print("The quartiles are: 25% Quartile\n:",described_quart['25%'].reset_index(),"50% Quartile\n:",described_quart['50%'].reset_index(),"75% Quartile\n: ",described_quart['75%'].reset_index())
        described_quart.to_csv( symbol.upper() + 'quartiles.csv', encoding='utf-8')
        # (symbol.upper() + " Quartiles", sep='\t', encoding='utf-8', index= False, header = True)
        described_quart['25%'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price"),plt.title("Quartile graph")
        described_quart['50%'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price"),plt.title("Quartile graph")
        described_quart['75%'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price"),plt.title("Quartile graph")
        plt.legend()
        plt.show()
        return 

def get_stock_range(stocks,symbol):
    described_range =  (stocks.apply(pd.DataFrame.describe, axis=1))
    print("The range for the Company Price is:\n:", described_range['max'].reset_index(),"\nMinimum\n",described_range['min'].reset_index())
    described_range['min'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price"),plt.title("Range Difference")
    described_range['max'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price"),plt.title("Range Difference")
    plt.legend()
    plt.show()


def get_coeff_var(stocks,symbol):
    var_coeff =  (stocks.apply(pd.DataFrame.describe, axis=1))
    print("The CoEfficient of Variation is: ",var_coeff['std'].mean()/var_coeff['mean'].mean())


def get_standard_deviation(stocks,symbol):
    std_dev =  (stocks.apply(pd.DataFrame.describe, axis=1))
    print("The Standard Deviation in the Company Price is: \n",std_dev['std'].reset_index())
    std_dev['std'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Standard Deviation in Closing Price"),plt.title("Standard Deviation")
    plt.legend()
    plt.show()


def get_stock_details(stocks,symbol):
    print("Stock details\n",stocks['Open'],stocks['High'],stocks['Low'],stocks['Close'])
    stocks['Open'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price($)"),plt.title("Stock Details")
    stocks['High'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price($)"),plt.title("Stock Details")
    stocks['Low'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price($)"),plt.title("Stock Details")
    stocks['Close'].plot(figsize=(16, 9)),plt.xlabel("Date"),plt.ylabel("Price($)"),plt.title("Stock Details")
    plt.legend()
    plt.show()

def gD_MACD(stocks):
    df_MACD = stocks[['Close']]
    df_MACD.reset_index(level=0, inplace=True)
    df_MACD.columns=['MACDDate','MACDCP']
    plt.plot(df_MACD.MACDDate, df_MACD.MACDCP, label='MACD')
    plt.show()
    p1 = df_MACD.MACDCP.ewm(span=12, adjust=False).mean()
    p2 = df_MACD.MACDCP.ewm(span=26, adjust=False).mean()
    macd = p1-p2
    p3 = macd.ewm(span=9, adjust=False).mean()
    plt.plot(df_MACD.MACDDate, macd, label='Stock MACD', color = '#EBD2BE')
    plt.plot(df_MACD.MACDDate, p3, label='Signal Line', color='#E5A4CB')
    plt.legend(loc='upper left')
    plt.show()
 
    
def gD_MA(stocks):
    df_MA = stocks[['Close']]
    df_MA.reset_index(level=0, inplace=True)
    df_MA.columns=['DateMA','MoveAvePrice']
    rolling_mean = df_MA.MoveAvePrice.rolling(window=20).mean()
    rolling_mean2 = df_MA.MoveAvePrice.rolling(window=50).mean()
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.xticks(rotation=90)
    plt.plot(df_MA.DateMA, df_MA.MoveAvePrice, label='Moving Averages')
    plt.plot(df_MA.DateMA, rolling_mean, label='20 Day SMA', color='orange')
    plt.plot(df_MA.DateMA, rolling_mean2, label='50 Day SMA', color='magenta')
    plt.legend()
    plt.show()
    return df_MA
    
def gD_WMA(stocks):
    weights = np.arange(1,11) #this creates an array with integers 1 to 10 included
    df_WMA = stocks[['Close']]
    df_WMA.reset_index(level=0, inplace=True)
    wma10 = df_WMA['Close'].rolling(10).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
    plt.figure(figsize = (12,6))
    plt.plot(df_WMA['Close'], label="Closing Price")
    plt.plot(wma10, label="10-Day WMA")
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.ylabel("Closing Price")
    plt.legend()
    plt.show()
    return df_WMA

def get_linearTrendLine(stocks): #https://stackoverflow.com/questions/29960917/timeseries-fitted-values-from-trend-python
    df=stocks
    dayZero = df.index[0]
    df['Day'] = (df.index - dayZero).days
    fit = sm.ols(formula="Close ~ Day", data=df).fit()
    print(fit.summary())
    predict = fit.predict(df)
    df['Fitted'] = predict
    #Plot the graph
    fig, ax = plt.subplots(figsize=(16,9))
    ax.scatter(df.index, df.Close)
    ax.plot(df.index, df.Fitted, 'r')
    ax.set_ylabel("Closing price in USD($)")
    fig.suptitle("Linear Trend Line")
    plt.show()
        