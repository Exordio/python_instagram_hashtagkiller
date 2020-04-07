import requests
import json
import time
import instagram_explore as ie

import numpy as np
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

links = []

def find(key, dictionary):
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

def get_Hashtag_Publication_Shortcodes(hashtag):
    res = ie.tag(hashtag)
    return list(find('shortcode', res.data))



if __name__ == "__main__":
    print("Hashtag_Killer v.0.1 (c) Exordio\n")
    # Entering hashtag here -
    x = get_Hashtag_Publication_Shortcodes(input('hashtag : '))
    print(x)
    for i in range(len(x)):
        links.append(f'www.instagram.com/p/{x[i]}')

    print(links)

    

