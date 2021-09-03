#!/usr/bin/python
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventCreateScrollWheelEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

import time

def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(
                    None, 
                    type, 
                    (posx,posy), 
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy)

def mousescroll(dx, dy):
        theEvent = CGEventCreateScrollWheelEvent(
                None, 
                type, 
                (dx,dy), 
                kCGMouseButtonLeft)
        pass

def mouseclick(posx,posy):
        # uncomment this line if you want to force the mouse 
        # to MOVE to the click location first (I found it was not necessary).
        mouseEvent(kCGEventMouseMoved, posx,posy)
        mouseEvent(kCGEventLeftMouseDown, posx,posy)
        mouseEvent(kCGEventLeftMouseUp, posx,posy)

if __name__ == "__main__":
        #mousemove(2087 ,1230)
        mouseclick(2087 ,1230)
        time.sleep(0.2)
        mouseclick(2087 ,1230)
        time.sleep(0.2)
        mouseclick(2437, 940)
