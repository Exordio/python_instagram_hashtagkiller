# -*- coding: utf-8 -*-

import time
import instagram_explore as ie
import pandas as pd
import config
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as bs

publication_Links = []
column_Names = ['Nametag', 'Subscribers', 'Discrption', 'Profile_link']
parsed_Data_Df = pd.DataFrame(columns = column_Names)

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
    firstPage = list(find('shortcode', res.data))
    data, cursor = ie.tag(hashtag, res.cursor)
    concat_Search_Pages = firstPage + list(find('shortcode', data))
    return concat_Search_Pages

def create_Publication_Link_List(shortcodes):
    for i in range(len(shortcodes)):
        publication_Links.append(f'https://www.instagram.com/p/{shortcodes[i]}')

def selenium_Launch(link):
    ua = dict(DesiredCapabilities.CHROME)
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=selenium")
    options.add_argument('headless') # non-display mode
    options.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(link)
    time.sleep(2.5)
    try:
        driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a''').click()
    except:
        print('\nXpath not found - :/ \n')
        driver.close()
        return ["", ""]

    time.sleep(2.5)

    # in first run or blocktologin, need to uncomment it once and loginin
    #driver.find_element_by_xpath("//input[@name='username']").send_keys(config.username)#config file / u can erase it and write your on here
    #driver.find_element_by_xpath("//input[@name='password']").send_keys(config.password)# psswd
    #driver.find_element_by_xpath(
    #    '''//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div''').click()

    data_List = [driver.current_url, driver.page_source]
    driver.close()
    return data_List

def get_Data(plinks):
    i = 0
    for url in plinks:
        input_List = selenium_Launch(url)
        i += 1
        print(f' ==== {i} ====')
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
        parsed_Data_Df.loc[len(parsed_Data_Df)] = [NameTag , SubscribersDiv, Discrp, input_List[0]]
        print(NameTag)
        print(SubscribersDiv)
        print(Discrp)
        print(input_List[0])
    parsed_Data_Df.drop_duplicates(keep=False, inplace=True)

def create_Table_Csv(p_df, csv_filename):
    p_df.to_csv(csv_filename, sep=';', encoding='utf-8', index = False)

def create_Table_Xls(p_df, xls_filename):
    p_df.to_excel(xls_filename, index=False, encoding="utf-8", sheet_name='Parsed_data')


if __name__ == "__main__":
    print("Hashtag_Killer v.0.1 (c) Exordio\n")
    hashtag = input('\nhashtag : ')
    print('\n\n ------------|| START PARSING ||------------\n')

    # Entering hashtag here -
    create_Publication_Link_List(get_Hashtag_Publication_Shortcodes(hashtag))
    #print(publication_Links)

    get_Data(publication_Links)

    print('\n ------------|| END PARSING ||------------\n\n')

    print(parsed_Data_Df)

    create_Table_Csv(parsed_Data_Df, 'Parsed_data.csv')
    create_Table_Xls(parsed_Data_Df, 'Parsed_data.xlsx')

    print("\n ======= END =======")




