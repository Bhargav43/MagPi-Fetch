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
