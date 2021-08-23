import pyautogui
import time
from PIL import ImageGrab
import cv2
import numpy as np
import mss

with mss.mss() as sct:
    full_screen = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
    fs_gray = cv2.cvtColor(full_screen, cv2.COLOR_BGR2GRAY)
    gear = cv2.imread("assets/needles/settings.png", cv2.IMREAD_GRAYSCALE)
    mt_result = cv2.matchTemplate(fs_gray, gear, cv2.TM_CCOEFF_NORMED, 0.9)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mt_result)

    x, y = max_loc
    last_time = time.time()
    monitor = {"top": int(y/2), "left": int(x/2), "width": 600, "height": 1075}

    while True:
        tt2 = sct.grab(monitor)
        game = np.array(tt2)

        cv2.imshow('screen', game)
        #print('fps ={}'.format(1/(time.time()-last_time)))
        last_time = time.time()
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


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

