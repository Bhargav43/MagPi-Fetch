import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re, os
from TextPrinter import threadstart, threadquit


def getextensions(url):
    session = HTMLSession()
    page = session.get(url)
    parsedpage = BeautifulSoup(page.text, 'html.parser')

    hrefs = parsedpage.find_all(class_="c-button c-button--secondary u-mb-x2")
    hrefs = [tag['href'] for tag in hrefs]
    return hrefs

def PDF_URL(url):
    session = HTMLSession()
    page = session.get(url)
    parsedpage = BeautifulSoup(page.text, 'html.parser')

    return parsedpage.find(class_="c-link")['href']

def scrapper():
    #Function for Getting the Number of Issue-Pages
    pagecount = lambda: int((BeautifulSoup((HTMLSession().get('https://magpi.raspberrypi.org/issues')).text, 'html.parser')).find(class_="c-pagination__label").text[-1])

    #Function Getting the URL of Latest Edition Which Has a Different Xpath
    latest = lambda: (BeautifulSoup((HTMLSession().get('https://magpi.raspberrypi.org/issues')).text, 'html.parser')).find(class_="c-issue-actions__link c-link u-text-bold")['href']

    #Appending the Latest Edition's URL First
    urls = ['https://magpi.raspberrypi.org' + latest()]

    #Appending All the Issue Page's PDF's URLs
    for i in range(1, pagecount()+1):
        [urls.append('https://magpi.raspberrypi.org' + ele) for ele in getextensions('https://magpi.raspberrypi.org/issues?page='+str(i))]

    #Appending All the Books Page's PDF's URLs
    [urls.append('https://magpi.raspberrypi.org' + ele) for ele in getextensions('https://magpi.raspberrypi.org/books')]


    #Dictionary Out of Mag Name and pdf URLs
    url_sets = {re.search('^.*\/(.*)\?.*$', url).group(1): url for url in [PDF_URL(url) for url in urls]}

    return url_sets


def compareSizes(checklist, urls, path):
    incomplete = []
    print('\nThe Comparing Could Take a While As It Checks the Local with Network.')

    threadstart('Please be Patient')

    for file in checklist:
        while True:
            try:
                if int(os.stat(os.path.join(path, file)).st_size) != int(requests.get(urls[file], stream=True).headers['content-length']):
                    incomplete.append(file)
                break
            except Exception:
                print('\nNetwork Issue, Probably! Please Wait While I Retry...')
    threadquit()

    return incomplete
