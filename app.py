import sys
import time
import feedparser  # Parse RSS feed
from qbittorrent import Client  # Qbittorrent Client
import re  # Regular Expressions
import inquirer  # Question Choice Library

animeList = []
animeFeed = feedparser.parse(
    "https://subsplease.org/rss/?r=1080")

qb = Client("http://127.0.0.1:8080/")
qb.login('nafislord', 'animedownload')


def addFeedData():
    for i in range(0, len(animeFeed.entries)):
        parsedTime = time.strftime(
            "%Y-%m-%d %H:%M:%S", animeFeed.entries[i].published_parsed)
        parseTitle = animeFeed.entries[i].title
        animeList.append((parsedTime, parseTitle))

    sortList()


def sortList():
    animeList.sort()


def listAnime(title):
    r = re.compile(".*"+title, re.IGNORECASE)
    foundItems = list(filter(r.match, animeList))
    if (foundItems == []):
        print("No Anime Found")
        main()
    answer = inquirer.prompt(
        [inquirer.List('anime', message="Which Anime do you wanna download?", choices=foundItems)])
    downloadAnime(answer["anime"])


def downloadAnime(title):
    for i in range(0, len(animeList)):
        if title == animeList[i]:
            qb.download_from_link(animeFeed.entries[i].link)
            print("Downloading " + title)
            break


def main():
    choice = input(
        "Type Anime Name to Download or type Quit! to exit: ")
    if choice == "Quit!":
        sys.exit()
    else:
        listAnime(choice)
        main()


addFeedData()
# main()
