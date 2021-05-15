# -*- coding: utf-8 -*-
"""
Created on Sat May 15 08:40:12 2021
create_new_user: 
    - name
    - mail
    - buzzwords
    - superbuzzwords=[]
    - links={'https://www.flugrevue.de/':True,'https://www.aero.de/': True,
             'https://www.pressebox.de/':True,'https://www.etcusa.com/':False,
             'https://www.flighttraining-service.de/':False}

@author: preis
"""

from config import Config
import pickle
import os
import pandas as pd

pickleFolder = './' + Config.PICKLE_FOLDER.split('./app/')[1]
def create_new_user(name, mail, buzzwords, superbuzzwords=[], links={'https://www.flugrevue.de/':True,'https://www.aero.de/':True,'https://www.pressebox.de/':True,'https://www.etcusa.com/':False,'https://www.flighttraining-service.de/':False}):
    with open(pickleFolder+'UserPickle.pkl', "rb") as f:
        user_df = pickle.load(f)  # load old user pickle
        user_df = user_df.append({'name': name, 'email': mail, 'links': links, 'buzzwords': buzzwords, \
                            'superbuzzwords': superbuzzwords }, ignore_index=True)
        try:
            if os.path.exists(pickleFolder+'users.xlsx'): 
                with pd.ExcelWriter(pickleFolder+'users.xlsx', mode ='a') as writer:  
                    user_df.to_excel(writer, sheet_name='Users')
            else:
                with pd.ExcelWriter(pickleFolder+'users.xlsx') as writer:  
                    user_df.to_excel(writer, sheet_name='Users')
        except IOError:
            print('IOError... :( ')
    print('New user created...')
    # pickle_this('UserPickle.pkl', user_df)  # save to pickle
    with open(pickleFolder+'UserPickle.pkl', "wb") as f:  # save to pickle
        pickle.dump(user_df, f, pickle.HIGHEST_PROTOCOL)
        
# example:
# create_new_user('KikNA', 'kirsten.preis@flightteam.de', ['Training, Simulator, PPL, UL, Lehrgang, ATPL, CPL'],['Flightteam','reise'])
create_new_user('testMe', 'kirsten.preis@amst.at', ['der'],['die'])
