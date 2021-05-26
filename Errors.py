# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 07:44:43 2020

@author: hp
"""

from colorama import Style,Fore
class Errors:
    
    # Only numbers accepted
    NUMBERS_ONLY = Fore.RED+"No alphabets or alphanumeric characters allowed. Please Try Again!"+Style.RESET_ALL
    #Error - When choice selected is out of domain
    INVALID_CHOICE = Fore.RED+"Incorrect choice, please select a value from the list."+Style.RESET_ALL
    #No File Found
    FILE_UNAVAILABLE = Fore.RED+"Unable to Locate &1. Kindly Check Configuration"+Style.RESET_ALL
    #Type Error
    TYPE_MISMATCH = Fore.RED+"Unable to carry on, please check input errors"+Style.RESET_ALL
    #Invalid Dates 
    INVALID_PERIOD = Fore.RED+"Invalid Period Entered"+Style.RESET_ALL
    

class Warnings:
        #Warning
    EXCEPT = Fore.YELLOW+"&0"+Style.RESET_ALL

    #Warning yFinance No Data 
    DATA_NOT_FOUND = Fore.YELLOW+"No Information Found"+Style.RESET_ALL
