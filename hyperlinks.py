import pickle
import pandas as pd
import numpy as np
import requests
import lxml.html as lh
from bs4 import BeautifulSoup

players = pickle.load(open("players.pkl", 'rb'))
array = np.asarray(players)

for i in range(0,1):
    link = array[i]
    numbers = [str(s) for s in link if s.isdigit()]
    id = int("".join(numbers))
    url = "http://pesdb.net/pes2019/?id=" + str(id)
    website = requests.get(url)
    doc = lh.fromstring(website.content)
    tr_elements = doc.xpath('//tr')

for t in tr_elements[0]:
    name = t.text_content()
    name = name.

Dict =
