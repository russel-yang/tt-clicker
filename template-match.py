import cv2
import numpy as np

haystack = cv2.imread("screenshot2021-0730_19-10-44-124337.png", cv2.IMREAD_UNCHANGED)

grayhs = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
needle = cv2.imread("assets/needles/settings.png", cv2.IMREAD_GRAYSCALE)

result = cv2.matchTemplate(grayhs, needle, cv2.TM_CCOEFF_NORMED, 0.9)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

cv2.circle(haystack, max_loc, 30, (0,0, 255), -1)

cv2.imshow('result', haystack)
cv2.waitKey(0)
print(max_loc)
