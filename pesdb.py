import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pickle

players = []
for i in range(1,401):
    url = "http://pesdb.net/pes2019/?page=" + str(i)
    website = requests.get(url)
    soup = BeautifulSoup(website.text, "lxml")
    new_players = soup.select("a[href*=id]")
    if not new_players:
        print("\nstopped")
        time.sleep(190)
        website = requests.get(url)
        soup = BeautifulSoup(website.text, "lxml")
        new_players = soup.select("a[href*=id]")
    players += new_players
    updated_players = [str(p) for p in players if 'http' not in str(p)]
    print(updated_players)
    pickle.dump(updated_players, open('players.pkl', 'wb'))
    time.sleep(0.5)





