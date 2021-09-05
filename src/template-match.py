import cv2
import numpy as np

haystack = cv2.imread("temp/1630784169.3677819.png", cv2.IMREAD_UNCHANGED)
print(haystack.shape)

#grayhs = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
needle = cv2.imread("assets/needles/main-menu.png", cv2.IMREAD_GRAYSCALE)
print(needle.shape)

result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

cv2.circle(haystack, max_loc, 30, (0,0, 255), -1)

cv2.imshow('result', haystack)
cv2.waitKey(0)
print(max_loc, max_val)
