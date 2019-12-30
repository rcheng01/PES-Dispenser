import pickle
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

players = pickle.load(open("players.pkl", 'rb'))
array = np.asarray(players)

rows = []
for i in range(0,1):
    link = array[i]
    numbers = [str(s) for s in link if s.isdigit()]
    id = int("".join(numbers))
    url = "http://pesdb.net/pes2019/?id=" + str(id)
    website = requests.get(url)
    soup = BeautifulSoup(website.content, "lxml")
    table = soup.find(id="table_0")
    tr = table.find("tr")
    attr_row = []
    th_content = []
    df = pd.DataFrame(
        columns=['Attacking Prowess:', 'Ball Control:', 'Low Pass:', 'Lofted Pass:', 'Finishing:', 'Place Kicking:',
                 'Swerve:', 'Header:', 'Kicking Power:', 'Speed:', 'Explosive Power:', 'Unwavering Balance:',
                 'Physical Contact:', 'Jump:', 'Stamina:'])
    for attribute in tr.contents:
        attr = str(attribute)
        name = re.findall("Player Name:</th><td>(.+?)</td>", attr)
        if name:
            name = name
        match = re.findall("id=(.+?)</td></tr>", attr)
        if match:
            match = match
            td_content = re.findall(">(.+?)'", str(match))
            td_content = [x for x in td_content if "40" not in x] #removes goalkeeper stats
            td_content = [x for x in td_content if "<" not in x]
            td_content = [int(x) for x in td_content]
            df.loc[name] = td_content
            print(df)




