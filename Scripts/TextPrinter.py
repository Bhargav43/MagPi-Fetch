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
