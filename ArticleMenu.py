import os
import curses
import textwrap

import Content_SMH
import AppCommon


OBJ_ARTICLEMENU = None
OBJ_ARTICLEMENU_SCROLL = None
OBJ_ARTICLEMENU_SCROLL_POSITION = 0
OBJ_ARTICLEMENU_SCROLL_ITEMS =  []


def renderArticleMenu(stdscr):
    
    global OBJ_ARTICLEMENU
    
    height, width = stdscr.getmaxyx()
    
    OBJ_ARTICLEMENU = curses.newwin(height - 2, width, 1, 0)
    OBJ_ARTICLEMENU.border(0)
    OBJ_ARTICLEMENU.bkgd(1, AppCommon.COLOR_BODY)
    OBJ_ARTICLEMENU.addstr(1, 5, "Select an article to read:", AppCommon.COLOR_BODY)
    OBJ_ARTICLEMENU.refresh()
    
    renderArticleMenuScroll(stdscr, None)
    
    AppCommon.SCREEN_CURRENT = "articlemenu"
    

def renderArticleMenuScroll(stdscr, direction):
    
    global OBJ_ARTICLEMENU
    global OBJ_ARTICLEMENU_SCROLL
    global OBJ_ARTICLEMENU_SCROLL_POSITION
    global OBJ_ARTICLEMENU_SCROLL_ITEMS
    
    height, width = stdscr.getmaxyx()
    
    scrollPadStartPositionY = 4
    scrollPadVisibleHeight = height - 5
    scrollPadVisibleWidth = width - 10
    scrollPadVisibleLines = scrollPadVisibleHeight - scrollPadStartPositionY
    
    if direction == "up":
        OBJ_ARTICLEMENU_SCROLL_POSITION -= 1
        
        if OBJ_ARTICLEMENU_SCROLL_POSITION < 0:
            OBJ_ARTICLEMENU_SCROLL_POSITION = 0
        
    elif direction == "down":
        OBJ_ARTICLEMENU_SCROLL_POSITION += 1
        
        if OBJ_ARTICLEMENU_SCROLL_POSITION >= len(OBJ_ARTICLEMENU_SCROLL_ITEMS):
            OBJ_ARTICLEMENU_SCROLL_POSITION = len(OBJ_ARTICLEMENU_SCROLL_ITEMS) - 1
    
    
    
    # Setup the scrollbar
    OBJ_ARTICLEMENU_SCROLL = curses.newpad(len(OBJ_ARTICLEMENU_SCROLL_ITEMS) + 1, 1000)
    
    i = 0
    for x in OBJ_ARTICLEMENU_SCROLL_ITEMS:
        
        if i == OBJ_ARTICLEMENU_SCROLL_POSITION:
            # Highlight the currently selected item with an arrow
            text = "-> " + x['title']
        else:
            text = "   " + x['title']
        
        OBJ_ARTICLEMENU_SCROLL.addstr(i, 1, text)
        i += 1
    
    if OBJ_ARTICLEMENU_SCROLL_POSITION > len(OBJ_ARTICLEMENU_SCROLL_ITEMS) - scrollPadVisibleLines:
        lastLineIsVisible = True
    else:
        lastLineIsVisible = False
    
    if not lastLineIsVisible:
        # Scroll
        OBJ_ARTICLEMENU_SCROLL.refresh(OBJ_ARTICLEMENU_SCROLL_POSITION, 0, scrollPadStartPositionY, 5, scrollPadVisibleHeight, scrollPadVisibleWidth)
    else:
        # Don't scroll anymore - just move the arrow down the page
        OBJ_ARTICLEMENU_SCROLL.refresh(len(OBJ_ARTICLEMENU_SCROLL_ITEMS) - scrollPadVisibleLines, 0, 4, 5, scrollPadVisibleHeight, scrollPadVisibleWidth)
