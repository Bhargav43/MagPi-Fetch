# [MagPi-Fetch](https://github.com/Bhargav43/MagPi-Fetch)
## Purpose :bulb:
The [MagPi](https://magpi.raspberrypi.org/)  is the official Raspberry Pi magazine. Written for the community, it is packed with Pi-themed projects, computing and electronics tutorials, how-to guides, and the latest community news and events.

The softcopies of these mags are open for everyone online. You can visit [Issues](https://magpi.raspberrypi.org/issues) section and [Books](https://magpi.raspberrypi.org/books) section of [magpi.raspberrypi.org](https://magpi.raspberrypi.org/) for downloading manually.

[**MagPi-Fetch**](https://github.com/Bhargav43/MagPi-Fetch) is a simple app designed for automating the process of downloading the mags from the website with few inputs rather than visiting individual pages and the respective download redirects.

## Base System's Configurations :wrench:
**Sno.** | **Name** | **Version/Config.**
-------: | :------: | :------------------
1 | Operating System | Windows 10 x64 bit
2 | Python | Version 3.7.0 x64 bit
3 | PyInstaller | Version 3.6
4 | IDE | Pyzo 4.10.2 x64 bit

_Recommendation: Except for Type of OS (Windows), other configurations doesn't matter even if you don't have Python in your system, if you are using the [`executable`](https://github.com/Bhargav43/MagPi-Fetch/blob/master/MagPi-Fetch.exe) directly. Try It._

## Requirements :heavy_exclamation_mark:
There aren't any mandates for this. Yet I recommend you to have the following.
1. Reliable internet connection as the downloads process in buffer.
1. Considerable space in the location of downloads.

By 31-May-2020,
* No. of Mags = 121
* Space Occupied = 2.58 GB
* Time Consumed = 30 mins. (approx.)

## Imported Modules :package:
Sn | **Module** | **Type** | **Version**
-: | :--------: | :------- | :----------
1 | os | *Built-in* | NA
2 | time | *Built-in* | NA
3 | re | *Built-in* | NA
4 | requests | *PyPI Installed* | 2.23.0
5 | requests_html | *PyPI Installed* | 0.10.0
6 | beautifulsoup4 | *PyPI Installed* | 4.9.1

## [Scripts](https://github.com/Bhargav43/MagPi-Fetch/tree/master/Scripts) :page_facing_up:
### 1/5 [MagPi-Fetch.py](https://github.com/Bhargav43/MagPi-Fetch/blob/master/Scripts/MagPi-Fetch.py)
```python
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
```
### 2/5 [ScrapperFunctions.py](https://github.com/Bhargav43/MagPi-Fetch/blob/master/Scripts/ScrapperFunctions.py)
```python
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
```
### 3/5 [SelectorFunctions.py](https://github.com/Bhargav43/MagPi-Fetch/blob/master/Scripts/SelectorFunctions.py)
```python
import os, time, sys
from TextPrinter import threadquit
import WriterFunction as wf
import ScrapperFunctions as sc

global_selectionlist = dict()

def userInput(mags):

    op, sel = -1, []

    print('\nPlease Enter the Location to Download the Files.\nExample:\tC:\\Users\\Bhargav\\Downloads')
    while True:
        try:
            loc = input('Your Input:\t')

            if os.path.isdir(loc):
                break
            else:
                raise
        except Exception:
            print('Invalid Path. Please Re-enter a Valid Directory\'s Path.')


    print('\nNow, Please Select The Type of Download You Want.\n1. Download One \n2. Selective Download\n3. Download All\n4. Missing and Incomplete')
    while True:
        try:
            op = int(input('\nEnter 1, 2, 3 or 4:\t'))
            if op in (1,2,3,4):
                break
            else:
                raise
        except Exception:
            print('Invalid Entry.')


    if op == 1:
        print('Enter Sno. or the Alias Number From the Above Displayed List.', end =' ')
        while True:
            try:
                val = int(input('Your Selection:\t'))
                if val in range(1, len(mags)+1) or val in [-a for a in range(1, len(mags)+1)]:
                    sel.append(val)
                    break
                else:
                    print('Value Out of Bounds.', end=' ')
                    raise
            except Exception:
                print('Invalid String. Retry.')

    elif op == 2:
        print('\nEnter List in Combination of Indexes Separated by Commas and Hyphens (Not Aliases, Only Sno.).\nExample: 1, 3-5, 9')
        while True:
            try:
                string = input('Your Selection:\t').split(',')
                for s in string:
                    if '-' in s:
                        if int(s.split('-')[0]) > int(s.split('-')[1]):
                            print('Range Error: Should be Lower to Higher.', end=' ')
                            raise
                        elif int(s.split('-')[0]) < 1 or int(s.split('-')[1]) > len(mags):
                            print(f'Index Out of Bounds [1,{len(mags)}] Error.', end=' ')
                            raise
                    elif int(s) < 1 or int(s) > len(mags):
                        print(f'Index Out of Bounds [1,{len(mags)}] Error.', end=' ')
                        raise

                [[sel.append(a) for a in range(int(ele.split('-')[0]), int(ele.split('-')[1])+1)] if '-' in ele else sel.append(int(ele)) for ele in string]
                break
            except Exception as e:
                print(e)
                print('Invalid String. Retry.')

    elif op == 3:
        print(f'\n({len(mags)} MagPi PDFs)*(Avg. Size 25 MB) = {len(mags)*25} MB approx.', end =' ')
        while True:
            flag  = input('Are You Sure You Want to Download All? [Y/N]\t').upper()
            if flag == 'Y':
                sel = [val for val in range(1, len(mags)+1)]
                break
            elif flag == 'N':
                return 'No', -1
            else:
                print('Invalid Entry')

    else:
        checklist, missing = [], []
        existing = os.listdir(loc)
        [checklist.append(mag) if mag in existing else missing.append(mag) for mag in mags]
        incomplete = sc.compareSizes(checklist, mags, loc)

        [sel.append([m for m in mags].index(ele)+1) for ele in missing+incomplete]
        if len(incomplete) != 0:
            print('\nIncomplete Downloads:')
            [print(i) for i in incomplete]
        else:
            print('\nIncomplete Downloads:\n~None~')
        if len(missing) != 0:
            print('\nMissing Downloads:')
            [print(m) for m in missing]
        else:
            print('\nMissing Downloads:\n~None~')
        if len(incomplete)+len(missing) > 99:
            while True:
                print(f'\n({len(incomplete)+len(missing)} MagPi PDFs)*(Avg. Size 25 MB) = {(len(incomplete)+len(missing))*25} MB approx.', end =' ')
                flag  = input('Are You Sure You Want to Download All? [Y/N]\t').upper()
                if flag == 'Y':
                    break
                elif flag == 'N':
                    return 'No', -1
                else:
                    print('Invalid Entry')
        elif len(incomplete)+len(missing) == 0:
            input(f'\nAll Files Already Exist at {loc}\nPress Any Key to Exit the Console.')
            sys.exit(0)
        print('\n')

    return sel, loc


def selectlist(url_sets):
    global global_selectionlist

    threadquit()

    names = [key for key in url_sets]   #List of Mag-Names

    declare = lambda a: {a: True}
    setTrue = lambda:(globals().update(global_selectionlist = {name: True for name in global_selectionlist}))
    setFalse = lambda:(globals().update(global_selectionlist = {name: False for name in global_selectionlist}))

    #global_selectionlist's sets declaration
    [global_selectionlist.update(aSet) for aSet in list(map(declare, names))]

    printList = lambda mags: (print(f'\nList of {len(mags)} Raspberry Pi Magz on Site Are as Follows:'),
                                time.sleep(2),
                                print('Sno.\tAlias No.\tName'),
                                [print(f'{i+1}\t{-(len(mags)-i)}\t{mags[i]}') for i in range(len(mags))])

    while True:
        printList(names)
        numList, loc = userInput(url_sets)
        if numList != 'No':
            break
        setFalse()

    selected = [names[int(l)] if l<0 else names[int(l)-1] for l in numList]
    if len(selected)<len(names)/2:
        setFalse()
        [global_selectionlist.__setitem__(name, True) for name in selected]
    else:
        setTrue()
        [global_selectionlist.__setitem__(name, False) for name in [name for name in names if name not in selected]]

    wf.global_selectionlist = global_selectionlist
    return url_sets, loc
```
### 4/5 [TextPrinter.py](https://github.com/Bhargav43/MagPi-Fetch/blob/master/Scripts/TextPrinter.py)
```python
import time
import sys
import threading

thread, stop_thread = False, False

def getpadding(string):
    try:
        width = os.get_terminal_size().columns
    except Exception:
        width = 40 if len(str(string)) < 38 else 60
    gap = width - len(str(string))
    if gap % 2 == 0:
        return int(gap/2), int(gap/2)
    else:
        return int((gap+1)/2), int((gap-1)/2)

def TextPrinter(string):
    start, end = getpadding(string)
    while True:
        global stop_thread
        if stop_thread:
            break

        for i in range(start):
            sys.stdout.write('-')
            sys.stdout.flush()
            time.sleep(0.05)
        for s in string:
            if s.isupper():
                for i in range(65, ord(s)+1):
                    time.sleep(0.03)
                    sys.stdout.write('\b') if i!=65 else sys.stdout.write('')
                    sys.stdout.flush()
                    sys.stdout.write(chr(i))
                    sys.stdout.flush()
            elif s.islower():
                for i in range(97, ord(s)+1):
                    time.sleep(0.03)
                    sys.stdout.write('\b') if i!=97 else sys.stdout.write('')
                    sys.stdout.flush()
                    sys.stdout.write(chr(i))
                    sys.stdout.flush()
            else:
                sym_ascii = [a for a in range(32, 64+1)]+[b for b in range(91, 96+1)]+[c for c in range(123, 126+1)]
                i = ini = [a for a in range(len(sym_ascii)) if sym_ascii[a]>ord(s)][0] if s!='~' else 0
                while True:
                    time.sleep(0.03)
                    sys.stdout.write('\b') if i!=ini else sys.stdout.write('')
                    sys.stdout.flush()
                    sys.stdout.write(chr(sym_ascii[i]))
                    sys.stdout.flush()
                    if i==(len(sym_ascii)-1):
                        i = -1
                    if chr(sym_ascii[i])==s:
                        break
                    i+=1

        for i in range(end):
            sys.stdout.write('-')
            sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write('\b'*(start+len(str(string))+end))
        sys.stdout.flush()


def threadstart(string):
    global thread, stop_thread
    stop_thread = False
    thread = threading.Thread(target=TextPrinter, args=(string, ))
    thread.start()

def threadquit():
    global thread, stop_thread
    stop_thread = True
    thread.join()

def main():
    global thread
    threadstart('Please Wait_.')
    time.sleep(30)
    threadquit()

if __name__=='__main__':
    main()
```
### 5/5 [WriterFunction.py](https://github.com/Bhargav43/MagPi-Fetch/blob/master/Scripts/WriterFunction.py)
```python
import requests
import sys, os
from TextPrinter import threadstart, threadquit

global_selectionlist = dict()

def writePDF(name, url, loc):
    global global_selectionlist
    if global_selectionlist[name]:
        threadstart('Writing '+name)
        reqObj = requests.get(url, stream=True)
        with open(os.path.join(loc, name), 'wb') as f:
            f.write(reqObj.content)
        threadquit()
```

### [Sample Output](https://github.com/Bhargav43/MagPi-Fetch/blob/master/Sample/Sample%20Output.txt) :bar_chart:
```
Microsoft Windows [Version 10.0.17134.1425]
(c) 2018 Microsoft Corporation. All rights reserved.

H:\Projects\Python Related Stuff\Pyzo Projects\MagPi-Fetch\dist>MagPi-Fetch.exe

Kindly Understand, The Purpose of The Program is to Automate The Process of Downloading MagPi PDFs But The Download Speed Can Nowhere be Near the General Browser's Level.

---------------Please Wait--------------
List of 118 Raspberry Pi Magz on Site Are as Follows:
Sno.    Alias No.       Name
1       -118    MagPi92.pdf
2       -117    MagPi91.pdf
3       -116    MagPi90.pdf
4       -115    MagPi89.pdf
5       -114    MagPi88.pdf
6       -113    MagPi87.pdf
7       -112    MagPi86.pdf
8       -111    MagPi85.pdf
9       -110    MagPi84.pdf
10      -109    MagPi83.pdf
11      -108    MagPi82.pdf
12      -107    MagPi81.pdf
13      -106    MagPi80.pdf
14      -105    MagPi79.pdf
15      -104    MagPi78.pdf
16      -103    MagPi77.pdf
17      -102    MagPi76.pdf
18      -101    MagPi75.pdf
19      -100    MagPi74.pdf
20      -99     MagPi73.pdf
21      -98     MagPi72.pdf
22      -97     MagPi71.pdf
23      -96     MagPi70.pdf
24      -95     MagPi69.pdf
25      -94     MagPi68.pdf
26      -93     MagPi67.pdf
27      -92     MagPi66.pdf
28      -91     MagPi65.pdf
29      -90     MagPi64.pdf
30      -89     MagPi63.pdf
31      -88     MagPi62.pdf
32      -87     MagPi61.pdf
33      -86     MagPi60.pdf
34      -85     MagPi59.pdf
35      -84     MagPi58.pdf
36      -83     MagPi57.pdf
37      -82     MagPi56.pdf
38      -81     MagPi55.pdf
39      -80     MagPi54.pdf
40      -79     MagPi53.pdf
41      -78     MagPi52.pdf
42      -77     MagPi51.pdf
43      -76     MagPi50.pdf
44      -75     MagPi49.pdf
45      -74     MagPi48.pdf
46      -73     MagPi47.pdf
47      -72     MagPi46.pdf
48      -71     MagPi45.pdf
49      -70     MagPi44.pdf
50      -69     MagPi43.pdf
51      -68     MagPi42.pdf
52      -67     MagPi41.pdf
53      -66     MagPi40.pdf
54      -65     MagPi39.pdf
55      -64     MagPi38.pdf
56      -63     MagPi37.pdf
57      -62     MagPi36.pdf
58      -61     MagPi35.pdf
59      -60     MagPi34.pdf
60      -59     MagPi33.pdf
61      -58     MagPi32.pdf
62      -57     MagPi31.pdf
63      -56     MagPi30.pdf
64      -55     MagPi29.pdf
65      -54     MagPi28.pdf
66      -53     MagPi27.pdf
67      -52     MagPi26.pdf
68      -51     MagPi25.pdf
69      -50     MagPi24.pdf
70      -49     MagPi23.pdf
71      -48     MagPi22.pdf
72      -47     MagPi21.pdf
73      -46     MagPi20.pdf
74      -45     MagPi19.pdf
75      -44     MagPi18.pdf
76      -43     MagPi17.pdf
77      -42     MagPi16.pdf
78      -41     MagPi15.pdf
79      -40     MagPi14.pdf
80      -39     MagPi13.pdf
81      -38     MagPi12.pdf
82      -37     MagPi11.pdf
83      -36     MagPi10.pdf
84      -35     MagPi09.pdf
85      -34     MagPi08.pdf
86      -33     MagPi07.pdf
87      -32     MagPi06.pdf
88      -31     MagPi05.pdf
89      -30     MagPi04.pdf
90      -29     MagPi03.pdf
91      -28     MagPi02.pdf
92      -27     MagPi01.pdf
93      -26     Pi-Projects5.pdf
94      -25     Retro_Gaming.pdf
95      -24     000_GetStartedRPi_DIGITAL.pdf
96      -23     000_RPi_BeginnersGuide_DIGITAL.pdf
97      -22     Beginners_Guide_v2.pdf
98      -21     C_GUI_Programming.pdf
99      -20     Essentials_Bash_v2.pdf
100     -19     CC_Book_of_Scratch_v1.pdf
101     -18     Beginners_Guide_v1.pdf
102     -17     Projects_Book_v4.pdf
103     -16     Annual2018.pdf
104     -15     Beginners_Book_v1.pdf
105     -14     Projects_Book_v3.pdf
106     -13     Essentials_AIY_Projects_Voice_v1.pdf
107     -12     Essentials_Camera_v1.pdf
108     -11     Projects_Book_v2.pdf
109     -10     Essentials_C_v1.pdf
110     -9      Essentials_GPIOZero_v1.pdf
111     -8      Essentials_Minecraft_v1.pdf
112     -7      Essentials_Scratch_v1.pdf
113     -6      Essentials_Sonic_Pi-v1.pdf
114     -5      Essentials_SenseHAT_v1.pdf
115     -4      Essentials_Games_v1.pdf
116     -3      Projects_Book_v1.pdf
117     -2      Essentials_Bash_v1.pdf
118     -1      MagPiSE1.pdf

Please Enter the Location to Download the Files.
Example:        C:\Users\Bhargav\Downloads
Your Input:     H:\MagPi

Now, Please Select The Type of Download You Want.
1. Download One
2. Selective Download
3. Download All
4. Missing and Incomplete

Enter 1, 2, 3 or 4:     4

The Comparing Could Take a While As It Checks the Local with Network.
------------Please be Patient-----------
Incomplete Downloads:
Essentials_Bash_v1.pdf

Missing Downloads:
Essentials_AIY_Projects_Voice_v1.pdf


-----Writing Essentials_Bash_v1.pdf-----Voice_v1.pdf--------
Files Have Been Successfully Downloaded to H:\MagPi
Press Any Key to Exit.

H:\Projects\Python Related Stuff\Pyzo Projects\MagPi-Fetch\dist>
```

### [Executable File](https://github.com/Bhargav43/MagPi-Fetch/blob/master/MagPi-Fetch.exe) :floppy_disk:
_[Executable](https://github.com/Bhargav43/MagPi-Fetch/blob/master/MagPi-Fetch.exe) (also called freezed file) for using in change of confguration of base system or in absence of python. The file be used for distribution with ease and without dependencies. Following is the commands I used for the same. [Click here](https://github.com/Bhargav43/MagPi-Fetch/blob/master/Freezing%20Logs.txt) for freezing logs._

#### Creating Specifications file :page_facing_up:
```
pyi-makespec --onefile --hidden-import=requests --hidden-import=requests_html --hidden-import=bs4 --hidden-import=re --hidden-import=os --hidden-import=time --hidden-import=sys --hidden-import=TextPrinter --hidden-import=ScrapperFunctions --hidden-import=SelectorFunctions --hidden-import=WriterFunction --hidden-import=pkg_resources.py2_warn --icon=".\Includes\RaspberryPiIcon.ico" --specpath="H:\Projects\Python Related Stuff\Pyzo Projects\MagPi-Fetch" ".\Scripts\MagPi-Fetch.py"
```

This creates the following [MagPi-Fetch.spec](https://github.com/Bhargav43/MagPi-Fetch/blob/master/MagPi-Fetch.spec) as follows,
```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Scripts\\MagPi-Fetch.py'],
             pathex=['H:\\Projects\\Python Related Stuff\\Pyzo Projects\\MagPi-Fetch'],
             binaries=[],
             datas=[],
             hiddenimports=['requests', 'requests_html', 'bs4', 're', 'os', 'time', 'sys', 'TextPrinter', 'ScrapperFunctions', 'SelectorFunctions', 'WriterFunction', 'pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MagPi-Fetch',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Includes\\RaspberryPiIcon.ico')
```

#### Creating Executable :arrow_forward:

PyPI `Pyinstaller 3.6` was used for creating the executable in PIP environment. Command as follows,
```
pyinstaller --onefile --hidden-import=requests --hidden-import=requests_html --hidden-import=bs4 --hidden-import=re --hidden-import=os --hidden-import=time --hidden-import=sys --hidden-import=TextPrinter --hidden-import=ScrapperFunctions --hidden-import=SelectorFunctions --hidden-import=WriterFunction --hidden-import=pkg_resources.py2_warn --icon=".\Includes\RaspberryPiIcon.ico" --specpath="H:\Projects\Python Related Stuff\Pyzo Projects\MagPi-Fetch" ".\Scripts\MagPi-Fetch.py"
```

### Finally, the Working Model :metal:

Click for accessing [MagPi-Fetch](https://github.com/Bhargav43/MagPi-Fetch)

# Farewell! :tada::tada:
