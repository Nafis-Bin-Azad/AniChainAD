from tkinter import *
import feedparser

NewsFeed = feedparser.parse(
    "https://subsplease.org/rss/?r=1080")

for i in range(0, len(NewsFeed.entries)):
    print(NewsFeed.entries[i].title)
    # print(NewsFeed.entries[i].link)
    # print(NewsFeed.entries[i].published)
    # print("\n")

    # print(NewsFeed.entries[i].title)
# entry = NewsFeed.entries[1]

# print(entry.keys())
# for ()
