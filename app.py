import sys
import time
import feedparser  # Parse RSS feed
from qbittorrent import Client  # Qbittorrent Client
import re  # Regular Expressions

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


def searchAnime(title):
    r = re.compile(".*"+title, re.IGNORECASE)
    result_list = filter(lambda tup: any(map(r.match, tup)), animeList)
    return result_list


def downloadAnime(title):
    for i in range(0, len(animeFeed.entries)):
        if title == animeFeed.entries[i].title:
            print("Downloading " + title)
            qb.download_from_link(animeFeed.entries[i].link)
            break


addFeedData()
