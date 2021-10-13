import concurrent.futures
import os
from getopt import getopt
from sys import argv

import praw
import requests


def getKeys():
    clientID = 'fA4Vlqo4tHyzqVgg1UEr3A'
    clientSecret = 'vd5eODvqcl8CdxLQhe9Lp5SvOVl4qQ'

    return (clientID, clientSecret)


def getPosts(DE, sort, count):
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
            count -= 1
            yield (post.url, post.id)
        if count == 0:
            break


def downloadImage(details):
    url, fileName = details
    res = requests.get(url)

    if os.path.exists(fileName):
        print(fileName.split('/')[-1], 'already exists')
        return

    with open(fileName, 'wb') as f:
        for chunk in res.iter_content():
            f.write(chunk)


def createFolder(name):
    if not os.path.isdir(name):
        os.mkdir(name)


def download(DE, sort='hot', count=5):
    folderName = 'unixpn-images'
    createFolder(folderName)

    details = []
    for post in getPosts(DE, sort, count):
        url, fileName = post
        ext = url.split('.')[-1]
        fileName = folderName + '/' + fileName + '.' + ext
        details.append((url, fileName))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(downloadImage, details)


def printUsage():
    print('Usage:')
    print(f'\t{argv[0]} [options] <desktop environment>')
    print('Options:')
    print('\t-s\t\t-> sort (new, hot, top)')
    print('\t-n\t\t-> number of images')


def main():
    if len(argv) >= 2:
        opts, args = getopt(argv[1:], 's:n:')
        DE = args[0]
        kwargs = {}
        for key, value in opts:
            if key == '-s':
                kwargs['sort'] = value
            elif key == '-n':
                kwargs['count'] = int(value)
        download(DE, **kwargs)
    else:
        printUsage()


if __name__ == '__main__':
    main()
