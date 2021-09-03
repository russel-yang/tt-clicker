import cv2
import time
import pyautogui
import random

class Vision:
    def __init__(self, top, left, coff) -> None:
        self.top = top
        self.left = left
        self.coff = coff
        self.ts_last_hero_upgrade = time.time()
        self.hero_menu_open = False
        self.skills = ["assets/needles/skills/warcry.png", "assets/needles/skills/shadowclone.png", "assets/needles/skills/deadlystrike.png", "assets/needles/skills/thundership.png"]

    def find_template(self, game, template, confidence = 0.6, start = 0, end=None):
        if (end == None):
            end = len(game)
        mt_result = cv2.matchTemplate(game[start:end], template, cv2.TM_CCOEFF_NORMED)
        
        w, h = template.shape[::-1]
        #loc = np.where( mt_result >= confidence)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mt_result)

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


    def play(game):
        pass