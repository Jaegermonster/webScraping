# -*- coding: utf-8 -*-
"""
Created on Sat May 15 08:31:42 2021
2do: 
    - Make email time an option setable by user (part of UserObject). 
    - Make links a Variable in Config with all available sites! 
    - use more read_pickle function...
@author: preis
"""

import os
import pickle
from app.config import Config
  
def pickle_this(pickleFileName, buzzed_df):    
    if os.path.exists(pickleFileName):  
        print('[',pickleFileName,']', 'pickle file exists...')  
        with open(Config.PICKLE_FOLDER+pickleFileName, "rb") as f:
            old_df = pickle.load(f)  # load old user pickle
            buzzed_df = old_df.append(buzzed_df)
            buzzed_df = buzzed_df.drop_duplicates(['head1', 'head2', 'content'])
            buzzed_df.reset_index(drop=True, inplace=True)
    else:
        print('[',pickleFileName,']', 'New pickle file created...')
    with open(Config.PICKLE_FOLDER+pickleFileName, "wb") as f:  # save to pickle
        pickle.dump(buzzed_df, f, pickle.HIGHEST_PROTOCOL)
        

def scrape_the_web(user_df, i):
    from app.Scraper import Scraper
    print('----- start of user ' + user_df['name'][i] + ' -----')
    MyScrape = Scraper(user_df['name'][i], user_df['email'][i], user_df['buzzwords'][i], user_df['superbuzzwords'][i], user_df['links'][i])  # Create objects
    
    df, validity = MyScrape.scrape_site()  # scrape websites for all headlines
    
    buzzed_df, buzzedStuff = MyScrape.snoop_list(df, user_df['buzzwords'][i])  # get only buzzed headlines
    buzzedPickleName = user_df['name'][i] + '_buzzed.pkl'
    pickle_this(buzzedPickleName, buzzed_df)  # save to pickle
    
    superbuzzed_df, superbuzzedStuff = MyScrape.snoop_list(df, user_df['superbuzzwords'][i])  # get only buzzed headlines
    superbuzzedPickleName = user_df['name'][i] + '_superbuzzed.pkl'
    pickle_this(superbuzzedPickleName, superbuzzed_df)  # save to pickle
    
    time_to_email = MyScrape.time_to_email(7,27)  # When script is called at 09:03 (WindowsTaskScheduler) it will send mail... 
    # time_to_email = MyScrape.time_to_email(10,17)  # When script is called at 09:03 (WindowsTaskScheduler) it will send mail... 
    
    # send mail:
    allTimePickleName = user_df['name'][i] + '_AllTimePickle.pkl'
    if time_to_email:  # send mail when it is mailing time
        MyScrape.send_mail(MyScrape.email, buzzedPickleName, allTimePickleName)
    elif superbuzzedStuff == 1: # send mail when superbuzzed headline is found
        print('Superbuzzword happend... ')
        MyScrape.send_mail(MyScrape.email, superbuzzedPickleName, allTimePickleName, 'Breaking news...')
    print('----- end of user ' + user_df['name'][i] + ' -----\n')
    return validity


        
  
def send_an_email(content, receiver, subject):
    import smtplib
    from email.message import EmailMessage
    myMail = Config()
    from_mail = myMail.EMAIL_ADDRESS
    mail_pass = myMail.EMAIL_PASSWORD
    # to_mail = myMail.config['RECEIVER_MAIL']
    # cc_mail = myMail.MY_EMAIL_ADDRESS
    mail_server = myMail.MAIL_SERVER
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = receiver
    # msg['Cc'] = cc_mail
    msg.set_content(content)
    with smtplib.SMTP_SSL(mail_server, 465) as smtp:
        smtp.login(from_mail, mail_pass)
        smtp.send_message(msg)                


def read_user_df():  
    with open(Config.PICKLE_FOLDER+'UserPickle.pkl', "rb") as f:
        user_df = pickle.load(f)  # load old user pickle   
        return user_df
 

def check_if_pages_are_still_valid():
    import pandas as pd
    # Get all links from user_df:
    user_df = read_user_df()  # get users
    links = user_df['links']  # take all links from all users
    all_links = pd.DataFrame(columns = ['links'])  # create empty df for links
    for link in links:
        if all_links.empty:
            all_links = all_links.append({'links': link}, ignore_index=True)
        else:
            all_links['links'][0].update(link)
    link_dict = all_links.iloc[0]['links']  # make dictionary from df

    # Create test user:    
    # links={'https://www.flugrevue.de/':True,
    #     'https://www.aero.de/':True,
    #     'https://www.pressebox.de/':True,
    #     'https://www.etcusa.com/':False,
    #     'https://www.flighttraining-service.de/':False,
    #     'https://air-munich.de/':False,
    #     'http://www.fliegerverein.eu/':False,
    #     'https://www.mfa.aero/de/':False,
    #     'https://www.flugausbildung.de/':False,
    #     'https://www.eaa.aero/en/':False}
    testAffe_df  = pd.DataFrame(columns = ['name', 'email', 'links', 'buzzwords', 'superbuzzwords'])
    testAffe_df = testAffe_df.append({'name': 'TestAffe', 'email': 'whizzogalaxy@web.de', 'links': link_dict, 'buzzwords': '', 'superbuzzwords':'' }, ignore_index=True)
    # TestScrape the sites: 
    checkValidWebsites = {}
    validity = scrape_the_web(testAffe_df,0)  
    checkValidWebsites.update(validity)
    content = []
    for item in list(checkValidWebsites.items()): 
        content.append(item)
    send_an_email(str(content), 'whizzogalaxy@web.de', 'Checking scrape sites...')
    print('=> Mail sent to TestAffe...')
    return content
            