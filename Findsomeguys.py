import requests
import json
import time
import instagram_explore as ie
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as bs



headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

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
    #options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    #options.add_argument('window-size=1920x935')chrome_options=options
    driver = webdriver.Chrome()
    driver.get(link)
    driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a''').click()
    page_Info = driver.page_source
    time.sleep(3)
    #driver.close()
    return page_Info

def get_Profile_Links(plinks, headers):
    for url in plinks:
        soup = bs(selenium_Launch(url), 'lxml')

        NameDiv = soup.find(class_="nZSzR")
        NameTag = NameDiv.find('h2', attrs={'class': '_7UhW9 fKFbl yUEEX KV-D4 fDxYl'}).text
        SubscribersDiv = soup.find("li", class_="Y8-fY").nextSibling.a.span.string
        divDiscrp = soup.find(class_="-vDIg")
        try:
            Discrp = divDiscrp.find("h1", class_="rhpdm").text
            Discrp = f'''{Discrp}\n{divDiscrp.find("span").text}'''
        except:
            pass

        print(NameDiv)
        print(NameTag)
        print(SubscribersDiv)
        print(Discrp)



        #session = requests.Session()
        #request = session.get(url, headers = headers)
        #if request.status_code == 200:


            #print(f'\n | {url} - status 200 OK |')
            #soup = bs(request.content, 'lxml')
            #div_Profile_Link = soup.find(class_ = "e1e1d")
            #profile_Link = soup.find('a', attrs = {'class' : "sqdOP yWX7d     _8A5w5   ZIAjV "})
            #print(soup)
            #profile_Link = soup.find('div', {'class': 'e1e1d'}).find('a').get('href')
            #print(profile_Link)
        #else:
        #    print('error')





if __name__ == "__main__":
    print("Hashtag_Killer v.0.1 (c) Exordio\n")
    # Entering hashtag here -
    create_Publication_Link_List(get_Hashtag_Publication_Shortcodes(input('hashtag : ')))
    print(publication_Links)
    get_Profile_Links(publication_Links, headers)




