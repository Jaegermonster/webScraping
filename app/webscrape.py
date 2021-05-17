# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 07:37:47 2021
2do: 
    - Make extra user file (in config?). 
    - Add Date and Time to BreakingNews... 
    - Add Multithreading with validityReturn
    - Set link:True if user wants this link to scrape
@author: preis
"""
from app.helper_functions import scrape_the_web, check_if_pages_are_still_valid
import pickle
import threading
import time
import schedule
from app.config import Config


with open(Config.PICKLE_FOLDER+'UserPickle.pkl', "rb") as f:
    user_df = pickle.load(f)  # load user pickle

def job():
    for i in range(0,user_df.shape[0]): 
        # scrape_the_web(user_df, i)  # w/o multithreding
        threading.Thread(target = scrape_the_web, args=(user_df,i)).start()  # w/ multithreding



schedule.every(12).minutes.do(job)
# schedule.every(30).seconds.do(job)
schedule.every().day.at("09:11").do(check_if_pages_are_still_valid)
# schedule.every().wednesday.at("13:15").do(check_if_pages_are_still_valid)
# schedule.every().sunday.at("20:17").do(check_if_still_alive)

while True:
    schedule.run_pending()
    time.sleep(1)