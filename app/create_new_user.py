# -*- coding: utf-8 -*-
"""
Created on Sat May 15 08:40:12 2021
2do: 
    - improve to excel file! Needs to update when user is updated. 
    - Remove dublicate sheets from excel when creating new user. 
create_new_user: 
    - name
    - mail
    - buzzwords
    - superbuzzwords=[]
    - links={'https://www.flugrevue.de/':True,'https://www.aero.de/': True,
             'https://www.pressebox.de/':True,'https://www.etcusa.com/':False,
             'https://www.flighttraining-service.de/':False,
             'https://air-munich.de/':False,
             'http://www.fliegerverein.eu/':False,
             'https://www.mfa.aero/de/':False,
             'https://www.flugausbildung.de/':False,
             'https://www.eaa.aero/en/':False}

@author: preis
"""

from config import Config
import pickle
import os
import pandas as pd

pickleFolder = './' + Config.PICKLE_FOLDER.split('./app/')[1]

def write_new_userDf(user_df):
    with open(pickleFolder+'UserPickle.pkl', "wb") as f:  # save to pickle
        pickle.dump(user_df, f, pickle.HIGHEST_PROTOCOL)
    print('user_df pickled...')    
        
def write_to_excel(user_df):
    try:
        if os.path.exists(pickleFolder+'users.xlsx'): 
            with pd.ExcelWriter(pickleFolder+'users.xlsx', mode ='a') as writer:  
                user_df.to_excel(writer, sheet_name='Users')
        else:
            with pd.ExcelWriter(pickleFolder+'users.xlsx') as writer:  
                user_df.to_excel(writer, sheet_name='Users')
    except IOError:
        print('IOError... :( ')


def create_new_user(name, mail, buzzwords, superbuzzwords=[], links={'https://www.flugrevue.de/':True,'https://www.aero.de/':True,
             'https://www.pressebox.de/':True,'https://www.etcusa.com/':False,
             'https://www.flighttraining-service.de/':False,
             'https://air-munich.de/':False,
             'http://www.fliegerverein.eu/':False,
             'https://www.mfa.aero/de/':False,
             'https://www.flugausbildung.de/':False,
             'https://www.eaa.aero/en/':False}):
    with open(pickleFolder+'UserPickle.pkl', "rb") as f:
        user_df = pickle.load(f)  # load old user pickle
        user_df = user_df.append({'name': name, 'email': mail, 'links': links, 'buzzwords': buzzwords, \
                            'superbuzzwords': superbuzzwords }, ignore_index=True)
        write_to_excel(user_df)
    print('New user created...')
    # pickle_this('UserPickle.pkl', user_df)  # save to pickle
    write_new_userDf(user_df)
    

def append_to_user(indexValue, buzzwords, superbuzzwords, links):  # Update user
    with open(pickleFolder+'UserPickle.pkl', "rb") as f:
        user_df = pickle.load(f)  # load old user pickle   
    if buzzwords: 
        user_df['buzzwords'][indexValue].update(buzzwords)    
        print('Append buzzwords')
    if superbuzzwords: 
        user_df['superbuzzwords'][indexValue].update(superbuzzwords)  
        print('Append superbuzzwords')  
    if links: 
        user_df['links'][indexValue].update(links)    
        print('Append links')
    write_new_userDf(user_df)
    return user_df
        
# # example:
# # create_new_user('KikNA', 'kirsten.preis@flightteam.de', ['Training, Simulator, PPL, UL, Lehrgang, ATPL, CPL'],['Flightteam','reise'])
# create_new_user('testMe', 'whizzogalaxy@web.de', [],[])

# user_df['links'][2].update({'links':"1000"})    
newLinks = {'https://air-munich.de/':False,
             'http://www.fliegerverein.eu/':False,
             'https://www.mfa.aero/de/':False,
             'https://www.flugausbildung.de/':False,
             'https://www.eaa.aero/en/':False}
# user_df = append_to_user(2,[],[],{'links':"1001"})
user_df = append_to_user(2,[],[],newLinks)