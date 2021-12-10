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

def create_json_add_to_mongo(id, date, home, home_logo, away, away_logo,  v1, x, v2, arbitrage):
    object = {}
    object['game_id'] = id
    object['date'] = date
    object['home'] = home
    object['home_logo'] = home_logo
    object['away'] = away
    object['away_logo'] = away_logo
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

            day = tr.find('div', attrs={'class': 'listDate'}).contents[0].text.replace(" ","")
            month = tr.find('div', attrs={'class': 'listDate'}).find('span', attrs={'class': 'monthGameTable'}).contents[0].text.replace(" ","")
            hour = tr.find('div', attrs={'class': 'listDate'}).find('span', attrs={'class': 'hourGameTable'}).contents[0].text.replace(" ","")
            date = day + "/" + month + " | " + hour

            home = tr.find('div', attrs={'class': 'teamsGame team1'}).find('div', attrs={'class': 'listNameTeam'}).contents[0]
            away = tr.find('div', attrs={'class': 'teamsGame team2'}).find('div', attrs={'class': 'listNameTeam'}).contents[0]

            home_logo = tr.find('div', attrs={'class': 'teamsGame team1'}).find('div', attrs={'class': 'logoTeamTable'}).find('img', attrs={'class': 'listLogoTeam'}).get("src")
            away_logo = tr.find('div', attrs={'class': 'teamsGame team2'}).find('div', attrs={'class': 'logoTeamTable'}).find('img', attrs={'class': 'listLogoTeam'}).get("src")

            odds_vector = []
            house_vector = []

            lista_odds = tr.find_all('td')
            for td in lista_odds:
                if(td.find('div', attrs={'class': 'tableOdds redirect'})):
                    td.find('div', attrs={'class': 'tableOdds redirect'})
                    odd = float(td.contents[0].text.replace(" ",""))
                    house = td.find('div', attrs={'class': 'housesList'}).get("data-brand")
                    odds_vector.append(odd)
                    house_vector.append(house)

            arbitrage = (1/odds_vector[0])+(1/odds_vector[1])+(1/odds_vector[2])
            v1 = str(odds_vector[0]) + " [" + house_vector[0] + "]"
            x = str(odds_vector[1]) + " [" + house_vector[1] + "]"
            v2 = str(odds_vector[2]) + " [" + house_vector[2] + "]"


            create_json_add_to_mongo(id, date, home, home_logo, away, away_logo, v1, x, v2, arbitrage)
            id += 1



