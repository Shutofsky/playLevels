# Clear the screen and hold it for 3 seconds
import curses
import random
import time
import string
import threading

playParams = dict()
playParams['leftSafe'] = 25
playParams['rightSafe'] = 35
playParams['left'] = 5
playParams['right'] = 50

start_time = time.time()


def millis():
    return (time.time() - start_time) * 1000.0

def initCurses():
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, 10, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, 10)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.noecho()
    curses.noraw()
    curses.curs_set(0)

def startPlayLevels():
    global playParams
    naprs = [1, -1]
    servWin = curses.newwin(3, 80, 0, 0)
    mainWin = curses.newwin(14, 80, 3, 0)
    auxWin = curses.newwin(7, 80, 19, 0)
    servWin.clear()
    servWin.nodelay(True)
    mainWin.clear()
    mainWin.nodelay(True)
    auxWin.clear()
    auxWin.nodelay(True)
    servWin.addstr(0, 10, "Останавливайте значение уровня сигнала с", curses.color_pair(1))
    servWin.addstr(1, 10, "помощью клавиши <ПРОБЕЛ> в безопасной зоне", curses.color_pair(1))
    servWin.addstr(2, 0, "=" * 79, curses.color_pair(1))
    servWin.refresh()
    for i in range(0,3):
        mainWin.addch(i, playParams['leftSafe'], "|", curses.color_pair(3))
        mainWin.addch(i, playParams['rightSafe'], "|", curses.color_pair(4))
        mainWin.addch(i+11, playParams['leftSafe'], "|", curses.color_pair(3))
        mainWin.addch(i+11, playParams['rightSafe'], "|", curses.color_pair(4))
    for i in range(4,12,2):
        mainWin.addch(i, playParams['leftSafe'], "|", curses.color_pair(3))
        mainWin.addch(i, playParams['rightSafe'], "|", curses.color_pair(4))
    mainWin.addstr(13, 0, "=" * 79, curses.color_pair(1))
    mainWin.refresh()
    auxWin.addstr(0, 10, "Каждая ошибка может существенно сократить", curses.color_pair(1))
    auxWin.addstr(1, 10, "Вашу жизнь!!!", curses.color_pair(1))
    auxWin.refresh()

    levelStrings=[{"x_len":0, "xNapr":0, "y":3, "timer":0, "cTime":0},
                  {"x_len":0, "xNapr":0, "y":5, "timer":0, "cTime":0},
                  {"x_len":0, "xNapr":0, "y":7, "timer":0, "cTime":0},
                  {"x_len":0, "xNapr":0, "y":9, "timer":0, "cTime":0}]
    cTime = millis()
    for i in range(0,4):
        levelStrings[i]['timer'] = random.uniform(0, 50)
        levelStrings[i]['cTime'] = cTime
        mainWin.addstr(3+i*2, playParams['left']-1, "[==", curses.color_pair(1))
    mainWin.refresh()
    countOff = 0
    while True:
        cTime = millis()
        for i in range(countOff,4):
            if ((cTime - levelStrings[i]['cTime'])>=levelStrings[i]['timer']):
                levelStrings[i]['x_len'] = levelStrings[i]['x_len'] + naprs[levelStrings[i]['xNapr']]
                if ((levelStrings[i]['x_len'] < 0) or 
                    (levelStrings[i]['x_len'] > (playParams['right']-playParams['left']))):
                    levelStrings[i]['xNapr'] = (levelStrings[i]['xNapr'] + 1) % 2
                mainWin.addstr(levelStrings[i]['y'], levelStrings[i]['x_len']+playParams['left']+1,
                               "=] ", curses.color_pair(1))
                levelStrings[i]['cTime'] = cTime
                mainWin.refresh()

        if mainWin.getch()==ord(' '):
            if (((levelStrings[countOff]['x_len']+playParams['left']+2) >= playParams['leftSafe']) and 
                ((levelStrings[countOff]['x_len']+playParams['left']+2) <= playParams['rightSafe'])):
                countOff = countOff + 1
                if(countOff>=4):
                    print("Win")
                    quit()
            else:
                print("Lose")
                quit()
 

        
        

 


def startTerminal():
    global db_parameters
    global db_updated
    global forceClose
    global prtSnd
    global wrdSnd
    initCurses()
    startPlayLevels()
    
if __name__ == "__main__":
    startTerminal()
