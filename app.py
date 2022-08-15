import time
import json
import os
import feedparser  # Parse RSS feed
import urllib.parse
import hashlib
from qbittorrent import Client  # Qbittorrent Client
import re  # Regular Expressions

periodToCheckForNewEpisodes = 3600  # in seconds
defaultAnimeSearchGroup = 'subsplease'
defaultDownloadResolution = '1080p'

qb = Client("http://127.0.0.1:8080/")
qb.login('nafislord', 'animedownload')


# Library functions if update is needed can be changed here

def parseFeed(rssFeedLink):
    """This function will parse a link that is an RSS feed and return the parsed data

    :param rssFeedLink: link to the RSS feed
    :type rssFeedLink: string
    :return: parsed data from the RSS feed
    :rtype: json object array
    """
    return feedparser.parse(rssFeedLink)


def textToURIFormat(text):
    """This will convert a text string to a URI format

    :param text: the text to convert to URI format
    :type text: string
    :return: the text in URI format
    :rtype: string
    """
    return urllib.parse.quote(text)


def generateAnimeHash(link, title):
    """This generates a md5 hash with link and title of the anime

    :param link: link of anime, title: title of anime
    :type link: string, title: string
    :return: MD5 hash of link and title
    :rtype: string
    """
    textToEncode = link + title
    return hashlib.md5(textToEncode.encode('utf-8')).hexdigest()


def downloadAnime(link):
    try:
        # params = {
        #     'save_path': savePath,
        #     'storage_mode': lt.storage_mode_t(2),
        #     'paused': False,
        #     'auto_managed': True,
        #     'duplicate_is_error': True
        # }
        # ses = lt.session()
        # ses.listen_on(6881, 6891)
        # handle = lt.add_magnet_uri(ses, link, params)
        # ses.start_dht()

        # while (not handle.has_metadata()):
        #     time.sleep(1)

        # while (handle.status().state != lt.torrent_status.seeding):
        #     s = handle.status()

        #     time.sleep(5)
        qb.download_from_link(link)
    except:
        pass


def generateRSSFeedString(animeGroup, resolution, searchTerm):
    query = f'{searchTerm} {resolution}'
    uriSearchQuery = textToURIFormat(query)
    return f"https://nyaa.si/?page=rss&u={animeGroup}&q={uriSearchQuery}"


# def addFeedData():
#     parseFeed()
#     for i in range(0, len(animeFeedData.entries)):
#         parsedTime = time.strftime(
#             "%Y-%m-%d %H:%M:%S", animeFeedData.entries[i].published_parsed)
#         parseTitle = animeFeedData.entries[i].title
#         animeFeedData.append((parsedTime, parseTitle))

#     sortList()


# def sortList():
#     animeFeedData.sort()


# def searchAnime(title, list):
#     r = re.compile(".*"+title, re.IGNORECASE)
#     result_list = filter(lambda tup: any(map(r.match, tup)), list)
#     return result_list


def checkForNewEpisode(oldItem, newItem):

    newHash = generateAnimeHash(
        newItem.link, newItem.title)
    if newHash == oldItem['lastHash']:
        print("No new episode found for " + oldItem['title'])
        return False
    else:
        print("New episode found")
        return True


def doesPrevListDataExist():
    if os.path.exists('animeList.json') and os.path.getsize('animeList.json') > 0:
        print("Anime List Data exists and is readable")
        return True
    else:
        print("Anime List Data file is missing or is not readable")
        return False


def loadData():
    with open('animeList.json', 'r') as f:
        data = json.load(f)
        return data


def writeDataToJSON(data):
    with open('animeList.json', 'w') as f:
        json.dump(data, f)


def searchForNewEpisodes(data):
    for index, item in enumerate(data):
        rssLink = generateRSSFeedString(
            item['animeGroup'], item['resolution'], item['title'])
        animeFeedData = parseFeed(rssLink)
        # searchAnime(item["title"], animeFeedData) # filter out the anime from the list
        newItem = animeFeedData.entries[0]

        if checkForNewEpisode(oldItem=item, newItem=newItem):
            print("Downloading " + newItem.title)
            downloadAnime(newItem.link)
            newHash = generateAnimeHash(newItem.link, newItem.title)
            data[index].update({'lastHash': newHash})


def main():
    if doesPrevListDataExist():
        while (True):
            data = loadData()
            # Check for new episodes for each anime in the list
            searchForNewEpisodes(data)
            writeDataToJSON(data)
            time.sleep(periodToCheckForNewEpisodes)
    else:
        print("Creating new anime list data")
        print("Please input anime to track")
        data = [{
            'title': input('Anime Name: '),
            'lastHash': 'None',
            'animeGroup': defaultAnimeSearchGroup,
            'resolution': defaultDownloadResolution,
        }]
        writeDataToJSON(data)


main()
