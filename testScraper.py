# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 07:37:47 2021

@author: preis
"""
from app.helper_functions import check_if_pages_are_still_valid
# import pickle
# import threading
# import pandas as pd
# import time
# import schedule
from app.config import Config

# links={'https://www.flugrevue.de/':True,
#        'https://www.aero.de/':True,
#        'https://www.pressebox.de/':True,
#        'https://www.etcusa.com/':False,
#        'https://www.flighttraining-service.de/':False,
#        'https://air-munich.de/':False,
#        'http://www.fliegerverein.eu/':False,
#        'https://www.mfa.aero/de/':False,
#        'https://www.flugausbildung.de/':False,
#        'https://www.eaa.aero/en/':False}
 
# user_df = pd.DataFrame(columns = ['name', 'email', 'links', 'buzzwords', 'superbuzzwords'])
# user_df = user_df.append({'name': 'TestAffe', 'email': Config.MY_EMAIL_ADDRESS, 'links': links, 'buzzwords': '', 'superbuzzwords':'' }, ignore_index=True)


# def job():
#     for i in range(0,user_df.shape[0]): 
#         scrape_the_web(user_df, i)  # w/o multithreading
#         # threading.Thread(target = scrape_the_web, args=(user_df,i)).start()  # w/ multithreading

# job()

# # schedule.every(12).minutes.do(job)
# schedule.every(30).seconds.do(job)
# schedule.every().day.at("11:11").do(check_if_pages_are_still_valid)
# # schedule.every().wednesday.at("13:15").do(check_if_pages_are_still_valid)
# # schedule.every().sunday.at("20:17").do(check_if_still_alive)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

content, testAffe_df = check_if_pages_are_still_valid()
print(content)
