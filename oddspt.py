from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

df = pd.DataFrame(columns=['Home', 'Away', 'V1', 'X', 'V2', 'Arbitrage'])
writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()

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






browser = webdriver.Chrome()
url = 'https://odds.pt/competicao/brasil-brasileirao-serie-a/1/'
browser.get(url)

scroll_all_down()

page_content = browser.page_source
site = BeautifulSoup(page_content, 'html.parser')
lista_todos = site.find(id="ContentGames")
boxes = lista_todos.find_all('div', attrs={'class': 'box center tableBox shadowBox'})
for box in boxes:
    for tr in box.find_all('tr'):
        if(tr.find('div', attrs={'class': 'teamsGame team1'}) and tr.find('div', attrs={'class': 'teamsGame team2'})):

            home = tr.find('div', attrs={'class': 'teamsGame team1'}).find('div', attrs={'class': 'listNameTeam'}).contents[0]
            print(home)
            away = tr.find('div', attrs={'class': 'teamsGame team2'}).find('div', attrs={'class': 'listNameTeam'}).contents[0]
            print(away)

            odds_vector = []

            lista_odds = tr.find_all('td')
            for td in lista_odds:
                if(td.find('div', attrs={'class': 'tableOdds redirect'})):
                    td.find('div', attrs={'class': 'tableOdds redirect'})
                    odd = float(td.contents[0].text.replace(" ",""))
                    odds_vector.append(odd)

            print(odds_vector)
            v1 = odds_vector[0]
            x = odds_vector[1]
            v2 = odds_vector[2]

            arbitrage = (1/v1)+(1/x)+(1/v2)
            print(arbitrage)


            data = pd.DataFrame([[home, away, v1, x, v2, arbitrage]])
            data.to_excel(writer, index=False)
            writer.save()
            print("------------------------------------")


