from lxml import html
import requests
import re
import math


def main():
    find_player_stats("Juan Soto")


def find_player_stats(playerName):
    parsedPlayerName = playerName.replace(" ", "-")
    # page = "https://www.fangraphs.com/players/" + parsedPlayerName + "/" + "20123"
    page = "https://www.fangraphs.com/players/juan-soto/20123/"

    result = requests.get(page)
    print(result)
    tree = html.fromstring(result.content)

    print(tree)

    # //div[@id="dashboard"]//div[@class="table-fixed"]//table

    table = tree.xpath('//*[@id="dashboard"]/div[3]/div/div/div/div[2]/table')

    print(table)


if __name__ == "__main__":
    main()
