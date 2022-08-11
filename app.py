import sys
from tkinter import *
import feedparser  # Parse RSS feed
from qbittorrent import Client  # Qbittorrent Client
import re  # Regular Expressions
import inquirer  # Question Choice Library

animeList = []

qb = Client("http://127.0.0.1:8080/")
qb.login('nafislord', 'animedownload')

animeFeed = feedparser.parse(
    "https://subsplease.org/rss/?r=1080")

for i in range(0, len(animeFeed.entries)):
    animeList.append(animeFeed.entries[i].title)


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


main()
