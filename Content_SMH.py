##################################################
# Basic HTML fetching and parsing for SMH.com.au #
##################################################

import urllib2
from bs4 import BeautifulSoup



def fetchArticleIndex():
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'SMH-Terminal-App-v1')]
    pageData = opener.open("http://www.smh.com.au").read()
    soup = BeautifulSoup(pageData)

    headlines = soup('h3', {'class': 'story__headline'})

    articles = []

    for x in headlines:
        if x('a')[0].string is not None and x('a')[0]['href'].encode("utf-8").strip()[:21] == "http://www.smh.com.au":
            articles.append({
                "title": x('a')[0].string.encode("utf-8").strip(),
                "url": x('a')[0]['href'].encode("utf-8").strip()
            })
    
    return articles


def fetchArticleContent(url):

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'SMH-Terminal-App-v1')]
    pageData = opener.open(url).read()
    soup = BeautifulSoup(pageData)
    
    contentDiv = soup('div', {'class': 'article__body'})[0].find_all('p')
    headerDiv = soup('header', {'class': 'article__header'})[0]
    
    try:
        authors = headerDiv('li', {'class': 'signature__name'})[0].find_all('h5')
    except:
        authors = []
    
    try:
        articleTitle = headerDiv.find_all('h1')[0].string
    except:
        articleTitle = ""
    
    try:
        articleDate = headerDiv('time', {'class': 'signature__datetime'})[0].string
    except:
        articleDate = ""
    
    articleText = ""
    articleAuthor = ""

    for x in contentDiv:
        if x.string is not None:
            articleText += x.string + "\n"

    for x in authors:
        if articleAuthor != "":
            articleAuthor += ", "
        
        if x.string is not None:
            articleAuthor += x.string

    return {
        "title": articleTitle.strip(),
        "date": articleDate.strip(),
        "author": articleAuthor.strip(),
        "body": articleText.strip()
    }
