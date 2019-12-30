import pickle
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import time

players = pickle.load(open("players.pkl", 'rb'))
df = pd.DataFrame(
        columns=['Name:', 'Attacking Prowess:', 'Ball Control:', 'Dribbling:', 'Low Pass:', 'Lofted Pass:', 'Finishing:', 'Place Kicking:',
                 'Swerve:', 'Header:', 'Defensive Prowess:', 'Ball Winning:', 'Kicking Power:', 'Speed:', 'Explosive Power:', 'Unwavering Balance:',
                 'Physical Contact:', 'Jump:', 'Stamina:'])
rows = []
for player in players:
    try:
        numbers = [str(s) for s in player if s.isdigit()]
        id = int("".join(numbers))
        url = "http://pesdb.net/pes2019/?id=" + str(id)
        website = requests.get(url)
        print(website.status_code)
        if website.status_code == 429:
            print("stopped")
            time.sleep(190)
            website = requests.get(url)
        soup = BeautifulSoup(website.content, "lxml")
        table = soup.find(id="table_0")
        tr = table.find("tr")
        th_content = []
        running_list = []
        for attribute in tr.contents:
            attr = str(attribute)
            name = re.findall("Player Name:</th><td>(.+?)</td>", attr)
            if name:
                name = name
                running_list.append(name)
            match = re.findall("id=(.+?)</td></tr>", attr)
            if match:
                match = match
                td_content = re.findall(">(.+?)'", str(match))
                td_content = [x for x in td_content if "40" not in x] #removes goalkeeper stats
                td_content = [x for x in td_content if "<" not in x]
                td_content = [int(x) for x in td_content]
                running_list += td_content

        df.loc[len(df)] = running_list
        print(df)
        df.to_csv("player_stats.csv")
    except Exception as e:
        print(player)
        print(e)




