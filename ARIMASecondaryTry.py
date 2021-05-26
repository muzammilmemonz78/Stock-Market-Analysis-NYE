# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 13:16:22 2020

@author: Muzammil Memon
"""
import numpy as np 
import pandas as pd 
import math  
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from datetime import datetime, timedelta
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from Errors import Errors as e
import os.path
    
def predict_ARIMA(symbol,stocks):
    stocks.to_csv(symbol.lower() + '.csv')
    df = pd.read_csv(symbol.lower() + '.csv')
    if os.path.isfile(symbol.lower() + '.csv') == True:
        #Get number of days
        number_of_days = input("Please enter the number of days of predict: ")
        if number_of_days.isdigit() == True:
            print("Predicting the closing price of " +symbol.upper() + " for the next " +number_of_days+"days..")
            predict_start_count = len(df)
            predict_end_count = predict_start_count + int(number_of_days)
            #Find start date for predictions
            last_date = df['Date'].iloc[-1]
            last_date = datetime.strptime(last_date,"%Y-%m-%d").date()
            first_pred_date = last_date + timedelta(days=1)
            #Get date range
            date_spec = pd.date_range(first_pred_date, periods=int(number_of_days), freq='D') 
            #Plot Correlations
            plt.figure(figsize=(10,10))
            lag_plot(df['Close'], lag=5)
            plt.xticks(rotation=90)
            plt.title(symbol.upper() + "'s" + " Autocorrelation plot")
            plt.show()
            #Set parameters and train/test data
            train_data, test_data = df[0:int(len(df)*0.6)], df[int(len(df)*0.6):]
            plt.figure(figsize=(12,7))
            plt.title(symbol.upper() + "'s" + " Stock Price")
            plt.xlabel('Dates')
            plt.ylabel('Close Price USD($)')
            plt.plot(df['Close'], 'blue', label='Training Data')
            plt.plot(test_data['Close'], 'green', label='Testing Data')
            plt.xticks(rotation=90)
            plt.xticks(np.arange(0,1000, 60), df['Date'][0:1000:60])
            plt.legend()
            plt.show()
            #Run forecast
            ar_train = train_data['Close'].values
            ar_test = test_data['Close'].values
            history = [x for x in ar_train]
            predictions = list()
            for t in range(len(ar_test)):
                model = ARIMA(history, order=(5,1,0))
                model_fit = model.fit(disp=0)
                output = model_fit.forecast()
                yhat = output[0]
                predictions.append(yhat)
                obs = ar_test[t]
                history.append(obs)
            #Get predicted values to date
            predict_start_count = len(history)
            predict_end_count = predict_start_count + int(number_of_days) -1 
            pred_fut = []
            pred = model_fit.predict(start= predict_start_count,end= predict_end_count)
            
            for i in range(len(pred)-1):
                us_pred = pred[i] + history[-1]
                pred_fut.append(us_pred) 
                history.append(us_pred)
                
            #Future preds for number of days
            plt.figure(figsize=(16,9))
            plt.title(symbol.upper() + "'s" +  " Predicted Prices")
            plt.xlabel('Dates')
            plt.ylabel('Prices')
            plt.plot(date_spec.to_pydatetime(),pred_fut, 'blue', label='Predicted Price')
            newdate = date_spec.to_pydatetime()
            dfTry = []
            dfTry = pd.DataFrame(date_spec, columns=['Date'])
            dfTry.set_index('Date').index.astype('datetime64[ns]')
            dfTry['Close'] = pred_fut
            final_t1 = df.append(dfTry)
            final_t1['Date'] = pd.to_datetime(final_t1.Date).dt.strftime('%d/%m/%Y')
            # Plot train,actual and predicted
            plt.figure(figsize=(16,9))
            df_plot = pd.merge(df,final_t1,on=['Date','Open','High','Low','Close','Adj Close','Volume'],how='outer')
            plt.plot(df_plot['Close'], 'green', color='blue', label='Training Price')
            plt.plot(df_plot['Close'].tail(int(number_of_days)), 'yellow', label='Predicted Price')
            plt.plot(test_data.index, test_data['Close'], color='red', label='Actual Price')
            plt.title(symbol.upper() + "'s" + " Future Prices Prediction")
            plt.xlabel('Dates')
            plt.ylabel('Prices')
            plt.xticks(rotation=90)
            plt.xticks(np.arange(0,1000, 60), df['Date'][0:1000:60])
            plt.legend()
            plt.show()
            print("\nPlotting the graph now")
            #Compute Values    
            error = mean_squared_error(ar_test, predictions)
            RMSE = math.sqrt(error)
            print('Testing Mean Squared Error: %.3f' % error)
            print('Root Mean Squared Error: %.3f' % RMSE)
            print("\nThe graphs have been plotted.")
            print("\nThank you for using the model!")
        else:
            print("\n"+e.NUMBERS_ONLY)
    else:
        print("\n"+e.FILE_UNAVAILABLE)
    return error,RMSE