from PIL.Image import NONE
import cv2
import time
import pyautogui
import random
import mss
import constants
import numpy as np

class Vision:
    def __init__(self, top, left, coff) -> None:
        self.top = top
        self.left = left
        self.coff = coff
        self.ts_last_hero_upgrade = time.time()
        self.ts_last_dialog_check = time.time()
        self.hero_menu_open = False
        self.skills_bought = False
        self.skills = ["assets/needles/skills/warcry.png", "assets/needles/skills/shadowclone.png", "assets/needles/skills/deadlystrike.png", "assets/needles/skills/thundership.png"]

    def find_template(self, game, template, confidence = 0.6, start = 0, end=None):
        if (end == None):
            end = len(game)
        mt_result = cv2.matchTemplate(game[start:end], template, cv2.TM_CCOEFF_NORMED)
        
        w, h = template.shape[::-1]
        #loc = np.where( mt_result >= confidence)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mt_result)
        #print(max_val, max_val)

        return (self.left + max_loc[0] / self.coff + w / self.coff / 2, self.top + start / self.coff + max_loc[1] / self.coff +  h / self.coff / 2) if max_val > confidence else None

    def find_company(self, game):
        clan_mate = cv2.imread("assets/needles/company.png", cv2.IMREAD_GRAYSCALE)
        start, end = 860, 1230
        pos = self.find_template(game, clan_mate, 0.6, start, end)
        return pos

    def find_skill(self,game):
        num = random.randrange(3)
        skill = cv2.imread(self.skills[num], cv2.IMREAD_GRAYSCALE)
        start, end = 1800, 2036
        pos = self.find_template(game, skill, 0.8, start, end)
        return pos

    def find_fairy(self,game):
        fairy = cv2.imread("assets/needles/fairy.png", cv2.IMREAD_GRAYSCALE)
        start, end = 200, 900
        pos = self.find_template(game, fairy, 0.7, start, end)
        return pos if pos != None and pos[0] - self.left > 150 else None

    def fire_thunder_ship(self, game):
        thunder = cv2.imread("assets/needles/skills/fire_thunder_ship.png", cv2.IMREAD_GRAYSCALE)
        pos = self.find_template(game, thunder, 0.5)
        return pos

    def upgrade_heros(self):
        if (time.time() - self.ts_last_hero_upgrade) < 10:
            return
        pyautogui.doubleClick(self.left + 150, self.top + 1030)
        for i in range(0, 5):
            pyautogui.doubleClick(self.left + 500, self.top + 757)
        for i in range(0, 5):
            pyautogui.doubleClick(self.left + 500, self.top + 853)
        for i in range(0, 5):
            pyautogui.doubleClick(self.left + 500, self.top + 950)

        time.sleep(0.1)
        pyautogui.vscroll(1)
        time.sleep(0.1)
        # close the window
        pyautogui.doubleClick(self.left + 150, self.top + 1030)

        self.ts_last_hero_upgrade = time.time()
    
    def take_shot(self):
        with mss.mss() as sct:
            monitor = {"top": self.top, "left": self.left, "width": constants.GAME_WINDOW_WIDTH, "height": constants.GAME_WINDOW_HEIGHT}
            return cv2.cvtColor(np.array(sct.grab(monitor)),cv2.COLOR_RGBA2GRAY) 

    def make_menu_fullscreen(self):
        shot = self.take_shot()
        # toggle full screen menu
        half_screen = cv2.imread("assets/needles/menu/half-screen.png", cv2.IMREAD_GRAYSCALE)
        pos = self.find_template(shot, half_screen, 0.9)
        if pos != None:
            pyautogui.click(pos[0], pos[1])
            time.sleep(0.3)

    def extra_clicks(self):
        # thunder shop
        pyautogui.click(self.left + 307, self.top + 405)
        # daggers
        pyautogui.click(self.left + 258, self.top + 470)
        pyautogui.click(self.left + 302, self.top + 492)
        pyautogui.click(self.left + 350, self.top + 470)
        # company extra click
        pyautogui.click(self.left+218, self.top + 540)

    def find_prestige(self):
        # click the menu
        pyautogui.click(self.left + 40, self.top + 1044, 2)
        time.sleep(0.3)
        shot = self.take_shot()

        # toggle full screen menu
        self.make_menu_fullscreen()

        prestige = cv2.imread("assets/needles/buy-skills/prestige.png", cv2.IMREAD_GRAYSCALE)
        start, end = 515, 715
        pos = self.find_template(shot, prestige, 0.95, start, end)
        while (pos == None):
            pyautogui.vscroll(1)
            time.sleep(1)
            shot = self.take_shot()
            pos = self.find_template(shot, prestige, 0.9)
        return pos

    def prestige(self):
        pos = self.find_prestige()
        pyautogui.click(pos[0] + 450, pos[1])
        time.sleep(0.3)
        
        shot = self.take_shot()
        first = cv2.imread("assets/needles/prestige/first.png", cv2.IMREAD_GRAYSCALE)
        pos = self.find_template(shot, first, 0.9)
        if (pos != None):
            pyautogui.click(pos[0], pos[1])
            time.sleep(0.3)
        #click the position directly
        pyautogui.click(self.left + 410, self.top + 800)
        time.sleep(20)

    def buy_skills(self, clicks):
        if self.skills_bought:
            return
        pos = self.find_prestige()
        if (pos != None):
            for y in [180, 508, 600, 690, 780, 880, 980]:
                pyautogui.click(self.left + 500, self.top + y, clicks, 0.1)
        # click the menu
        pyautogui.click(self.left + 40, self.top + 1044, 1)
        self.skills_bought = True

    def dismiss_dialog(self, game):
        if (time.time()- self.ts_last_dialog_check < 60):
            return False
        cancel = cv2.imread("assets/needles/buttons/cancel.png", cv2.IMREAD_GRAYSCALE)
        pos = self.find_template(game, cancel, 0.8)
        self.ts_last_dialog_check  = time.time()
        if (pos != None):
            pyautogui.click(pos[0], pos[1])
            return True
        return False
    
    def enchant_artifect(self):
        # find enchantmet
        shot = self.take_shot()
        enchant = cv2.imread("assets/needles/buttons/enchant.png", cv2.IMREAD_GRAYSCALE)
        pos = self.find_template(shot, enchant, 0.9)
        if (pos != None):
            pyautogui.click(pos[0], pos[1])
            time.sleep(0.3)
            shot = self.take_shot()
            perform_enchant = cv2.imread("assets/needles/buttons/perform-enchant.png", cv2.IMREAD_GRAYSCALE)
            pos = self.find_template(shot, perform_enchant, 0.8)
            if (pos != None):
                pyautogui.click(pos[0], pos[1])
                pyautogui.sleep(1)
                pyautogui.click(pos[0], pos[1], 2, 0.2)

    def buy_artifects(self):
        pyautogui.click(self.left + 450, self.top + 1050,2)
        time.sleep(0.4)
        self.make_menu_fullscreen()

        # reset to top by book of shadow
        bos = cv2.imread("assets/needles/artifacts/bos.png", cv2.IMREAD_GRAYSCALE)
        shot = self.take_shot()
        start, end = 520, 720
        pos = self.find_template(shot, bos, 0.9, start, end)
        while (pos == None):
            pyautogui.vscroll(1)
            time.sleep(0.5)
            shot = self.take_shot()
            pos = self.find_template(shot, bos, 0.9, start, end)

        #click in the menu
        pyautogui.click(self.left + 285, self.top + 100)
        time.sleep(0.2)
        self.enchant_artifect()

        for x in range(0,8):
            pyautogui.click(self.left + 500, self.top + 300 + x * 100, 1, 0.2)

        # close the menu
        pyautogui.click(self.left + 450, self.top + 1050,1)
        
        # for _ in range(0,1):
        #     pyautogui.vscroll(-1)
        #     time.sleep(0.5)
        

    def play(game):
        pass