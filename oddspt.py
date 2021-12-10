import json
import time
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver

client = pymongo.MongoClient("mongodb://vasco:rootadmin@bethub-shard-00-00.24hpv.mongodb.net:27017,bethub-shard-00-01.24hpv.mongodb.net:27017,bethub-shard-00-02.24hpv.mongodb.net:27017/BetHub?ssl=true&replicaSet=atlas-14c0oo-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.BetHub
db.games.delete_many({})


def scroll_all_down():
    lenOfPage = browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(2)
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

#def get_casa_aposta():

def create_json_add_to_mongo(id, home, away, v1, x, v2, arbitrage):
    object = {}
    object['game_id'] = id
    object['home'] = home
    object['away'] = away
    object['v1'] = v1
    object['x'] = x
    object['v2'] = v2
    object['percentage'] = arbitrage
    json_data = json.dumps(object)
    db.games.insert_one(object)




browser = webdriver.Chrome()
url = 'https://pt.odds.dog/'
browser.get(url)

scroll_all_down()

page_content = browser.page_source
site = BeautifulSoup(page_content, 'html.parser')
lista_todos = site.find(id="ContentGames")

id = 0

boxes = lista_todos.find_all('div', attrs={'class': 'box center tableBox shadowBox'})
for box in boxes:       #Por cada box de jogos que encontra
    for tr in box.find_all('tr'):       #Por cada jogo que encontra
        if(tr.find('div', attrs={'class': 'teamsGame team1'}) and tr.find('div', attrs={'class': 'teamsGame team2'})):

            home = tr.find('div', attrs={'class': 'teamsGame team1'}).find('div', attrs={'class': 'listNameTeam'}).contents[0]
            away = tr.find('div', attrs={'class': 'teamsGame team2'}).find('div', attrs={'class': 'listNameTeam'}).contents[0]

            odds_vector = []

            lista_odds = tr.find_all('td')
            for td in lista_odds:
                if(td.find('div', attrs={'class': 'tableOdds redirect'})):
                    td.find('div', attrs={'class': 'tableOdds redirect'})
                    odd = float(td.contents[0].text.replace(" ",""))
                    odds_vector.append(odd)

            v1 = odds_vector[0]
            x = odds_vector[1]
            v2 = odds_vector[2]
            arbitrage = (1/v1)+(1/x)+(1/v2)

            create_json_add_to_mongo(id, home, away, v1, x, v2, arbitrage)
            id += 1



