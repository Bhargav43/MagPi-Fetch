# import requests
# from requests_html import HTMLSession
# from bs4 import BeautifulSoup
# import re, os, time
import sys
from TextPrinter import threadstart, threadquit
import ScrapperFunctions as sc
import SelectorFunctions as se
import WriterFunction as wf

def main():

    print('\nKindly Understand, The Purpose of The Program is to Automate The Process of Downloading MagPi PDFs But The Download Speed Can Nowhere be Near the General Browser\'s Level.\n')

    threadstart('Please Wait')

    try:
        url_sets, loc = se.selectlist(sc.scrapper())
    except Exception:
        threadquit()
        print('Network Issue. Please Check Your Connection And Retry.')
        sys.exit(0)

    #[print(k,'\t', v) for (k,v) in zip(wf.global_selectionlist, wf.global_selectionlist.values())]

    #Running the Whole List to Download. Subsetting Will be Done by Global Variables.
    [wf.writePDF(name, url_sets[name], loc) for name in url_sets]

    input(f'\nFiles Have Been Successfully Downloaded to {loc}\nPress Any Key to Exit.')

if __name__=="__main__":
    main()

