import pyautogui
import time
from PIL import ImageGrab
import cv2
import numpy as np
import mss
import constants
from vision import Vision

abyssal = True

def findGameWindowPos():
    with mss.mss() as sct:
        full_screen = np.array(sct.grab({"top": 0, "left": 0, "width": 2560, "height": 1440}))
        coff = full_screen.shape[0] / 1440
        fs_gray = cv2.cvtColor(full_screen, cv2.COLOR_BGR2GRAY)
        if abyssal:
            gear = cv2.imread("assets/needles/abyssal.png", cv2.IMREAD_GRAYSCALE)
        else:
            gear = cv2.imread("assets/needles/settings.png", cv2.IMREAD_GRAYSCALE)
        mt_result = cv2.matchTemplate(fs_gray, gear, cv2.TM_CCOEFF_NORMED)
        max_loc = cv2.minMaxLoc(mt_result)[3]

        x, y = max_loc
        left = x / coff
        top = y / coff
    return (top - 98, left - 20, coff) if abyssal else (top , left, coff) 

(top, left, coff) = findGameWindowPos()

def progress(game): 
    poi = game[100:140, 500:700]
    return poi


with mss.mss() as sct:
    last_time = time.time()
    monitor = {"top": top, "left": left, "width": constants.GAME_WINDOW_WIDTH, "height": constants.GAME_WINDOW_HEIGHT}
    vision = Vision(top, left, coff)

    while True:
        tt2 = sct.grab(monitor)
        game = np.array(tt2)
        game = cv2.cvtColor(game, cv2.COLOR_RGBA2GRAY)

        result = vision.find_nothanks(game)
        if (result != None):
            pyautogui.click(result[0], result[1])
            continue   
        
        if (vision.dismiss_dialog(game)):
            continue

        result = vision.find_fairy(game)
        if (result != None):
            pyautogui.click(result[0], result[1])   
        result = vision.find_company(game)
        if (result != None):
            pyautogui.click(result[0], result[1])   
        result = vision.find_skill(game)
        if (result != None):
            pyautogui.click(result[0], result[1])  
 

        cv2.imshow('screen', game)
        #print('fps ={}'.format(1/(time.time()-last_time)))
        last_time = time.time()
        time.sleep(2)

        vision.extra_clicks()
        # upgrade heros
        #vision.upgrade_heros()

        key = cv2.waitKey(25) & 0xFF
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
        elif key == ord("s"):
            cv2.imwrite("temp/{}.png".format(time.time()), game)


# pyautogui.moveTo(1286, 647, 0.5)
# pyautogui.click()
# # pyautogui.typewrite('space')

# pyautogui.moveTo(0,0, 0.5)
def upgradeHeros():
    for x in range(0, 10, 1):
        heroLevelUpLocations = pyautogui.locateCenterOnScreen('assets/needles/heroUpgradable.png', confidence=0.8)
        if heroLevelUpLocations != None:
            print(heroLevelUpLocations)
            pyautogui.moveTo(heroLevelUpLocations.x/2, heroLevelUpLocations.y/2, 1)
            time.sleep(1)
            pyautogui.doubleClick()

#pyautogui.displayMousePosition()

def simpleBattle():
    pyautogui.moveTo(230,600, 1)
    pyautogui.doubleClick()
    time.sleep(1)
    pyautogui.click()
    pyautogui.press('w')
    time.sleep(2)
    pyautogui.press('e')
    time.sleep(2)
    pyautogui.press('r')
    time.sleep(2)
    pyautogui.press('t')
    time.sleep(2)
    pyautogui.press('y')
    pyautogui.press('space')

#simpleBattle()
#upgradeHeros()

