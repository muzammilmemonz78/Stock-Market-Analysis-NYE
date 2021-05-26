# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 19:16:37 2020

@author: Muzammil Memon

"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from Errors import Errors as e
from Errors import Warnings as w

pd.options.mode.chained_assignment = None  # Ignore default warnings

def predict_LinReg(symbol,stocks):
    stocks.to_csv(symbol.lower() + '.csv')
    lin_regDS = pd.read_csv(symbol.lower() + '.csv') 
    indate = lin_regDS
    #User Input
    input_us = input("Please enter the number of days of predict: ")
    if input_us.isdigit() == True:
        print("Predicting the closing price of " +symbol.upper() + "for the next " +input_us +"days..")
        futureDays = int(input_us)
        print("Days trained = ",lin_regDS.shape)
        last_date = lin_regDS['Date'].iloc[-1]
        last_date = datetime.strptime(last_date,"%Y-%m-%d")
        first_pred_date = last_date + timedelta(days=1)
        #Date Range
        pred_dates = pd.DataFrame(columns=['Date'])
        for next_date in range(futureDays):
            first_pred_date = last_date + timedelta(days=1)
            pred_dates.append({'Date':next_date},ignore_index=True)
        dates = pd.date_range(first_pred_date, periods=futureDays)  
        sns.set()
        #Plot close price
        plt.figure(figsize=(10, 4))
        plt.title(symbol.upper() + "'s" + " Stock Price")
        plt.xlabel("Date")
        plt.xticks(rotation=90)
        plt.xticks(np.arange(0,len(indate), 30), indate['Date'][0:len(indate):30])
        plt.ylabel("Close Price USD ($)")
        plt.plot(lin_regDS['Close'])
        plt.show()
        #LinReg Train, test and implement
        lin_regDS = lin_regDS[['Close']]
        lin_regDS["Prediction"] = lin_regDS[['Close']].shift(-futureDays)
        x = np.array(lin_regDS.drop(["Prediction"], 1))[:-futureDays]
        y = np.array(lin_regDS["Prediction"])[:-futureDays]
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.40)
        linear = LinearRegression().fit(xtrain, ytrain)
        fut_pred = lin_regDS.drop(["Prediction"], 1)[:-futureDays]
        fut_pred = fut_pred.tail(futureDays)
        fut_pred = np.array(fut_pred)
        linearPrediction = linear.predict(fut_pred)
        # print("Please find the predicted prices below\nLinear regression prediction =",linearPrediction)
        predictions = linearPrediction
        valid = lin_regDS[x.shape[0]:]
        valid["Predictions"] = predictions
        #Plot LR predictions
        plt.figure(figsize=(10, 6)) 
        plt.title(symbol.upper() + "'s" + " Stock Price Prediction Model(Linear Regression Model)")
        plt.xlabel("Dates")
        plt.xticks(rotation=90)
        plt.ylabel("Close Price USD ($)")
        plt.plot(lin_regDS['Close'])
        plt.xticks(np.arange(0,len(indate), 30), indate['Date'][0:len(indate):30])
        plt.plot(valid[["Close", "Predictions"]])
        plt.legend(["Actual", "UserDates", "Predictions"])
        plt.show()
        #Concat date to CloseDF
        dfTry = []
        dfTry = pd.DataFrame(dates, columns=['FutDate'])
        dfTry.set_index('FutDate').index.astype('datetime64[ns]')
        size_difference = valid.index.size - dfTry.index.size
        dfTry.index = valid.index[size_difference:]
        final_plot = pd.concat([valid, dfTry], axis=1)
        del final_plot['Prediction']
        # print("Predicitions vs Days\n", final_plot)
        print("\nPlotting the graph now")
        #Plot Predicted Prices
        plt.plot(final_plot['FutDate'],final_plot['Predictions'], color='green', label='Prediction')
        plt.xlabel('Future Dates')
        plt.ylabel('Closing Price ($)')
        plt.title( symbol.upper() + "'s" + " Future Predicted Closing Prices") #symbol.upper()
        plt.legend()
        plt.xticks(rotation=90)
        plt.show()
        print("\nThe graphs have been plotted.")
        print("\nThank you for using the model!")
    else:
        print("\n"+e.NUMBERS_ONLY)
    return lin_regDS
