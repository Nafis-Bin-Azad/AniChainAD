import sys
import time
import feedparser  # Parse RSS feed
import urllib.parse
from qbittorrent import Client  # Qbittorrent Client
import re  # Regular Expressions

animeList = []
rssFeed = "https://nyaa.si/?page=rss&c=0_0&f=0&&u=subsplease&q=one+piece+1080p"
animeFeed = None
animeListToTrack = ["One Piece"]
animeGroups = ["subsplease", "yameii"]
downloadResolution = "1080p"

qb = Client("http://127.0.0.1:8080/")
qb.login('nafislord', 'animedownload')


def generateRSSFeedString(animeGroup, resolution, searchTerm):
    query = f'{searchTerm} {resolution}'
    uriSearchQuery = urllib.parse.quote(query)
    feedString = f"https://nyaa.si/?page=rss&u={animeGroup}&q={uriSearchQuery}"


def parseFeed():
    animeFeed = feedparser.parse(rssFeed)


def addFeedData():
    parseFeed()
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
