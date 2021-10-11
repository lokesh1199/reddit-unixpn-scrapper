import os
from getopt import getopt
from sys import argv

import praw
import requests
from dotenv import load_dotenv


def getKeys():
    load_dotenv()
    clientID = os.getenv('clientID')
    clientSecret = os.getenv('clientSecret')

    return (clientID, clientSecret)


def getPosts(DE, sort, limit):
    clientID, clientSecret = getKeys()

    reddit = praw.Reddit(
        client_id=clientID,
        client_secret=clientSecret,
        user_agent='unixpn-scrapper',
    )
    unixpn = reddit.subreddit('unixporn')

    validExtensions = ['jpg', 'jpeg', 'png', 'gif']
    for post in unixpn.search(DE, sort=sort, limit=100):
        if post.url.split('.')[-1] in validExtensions:
            limit -= 1
            yield (post.url, post.id)
        if limit == 0:
            break


def downloadImage(url, fileName):
    res = requests.get(url)

    with open(fileName, 'wb') as f:
        for chunk in res.iter_content():
            f.write(chunk)


def createFolder(name):
    if not os.path.isdir(name):
        os.mkdir(name)


def download(DE, sort='hot', limit=5):
    folderName = 'unixpn-images'
    createFolder(folderName)

    for post in getPosts(DE, sort, limit):
        url, fileName = post
        ext = url.split('.')[-1]
        fileName = folderName + '/' + fileName + '.' + ext
        downloadImage(url, fileName)


def printUsage():
    print('Usage:')
    print(f'\t{argv[0]} [options] <desktop environment>')
    print('Options:')
    print('\t-s\t\t-> sort (new, hot, top)')
    print('\t-n\t\t-> number of images')


def main():
    if len(argv) >= 2:
        opts, args = getopt(argv[1:], 's:n:', ['sort', 'count'])
        DE = args[0]
        kwargs = {}
        for key, value in opts:
            if key == '-s':
                kwargs['sort'] = value
            elif key == '-n':
                kwargs['limit'] = int(value)
        download(DE, **kwargs)
    else:
        printUsage()


if __name__ == '__main__':
    main()
