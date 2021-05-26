# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 07:46:45 2020

@author: Muzammil Memon
"""

from datetime import datetime
import unittest
from stockquotes2 import validate_period
from ticker_plot import get_ticker_data,export_data
import yfinance as yf
from Errors import Errors as e
from DescriptiveVisualizations import get_coeff_var
import pandas as pd



class DataDLTest(unittest.TestCase):
    def test_export_Data(self):
        #Check length of data for dates
        try:
            data_df = yf.download('baba', start='2020-02-01', end='2020-03-02')
            data = export_data('baba', '2020-02-01', '2020-03-02')
            self.assertEqual(len(data),len(data_df))
            
            #Data Compare for a Period
            data = export_data('amzn', '2020-01-01','2020-02-01')
            data_df = yf.download('amzn', period='1mo')
            self.assertEqual(len(data),len(data_df))
            
            #Wrong Ticker Symbol- Output - MSFTTT: No data found, symbol may be delisted
            data = export_data('msfttt', '2020-02-03', '2020-03-28')
            self.assertEqual(data.empty,True)
            
            #4. No period - Output "Not a Valid Period"
            data = export_data('amzn', '0', '0')
            self.assertEqual(data.empty,True)
        except ValueError:
            print("\n"+e.TYPE_MISMATCH)

class Test_Stock_Search(unittest.TestCase):
    def test_validate_period(self):
        #Check Date
        entered_date = validate_period("2020-01-01")
        self.assertEqual(entered_date,datetime.strptime("2020-01-01","%Y-%m-%d").date())
        #Failed Date
        entered_date = validate_period("This is a failed test")
        self.assertEqual(entered_date,"ASD")

class Test_Get_Var_CoEff(unittest.TestCase):
    def Test_validate_VarCoeff(self):
        #Incorrect stock
        df_stocks = export_data('amzn', '2020-01-01','2020-02-01')
        var_coeff = df_stocks.apply(pd.DataFrame.describe, axis=1)
        data = get_coeff_var(df_stocks,'AMZN')
        self.assertEqual(data,var_coeff['std'].mean()/var_coeff['mean'].mean())

class Test_get_Ticker_Data(unittest.TestCase):
    def Test_GetTData(self):
        #Correct Choice
        data = get_ticker_data('amzn','1y')
        self.assertEqual(data.empty,False)
        #Incorrect Choice
        data = get_ticker_data('amzn','25weekmonths')
        self.assertEqual(data.empty,True)
if __name__ == "__main__":
    unittest.main()
    
