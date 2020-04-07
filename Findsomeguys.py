import requests
import json
import time
import instagram_explore as ie
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as bs
#headers = {'accept': '*/*',

#           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

publication_Links = []

def find(key, dictionary): # find keys into dicts...
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

def get_Hashtag_Publication_Shortcodes(hashtag): #
    res = ie.tag(hashtag)
    return list(find('shortcode', res.data))

def create_Publication_Link_List(shortcodes):
    for i in range(len(shortcodes)):
        publication_Links.append(f'https://www.instagram.com/p/{shortcodes[i]}')

def selenium_Launch(link):
    #ua = dict(DesiredCapabilities.CHROME)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(link)
    driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a''').click()
    time.sleep(2.5)
    data_List = [driver.current_url, driver.page_source]
    #profile_Link = driver.current_url
    #page_Info = driver.page_source
    driver.close()
    return data_List

def get_Data(plinks):
    for url in plinks:
        input_List = selenium_Launch(url)
        soup = bs(input_List[1], 'lxml')
        try:
            NameDiv = soup.find(class_="nZSzR")
            try:
                NameTag = NameDiv.find('h2', attrs={'class': '_7UhW9 fKFbl yUEEX KV-D4 fDxYl'}).text
            except:
                NameTag = ""
                pass
            try:
                SubscribersDiv = soup.find("li", class_="Y8-fY").nextSibling.a.span.string
            except:
                SubscribersDiv = ""
                pass
            try:
                divDiscrp = soup.find(class_="-vDIg")
            except:
                divDiscrp = ""
                pass
            try:
                Discrp = divDiscrp.find("h1", class_="rhpdm").text
            except:
                Discrp = ""
                pass
            try:
                Discrp = f'''{Discrp}\n{divDiscrp.find("span").text}'''
            except:
                Discrp = ""
                pass
        except:
            print('\nError ??\n')
            next()
            

        #print(NameDiv)
        print(NameTag)
        print(SubscribersDiv)
        print(Discrp)
        print(input_List[0])






if __name__ == "__main__":
    print("Hashtag_Killer v.0.1 (c) Exordio\n")
    # Entering hashtag here -
    create_Publication_Link_List(get_Hashtag_Publication_Shortcodes(input('hashtag : ')))
    print(publication_Links)
    get_Data(publication_Links)

    print("\n ======= END =======")




