# https://cdn.fangraphs.com/api/players/stats?playerid=20123&position=OF&z=1646561463112
# https://stackoverflow.com/questions/45867355/beautiful-soup-fetch-dynamic-table-data
# python3 -m pip install webdriver_manager
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv


def get_html(url):
    # browser = webdriver.Chrome(
    #     '/Users/etai_barash/Desktop/Comp_Sci/fantasyBaseball/playerStats/chromedriver')
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()))
    browser.get(url)
    time.sleep(3)
    return browser.page_source


def get_player_ids():
    player_ids = []
    with open('playerIds.csv', mode='r') as players_csv:
        players_reader = csv.DictReader(players_csv)
        for row in players_reader:
            player_ids.append(
                dict({'name': row['FANGRAPHSNAME'], 'id': row['IDFANGRAPHS']}))

    return player_ids


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('div', {'id': 'dashboard'})
    table = div.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr', {'class': 'row-mlb-season'})
    rows.extend(table_body.find_all('tr', {'class': 'row-projection'}))
    for row in rows:
        for td in row.find_all('td', {'data-stat': 'Season'}):
            if td.get_text(strip=True) == '2022':
                projSystem = row.find('td', {'data-stat': 'Team'})
                if projSystem.get_text(strip=True) == 'THE BAT X':
                    woba = row.find('td', {'data-stat': 'wOBA'})
                    parsedWoba = woba.get_text(strip=True)
                    wrc = row.find('td', {'data-stat': 'wRC+'})
                    parsedwrc = wrc.get_text(strip=True)
                    print('2022 wOBA: ' + str(parsedWoba))
                    print('2022 wRC+: ' + str(parsedwrc))
            elif td.get_text(strip=True) == '2021':
                woba = row.find('td', {'data-stat': 'wOBA'})
                parsedWoba = woba.get_text(strip=True)
                xwoba = row.find('td', {'data-stat': 'xwOBA'})
                parsedxWoba = xwoba.get_text(strip=True)
                wrc = row.find('td', {'data-stat': 'wRC+'})
                parsedwrc = wrc.get_text(strip=True)
                print('2021 wOBA: ' + str(parsedWoba))
                print('2021 xwOBA: ' + str(parsedxWoba))
                print('2021 wRC+: ' + str(parsedwrc))


def main():
    player_ids = get_player_ids()

    print("What player are you looking for?")
    desired_name = input()

    while desired_name != 'q':
        desired_id = 0

        for player_id in player_ids:
            if player_id['name'].lower() == desired_name.lower():
                desired_id = player_id['id']

        if desired_id == 0:
            print("Could not find player")
            input()

        desired_name = desired_name.replace(" ", "-")

        url = "https://www.fangraphs.com/players/" + \
            desired_name.lower() + "/" + str(desired_id) + "/stats"
        html = get_html(url)

        parse_html(html)

        print("What player are you looking for?")
        desired_name = input()


if __name__ == "__main__":
    main()
