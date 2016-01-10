import os
import curses
import textwrap
import random

import AppCommon



COLOR_MENU = None
COLOR_BODY = None
COLOR_BLOCKTEXT = None

SCREEN_CURRENT = None

OBJ_TOPBAR = None
OBJ_BOTTOMBAR = None

def renderTopBar(stdscr):
    global OBJ_TOPBAR
    
    height, width = stdscr.getmaxyx()
    
    authorTag = "(C) 2016 Archaic Software Associates"
    
    OBJ_TOPBAR = curses.newwin(1, width, 0, 0)
    OBJ_TOPBAR.bkgd(1, curses.color_pair(2))
    OBJ_TOPBAR.addstr(0, max(len(authorTag), width) - len(authorTag) - 1, authorTag[:width - 2], AppCommon.COLOR_MENU)
    OBJ_TOPBAR.addstr(0, 1, "SMH.com.au Terminal Access   ", AppCommon.COLOR_MENU)
    
    OBJ_TOPBAR.refresh()


def renderBottomBar(stdscr, extraText = None):
    global OBJ_BOTTOMBAR
    global SCREEN_CURRENT
    global COLOR_MENU
    
    height, width = stdscr.getmaxyx()
    
    OBJ_BOTTOMBAR = curses.newwin(1, width, height - 1, 0)
    OBJ_BOTTOMBAR.bkgd(1, curses.color_pair(2))
    
    if SCREEN_CURRENT == "content":
        OBJ_BOTTOMBAR.addstr(0, 1, "Q = Quit; R = Return", COLOR_MENU)
    else:
        OBJ_BOTTOMBAR.addstr(0, 1, "Q = Quit", COLOR_MENU)
    
    if extraText is not None:
        OBJ_BOTTOMBAR.addstr(0, width - len(extraText) - 1, extraText[:width - 2], COLOR_MENU)
    
    OBJ_BOTTOMBAR.refresh()

