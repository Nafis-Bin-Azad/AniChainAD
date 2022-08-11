from tkinter import *
import feedparser  # Parse RSS feed
import sys
from qbittorrent import Client  # Qbittorrent Client
import re  # Regular Expressions
import inquirer  # Question Choice Library


# https://www.thepythoncode.com/article/download-torrent-files-in-python
# 'title', 'title_detail', 'links', 'link', 'id', 'guidislink', 'published', 'published_parsed', 'tags', 'subsplease_size'
qb = Client("http://127.0.0.1:8080/")
qb.login('nafislord', 'animedownload')

NewsFeed = feedparser.parse(
    "https://subsplease.org/rss/?r=1080")

animeList = []

for i in range(0, len(NewsFeed.entries)):
    animeList.append(NewsFeed.entries[i].title)
    # print(NewsFeed.entries[i].title)
    # print(NewsFeed.entries[i].published)


def listAnime(title):
    r = re.compile(".*"+title, re.IGNORECASE)
    foundItems = list(filter(r.match, animeList))
    print(foundItems)
    # for i in range(0, len(animeList)):
    #     x =

    #     if title ==:
    #         print(NewsFeed.entries[i].link)
    #         qb.download_from_link(NewsFeed.entries[i].link)
    #         break
    #     else:
    #         print("Anime not found")
    #         main()


# magnet_link = NewsFeed.entries[0].link
# qb.download_from_link(magnet_link)

torrents = qb.torrents()

for torrent in torrents:
    print(torrent['name'])


def main():
    choice = input(
        "Type Anime Name to Download or type Quit! to exit: ")
    if choice == "Quit!":
        sys.exit()
    else:
        listAnime(choice)
        main()


main()
