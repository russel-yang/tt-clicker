import pyautogui
import time
from PIL import ImageGrab
import cv2
import numpy as np
import mss
import constants
from vision import Vision
from pynput.mouse import  Controller

mouse = Controller()

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

def upgradeHeros():
    print(left + 150, top + 1050)
    pyautogui.doubleClick(left + 150, top + 1050)
    time.sleep(0.2)
    print(left + 500, top + 780)
    pyautogui.click(left + 500, top + 780)
    time.sleep(1)
    # click first upgrade
    # for i in range(0, 5):
    #     pyautogui.click(left + 500, top + 800)
    #     pyautogui.click(left + 500, top + 890)
    # mouse.scroll(0, 2)
    # time.sleep(0.1)
    # mouse.scroll(0, 8)
    #mouse.scroll(0,100)
    #pyautogui.doubleClick()
    # for i in range(0, 20):
    #     pyautogui.vscroll(1)
    # pyautogui.doubleClick(left + 150, top + 1050)
    # pyautogui.hscroll(500)
    # pyautogui.hscroll(600)
    # pyautogui.scroll(700)


with mss.mss() as sct:
    last_time = time.time()
    monitor = {"top": top, "left": left, "width": constants.GAME_WINDOW_WIDTH, "height": constants.GAME_WINDOW_HEIGHT}
    vision = Vision(top, left, coff)


    tt2 = sct.grab(monitor)
    game = np.array(tt2)
    game = cv2.cvtColor(game, cv2.COLOR_RGBA2GRAY)


    # result = vision.find_fairy(game)
    # if (result != None):
    #     pyautogui.click(result[0], result[1])   
    # result = vision.find_company(game)
    # if (result != None):
    #     pyautogui.click(result[0], result[1])   
    # result = vision.find_skill(game)
    # if (result != None):
    #     pyautogui.click(result[0], result[1])  
    # result = vision.upgrade_heros(game)
    # if (result != None):
    #     print(result)
    #     pyautogui.click(result[0], result[1])   
    # 
    
    cv2.imshow('screen', game)
    #print('fps ={}'.format(1/(time.time()-last_time)))
    last_time = time.time()

    #upgradeHeros() 


    # # thunder shop
    # pyautogui.click(left + 307, top + 405)
    # # daggers
    # pyautogui.click(left + 258, top + 470)
    # pyautogui.click(left + 302, top + 492)
    # pyautogui.click(left + 350, top + 470)

    key = cv2.waitKey(0) & 0xFF
    cv2.imwrite("temp/{}.png".format(time.time()), game)





