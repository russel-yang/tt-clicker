import pyautogui
import time
from PIL import ImageGrab
import cv2
import numpy as np
import mss
import pytesseract
import constants

def findGameWindowPos():
    with mss.mss() as sct:
        full_screen = np.array(sct.grab({"top": 0, "left": 0, "width": 2560, "height": 1440}))
        fs_gray = cv2.cvtColor(full_screen, cv2.COLOR_BGR2GRAY)
        gear = cv2.imread("assets/needles/settings.png", cv2.IMREAD_GRAYSCALE)
        mt_result = cv2.matchTemplate(fs_gray, gear, cv2.TM_CCOEFF_NORMED, 0.9)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mt_result)

        x, y = max_loc
        left = x / 2
        top = y / 2
    return (top, left)

(top, left) = findGameWindowPos()

def find_company(game):
    clan_mate = cv2.imread("assets/needles/company.png", cv2.IMREAD_GRAYSCALE)
    mt_result = cv2.matchTemplate(game, clan_mate, cv2.TM_CCOEFF_NORMED)
    
    w, h = clan_mate.shape[::-1]
    loc = np.where( mt_result >= 0.6)
    clicked = False
    for pt in zip(*loc[::-1]):
        # click the game window
        if (clicked != True):
            pyautogui.click(left + pt[0] / 2  + w / 4, top + pt[1] / 2 +  h / 4)
            clicked = True
            break

def find_skill(game):
    skill = cv2.imread("assets/needles/skills/warcry.png", cv2.IMREAD_GRAYSCALE)
    mt_result = cv2.matchTemplate(game, skill, cv2.TM_CCOEFF_NORMED)
    
    w, h = skill.shape[::-1]
    loc = np.where( mt_result >= 0.9)
    clicked = False
    for pt in zip(*loc[::-1]):
        # click the game window
        if (clicked != True):
            pyautogui.click(left + pt[0] / 2  + w / 4, top + pt[1] / 2 +  h / 4 )
            print("found:", pt)
            clicked = True
            break

def find_fairy(game):
    clan_mate = cv2.imread("assets/needles/fairy.png", cv2.IMREAD_GRAYSCALE)
    mt_result = cv2.matchTemplate(game, clan_mate, cv2.TM_CCOEFF_NORMED)
    
    w, h = clan_mate.shape[::-1]
    loc = np.where( mt_result >= 0.8)
    clicked = False
    for pt in zip(*loc[::-1]):
        #click the game window
        if (clicked != True):
            print("find and click")
            pyautogui.click(left + pt[0] / 2  + w / 4, top + pt[1] / 2 +  h / 4)
            clicked = True
            break

with mss.mss() as sct:
    last_time = time.time()
    monitor = {"top": top, "left": left, "width": constants.GAME_WINDOW_WIDTH, "height": constants.GAME_WINDOW_HEIGHT}

    while True:
        tt2 = sct.grab(monitor)
        game = np.array(tt2)
        game = cv2.cvtColor(game, cv2.COLOR_RGBA2GRAY)

        #find_fairy(game)
        #find_company(game)
        find_skill(game)

        cv2.imshow('screen', game)
        print('fps ={}'.format(1/(time.time()-last_time)))
        last_time = time.time()

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

