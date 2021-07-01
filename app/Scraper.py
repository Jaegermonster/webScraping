# -*- coding: utf-8 -*-
"""
Created on Sat May  1 19:04:15 2021
2 do:
    - check amst.at for youtube link (link not working)
@author: preis
"""

import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import os
import pickle
from app.helper_functions import send_an_email
from app.config import Config


class Scraper: 
    def __init__(self, name, email, buzzwords, superbuzzwords, websites):
        self.name = name
        self.email = email
        self.buzzwords = buzzwords
        self.superbuzzwords = superbuzzwords
        self.websites = websites

    def scrape_site(self):
        # websites.get('link')[1]
        self.validity = {}
        df  = pd.DataFrame(columns = ['head1', 'head2', 'content', 'link', 'when', 'useBuzz', 'buzzed'])
        here_and_now = Scraper.get_time_string(self)
        for i in range(0,len(self.websites)):
            URL = list(self.websites.items())[i][0]
            page = requests.get(URL)
            if 'www.aero.de' in URL: 
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml')
                valid = {URL:False}
                for a_tag in soup.find_all("a"):
                    article = a_tag.find("div", attrs={"article-content"})
                    link = a_tag.attrs['href']
                    link = 'www.aero.de/' + link
                    if a_tag.find("h5") is not None:
                        # head1 = a_tag.find("h5").get_text()
                        if a_tag.find('h3') is not None:
                            head2 = a_tag.find('h3').get_text()
                            valid = {URL:True}
                        if a_tag.find('h1') is not None:
                            head2 = a_tag.find('h1').get_text()
                            valid = {URL:True}
                        df = df.append({'head1': a_tag.find("h5").get_text(), 'head2': head2, 'content': article.get_text(), 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                    if a_tag.find("h4") is not None and article is not None:
                        valid = {URL:True}
                        df = df.append({'head1': a_tag.find("h4").get_text(), 'content': article.get_text(), 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)           
                self.validity.update(valid)
            if 'flugrevue' in URL:  # without the 4 alpha headlines 
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml')
                valid = {URL:False}
                for div_tag in soup.find_all('div'):
                    div_tag = div_tag.find("a", class_="v-A_-white__tile__container")
                    if div_tag is not None: 
                        head_beta_1 = div_tag.find('span', class_="v-A_-subline v-A_-subline--beta")   
                        head_beta_2 = div_tag.find('span', class_="v-A_-headline v-A_-headline--beta") 
                        head_gamma_1 = div_tag.find('span', class_="v-A_-subline v-A_-subline--gamma") 
                        head_gamma_2 = div_tag.find('span', class_="v-A_-headline v-A_-headline--delta")
                        if head_beta_1 is not None: 
                            head1 = head_beta_1.text
                        elif head_gamma_1 is not None: 
                            head1 = head_gamma_1.text
                        if head_beta_2 is not None: 
                            head2 = head_beta_2.text
                        elif head_gamma_2 is not None: 
                            head2 = head_gamma_2.text
                        content = div_tag.p.text
                        link = div_tag.attrs['href'] 
                        df = df.append({'head1':head1, 'head2':head2, 'content':content, 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
                # for div_tag in soup.find_all("div"):
                #     a_tag = div_tag.find('a')
                #     content = div_tag.find('p')
                #     if content is not None:
                #         content = content.text
                #         valid = {URL:True}
                #     head_alpha_1 = div_tag.find("span", attrs={"v-A_-subline v-A_-subline--alpha"}) 
                #     head_alpha_2 = div_tag.find("span", attrs={"v-A_-headline v-A_-headline--alpha"}) 
                #     head_beta_1 = div_tag.find("span", attrs={"v-A_-subline v-A_-subline--beta"}) 
                #     head_beta_2 = div_tag.find("span", attrs={"v-A_-headline v-A_-headline--beta"}) 
                #     head_gamma_1 = div_tag.find("span", attrs={"v-A_-subline v-A_-subline--gamma"}) 
                #     head_gamma_2 = div_tag.find("span", attrs={"v-A_-headline v-A_-headline--delta"}) 
                #     head_gamma = div_tag.find("a", attrs={"v-A_-white__tile__container"}) 
                #     if head_alpha_1:
                #         valid = {URL:True}
                #         df = df.append({'head1': head_alpha_1.get_text(), 'head2': head_alpha_2.get_text(), 'content': content, 'link': a_tag.attrs['href'], 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                #     if head_beta_1:
                #         valid = {URL:True}
                #         df = df.append({'head1': head_beta_1.get_text(), 'head2': head_beta_2.get_text(), 'content': content, 'link': a_tag.attrs['href'], 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                #     if head_gamma:
                #             head_gamma_1 = div_tag.find("span", attrs={"v-A_-subline v-A_-subline--gamma"}) 
                #             head_gamma_2 = div_tag.find("span", attrs={"v-A_-headline v-A_-headline--delta"}) 
                #             if head_gamma_1:
                #                 head_gamma_1 = head_gamma_1.get_text()
                #             if head_gamma_2:
                #                 head_gamma_2 = head_gamma_2.get_text()
                #             valid = {URL:True}
                #             df = df.append({'head1': head_gamma_1, 'head2': head_gamma_2, 'content': content, 'link': head_gamma.attrs['href'], 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                # self.validity.update(valid)
            if 'pressebox' in URL: 
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml')
                valid = {URL:False}
                for div_tag in soup.find_all("div", class_="col-xs-12 col-md-8"):
                    h1_tag = div_tag.find("h1")
                    content = div_tag.find("div", class_="teaser")
                    link = div_tag.find(href=True)
                    link = 'www.pressebox.de' + link.attrs['href']
                    if div_tag is not None:
                        head1 = h1_tag.get_text()
                        content = content.get_text()
                        df = df.append({'head1': head1.split('\n')[2], 'head2': '', 'content': content.split('\n')[1], 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'etcusa' in URL: 
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', id="display_news"))
                valid = {URL:False}
                for div_tag in soup.find_all('script'):
                    if div_tag is not None:
                        mySoup = div_tag.string
                all_news = mySoup.split('</b>')
                news = []
                headline = []
                link = []
                for i in range(1,len(all_news)):
                    news.append(all_news[i].split('<br />'))
                    head = str(news[i-1]).split("'<a href=\\")
                    headline.append(str(head[0]).split("\\"))
                    link_temp = str(head[1]).split("\\")[1]
                    link.append(link_temp.strip('"'))
                    df = df.append({'head1': str(headline[i-1]), 'head2': '', 'content': '', 'link': str(link[i-1]), 'when':here_and_now, 'useBuzz':False}, ignore_index=True)               
                    valid = {URL:True}
                self.validity.update(valid)
            if 'flighttraining' in URL: 
                print('Scraping... ', URL)  
                soup = BeautifulSoup(page.content, 'lxml')    
                valid = {URL:False}
                for div_tag in soup.find_all("div", class_="sppb-article-info-wrap"):
                    head = div_tag.find("a")
                    content = div_tag.find("div", class_="sppb-article-introtext")
                    link = div_tag.find(href=True)
                    link = URL + link.attrs['href']
                    valid = {URL:False}
                    if head is not None:
                        df = df.append({'head1':head.text, 'head2': '', 'content':content.get_text(), 'link': link, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        # print(df)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'air-munich' in URL:   
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', class_="col-md-4"))
                valid = {URL:False}
                for div_tag in soup.find_all("div"):
                    head = div_tag.find("h4")
                    content = div_tag.find("p")
                    if head and content is not None:
                        df = df.append({'head1':head.get_text(), 'head2': '', 'content':content.get_text(), 'link': URL, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'fliegerverein' in URL:  
                print('Scraping... ', URL)
                page = requests.get(URL + 'Ausbildung.htm')
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('table', id="AutoNumber1"))
                valid = {URL:False}
                for div_tag in soup.find_all("a"):
                    link = URL + div_tag.attrs['href']
                    if div_tag is not None:
                        df = df.append({'head1':div_tag.get_text(), 'head2': '', 'content':'', 'link': link, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'mfa.aero' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('section', class_="av_textblock_section ")) 
                valid = {URL:False}
                for i in range(2,4):
                    head = soup.find_all('div')[i].text
                    if head is not None:
                        df = df.append({'head1':head, 'head2': '', 'content':'', 'link': URL, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'flugausbildung' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml')
                valid = {URL:False}
                for div_tag in soup.find_all('div', class_="wrap mcb-wrap one valign-top clearfix"):
                    content = div_tag.find('p')
                    if content is not None: 
                        df = df.append({'head1':'', 'head2':content.get_text(), 'content':'', 'link': URL, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        # df = df.append({'head1':'', 'head2': '', 'content':content.get_text(), 'link': URL, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'eaa.aero' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', class_="elm-wrapper elm-text-wrapper")) 
                valid = {URL:False}
                for div_tag in soup.find_all("div"): 
                    if div_tag is not None: 
                        content = div_tag.get_text()
                        content = content.strip('\n')
                        df = df.append({'head1':'', 'head2':content, 'content':'', 'link': URL, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        # df = df.append({'head1':'', 'head2': '', 'content':content, 'link': URL, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'reiser' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', class_="news")) 
                valid = {URL:False}
                for div_tag in soup.find_all("article"):   
                    head1 = div_tag.a.attrs['title']
                    content = div_tag.p.get_text()
                    link = div_tag.a.attrs['href']    
                    if head1 is not None: 
                        df = df.append({'head1':head1, 'head2': content, 'content':'', 'link': link, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'amst' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', class_="news  news-overview ce-bg-2")) 
                valid = {URL:False}
                for div_tag in soup.find_all('div', class_="feature_box_text"):
                    head1 = div_tag.h3.text
                    content = div_tag.find('div', class_="feature_box_shorttext text_content")
                    link = div_tag.a 
                    if head1 is not None: 
                        if link:
                            link = 'https://www.amst.co.at' + link.attrs['href'] 
                        else:
                            link = ''
                        df = df.append({'head1':head1, 'head2': content.text, 'content':'', 'link': link, 'when':here_and_now, 'useBuzz':False}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'aerobuzz' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', class_="articles_recents")) 
                valid = {URL:False}
                for div_tag in soup.find_all('li'):
                    head1 = div_tag.h3
                    content = div_tag.p
                    link = div_tag.find_all('a')[2].attrs['href']
                    if head1 is not None and content is not None and link is not None: 
                        head1 = head1.get_text().strip('\n')
                        head1 = head1.strip(' ')
                        df = df.append({'head1':head1, 'head2': '', 'content':content.text, 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'virtualreality' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('main', id="main"))
                valid = {URL:False}
                for div_tag in soup.find_all('article'):
                    link = div_tag.h3.find('a').attrs['href']
                    head1 = div_tag.h3
                    contents = div_tag.find_all('p')
                    content1 = contents[1]
                    if len(contents) == 3:
                        content2 = contents[2].text
                    if len(contents) < 3:
                        content2 = ''
                    content = content1.text + content2
                    if head1 is not None: 
                        head1 = head1.text.strip('\n')
                        df = df.append({'head1':head1, 'head2': '', 'content':content, 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'simpleflying' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', class_="archive-main archive-grid  archive-heading-small archive-borders-disabled archive-shadow-enabled archive-scale-disabled")) 
                valid = {URL:False}
                for div_tag in soup.find_all('div', class_="post-inner"):
                    link = div_tag.a.attrs['href']
                    head1 = div_tag.h2
                    content = div_tag.find('div', class_="entry-excerpt")
                    if head1 is not None: 
                        content = content.text.strip('\n')
                        content = content.strip('\t')
                        df = df.append({'head1':head1.text, 'head2': '', 'content':content, 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'ainonline' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', class_="small-12 medium-7 large-8 columns main-content first")) 
                valid = {URL:False}
                for div_tag in soup.find_all('div'):
                    head1 = div_tag.find('div', class_="views-field views-field-title")
                    if head1 is not None: 
                        head1 = div_tag.find('span', class_="field-content title")
                        head2 = div_tag.find('div', class_="field-content teaser")
                        link = 'https://www.ainonline.com' + div_tag.a.attrs['href'] 
                        df = df.append({'head1':head1.text, 'head2':head2.text, 'content':'', 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid)
            if 'heise.de' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml')
                valid = {URL:False}
                for div_tag in soup.find_all('div', class_="a-layout__main"):
                    for div_tag in div_tag.find_all("article"):
                        valid = {URL:False}
                        if div_tag is not None: 
                            # print(head1.get_text())
                            head1 = div_tag.h1
                            head1 = head1.get_text().strip('\n')
                            link = div_tag.find('a').attrs['href']
                            if link:
                                link = 'https://www.heise.de' + link
                            df = df.append({'head1':head1, 'head2':'', 'content':content, 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                            valid = {URL:True}
                self.validity.update(valid)
            if 'artificialintelligence' in URL:  
                print('Scraping... ', URL)
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('main', id="main"))
                valid = {URL:False}
                for article_tag in soup.find_all("article"):
                    head1 = article_tag.header
                    if head1 is not None: 
                        head1 = head1.get_text().strip('\n')
                        content = article_tag.find('div', class_="cell small-12 medium-8 large-6")
                        link = article_tag.a.attrs['href']
                        df = df.append({'head1':head1, 'head2':'', 'content':content.text, 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid))
            if 'aerospacetestinginternational' in URL:  
                print('Scraping... ', URL)                
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('div', class_="row b-row listing meta-below grid-2")) 
                valid = {URL:False}
                for div_tag in soup.find_all('div', class_="column half b-col"):
                    head1 = div_tag.h2
                    if head1 is not None: 
                        head1 = head1.text
                        content = div_tag.p.text
                        link = div_tag.find('a').attrs['href']
                        df = df.append({'head1':head1, 'head2':'', 'content':content, 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid))
            if 'generalaviationnews' in URL:  
                print('Scraping... ', URL)                
                soup = BeautifulSoup(page.content, 'lxml', parse_only = SoupStrainer('main', class_="content"))
                valid = {URL:False}
                for article_tag in soup.find_all('article'):
                    head1 = article_tag.h2
                    if head1 is not None: 
                        head1 = head1.text
                        content = article_tag.div.p.text
                        link = article_tag.find('a').attrs['href']
                        df = df.append({'head1':head1, 'head2':'', 'content':content, 'link': link, 'when':here_and_now, 'useBuzz':True}, ignore_index=True)
                        valid = {URL:True}
                self.validity.update(valid))

    
        self.df = df.drop_duplicates(['head1', 'head2', 'content'])
        self.df.reset_index(drop=True, inplace=True)
        return self.df, self.validity
    
    
    def snoop_list(self, df, buzzwords):
        import copy
        self.buzzed_df  = pd.DataFrame(columns = ['head1', 'head2', 'content', 'link', 'useBuzz', 'buzzed'])
        true_df = copy.deepcopy(df[(df['useBuzz']==True)])
        false_df = copy.deepcopy(df[(df['useBuzz']==False)])
        for buzzword in buzzwords:
            true_df["buzzed"] = true_df["head1"].str.find(buzzword) + true_df["head2"].str.find(buzzword) + true_df["content"].str.find(buzzword) 
            subset = true_df[(true_df["buzzed"]>=-2) ]   # Check if buzzword is in any headline/content
            self.buzzed_df = self.buzzed_df.append(subset) 
        self.buzzed_df.drop(['buzzed'], axis='columns', inplace=True)
        self.buzzed_df = self.buzzed_df.drop_duplicates(['head1', 'head2', 'content'])
        self.buzzed_df = self.buzzed_df.append(false_df)
        self.buzzed_df.reset_index(drop=True, inplace=True)
        if len(self.buzzed_df.head1) == 0:
            self.buzzedStuff = 0
        else:
            self.buzzedStuff = 1
        return self.buzzed_df, self.buzzedStuff
 

    def send_mail(self, receiver, buzzed_pickle, allTimePickleName, subject='normal'):
        def get_news_from_buzzed(AllTimePickle, BuzzedPickle):
            if os.path.exists(AllTimePickle):
                with open(BuzzedPickle, "rb") as f:
                    buzzed_df = pickle.load(f)  # load old user pickle
                with open(AllTimePickle, "rb") as f:
                    alltime_df = pickle.load(f)  # load old user pickle
                idx = alltime_df.index  # get index
                old_max_idx = idx.max() # get max index
                
                news_df = alltime_df.append(buzzed_df)  # Merge new and old news
                news_df = news_df.drop_duplicates(['head1', 'head2', 'content'])  # Drop already known news
                news_df.reset_index(drop=True, inplace=True)  # make index nice again
                
                idx = news_df.index     # get index
                new_max_idx = idx.max() # get max index
                
                if new_max_idx-old_max_idx == 0:  # check if new news are available
                    print('--> Zzzzzz...')
                    news_df = []
                else: 
                    print('--> New stuff is going on...')
                    for i in range(0,old_max_idx+1):
                        news_df = news_df.drop(index=[i])  # delete all old news
                    # Create new AllTimePickle:
                    alltime_df = alltime_df.append(news_df)
                    alltime_df = alltime_df.drop_duplicates(['head1', 'head2', 'content'])
                    alltime_df.reset_index(drop=True, inplace=True)
                    with open(AllTimePickle, "wb") as f:  # save to pickle
                        pickle.dump(alltime_df, f, pickle.HIGHEST_PROTOCOL)  
                    # alltime_df.to_pickle(AllTimePickle)
                    print('--> [', AllTimePickle, '] extended...')
                    alltime_df.to_excel(Config.PICKLE_FOLDER+"AllTimePickle.xlsx")
                    
                return news_df  # all new news... nice!
            else:
                with open(BuzzedPickle, "rb") as f:
                    buzzed_df = pickle.load(f)  # load old user pickle
                with open(AllTimePickle, "wb") as f:  # save to pickle
                    pickle.dump(buzzed_df, f, pickle.HIGHEST_PROTOCOL)    
                print('[', AllTimePickle,'] New AllTimePickle created... ')
                buzzed_df.to_excel(Config.PICKLE_FOLDER+"AllTimePickle.xlsx")
                return buzzed_df

        try: 
            if os.path.exists(Config.PICKLE_FOLDER+buzzed_pickle):
                news_df = get_news_from_buzzed(Config.PICKLE_FOLDER+allTimePickleName, Config.PICKLE_FOLDER+buzzed_pickle)
                lines = []
                if type(news_df) != list:  # check if new news are available
                    here_and_now = Scraper.get_time_string(self)
                    for i, row in news_df.iterrows():
                        lines.append(f"{row['head1']}\n{row['head2']}\n{row['link']}\n\n")
                    send_text = ''.join(lines)  # make str from list
                    # if send_text:
                    if subject == 'normal': 
                        subject = 'News - '+ here_and_now + 'z'
                    send_an_email(send_text, receiver, subject) 
                    print('--> Mail sent...') 
                    os.remove(Config.PICKLE_FOLDER+buzzed_pickle)
                    print('[', buzzed_pickle,'] pickle file deleted... ') 
                else:
                    print('--> Nothing new...')
            else:
                print('--> No buzzed lines found...')
        except IOError:
            print('--> [', buzzed_pickle, '] not accessible... :( ')
    
            
    def time_to_email(self, mail_hour, mail_minute):
        from time import localtime, strftime, time
        now = time()
        local_tup = localtime(now)
        hour = "%H:%M"
        time_str = strftime(hour, local_tup)
        if int(time_str[0:2]) == mail_hour and int(time_str[3:5]) < mail_minute:
            self.time_to_email = 1
        else:
            self.time_to_email = 0
        return self.time_to_email

    def get_time_string(self):
        import datetime
        now = datetime.datetime.now()
        if now.minute < 10:
            minute = '0' + str(now.minute)
        else:
            minute = str(now.minute)
        self.here_and_now = "%s.%s.%s - %s:%s" % (now.year, now.month, now.day, now.hour, minute)
        return self.here_and_now
   
