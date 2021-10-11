import requests
import praw
from dotenv import load_dotenv
import os
from sys import argv


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

    for post in unixpn.search(DE, sort=sort, limit=limit):
        if not post.is_self:
            yield (post.url, post.id)


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
    print(f'Usage: {argv[0]} <desktop environment>')


def main():
    if len(argv) == 2:
        download(argv[1])
    else:
        printUsage()


if __name__ == '__main__':
    main()
