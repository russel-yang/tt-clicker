import pyautogui
import time

# pyautogui.moveTo(1286, 647, 0.5)
# pyautogui.click()
# # pyautogui.typewrite('space')

# pyautogui.moveTo(0,0, 0.5)
def upgradeHeros():
    heroLevelUpLocations = pyautogui.locateCenterOnScreen('assets/needles/heroUpgradable.png', confidence=0.8)
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
upgradeHeros()

