import os
import curses
import textwrap

import Content_SMH
import AppCommon
import ArticleMenu


OBJ_CONTENTSCREEN = None
OBJ_CONTENTSCREEN_SCROLL = None
OBJ_CONTENTSCREEN_SCROLL_POSITION = 0
OBJ_CONTENTSCREEN_SCROLL_TEXT = ""


def renderContentScreen(stdscr):
    
    global OBJ_CONTENTSCREEN
    global OBJ_CONTENTSCREEN_SCROLL_TEXT
    global OBJ_CONTENTSCREEN_SCROLL_POSITION
    
    OBJ_CONTENTSCREEN_SCROLL_POSITION = 0
    
    height, width = stdscr.getmaxyx()
    
    OBJ_CONTENTSCREEN = curses.newwin(height - 2, width, 1, 0)
    OBJ_CONTENTSCREEN.border(0)
    OBJ_CONTENTSCREEN.bkgd(1, AppCommon.COLOR_BODY)
    OBJ_CONTENTSCREEN.addstr(1, 5, "Article:", AppCommon.COLOR_BODY)
    OBJ_CONTENTSCREEN.addstr(6, 5, "Loading...", AppCommon.COLOR_BODY)
    OBJ_CONTENTSCREEN.refresh()
    
    # Fetch the article's content
    url = ArticleMenu.OBJ_ARTICLEMENU_SCROLL_ITEMS[ArticleMenu.OBJ_ARTICLEMENU_SCROLL_POSITION]['url']
    
    try:
        # Fetch the full content from the website
        content = Content_SMH.fetchArticleContent(url)
        
        OBJ_CONTENTSCREEN_SCROLL_TEXT = "\n" + ''.join([i if ord(i) < 128 else ' ' for i in content['title']]) + "\n"
        OBJ_CONTENTSCREEN_SCROLL_TEXT += ''.join([i if ord(i) < 128 else ' ' for i in content['date']]) + "\n"
        OBJ_CONTENTSCREEN_SCROLL_TEXT += ''.join([i if ord(i) < 128 else ' ' for i in content['author']]) + "\n\n\n"
        
        # Strip out non-ASCII characters for the body text
        OBJ_CONTENTSCREEN_SCROLL_TEXT += ''.join([i if ord(i) < 128 else ' ' for i in content['body']])
        
    except Exception, e:
        print e
        OBJ_CONTENTSCREEN_SCROLL_TEXT = "ERROR: Unable to fetch article :( \n\n" + str(e)
    
    OBJ_CONTENTSCREEN_SCROLL_TEXT += "\n\n" + url
    
    renderContentScreenScroll(stdscr)
    
    AppCommon.SCREEN_CURRENT = "content"

def renderContentScreenScroll(stdscr, direction = None):
    
    global OBJ_CONTENTSCREEN_SCROLL
    global OBJ_CONTENTSCREEN_SCROLL_POSITION
    global OBJ_CONTENTSCREEN_SCROLL_TEXT
    
    height, width = stdscr.getmaxyx()
    
    scrollPadStartPositionY = 4
    scrollPadStartPositionX = 5
    scrollPadVisibleHeight = height - 5
    scrollPadVisibleWidth = width - scrollPadStartPositionX
    scrollPadVisibleLines = scrollPadVisibleHeight - scrollPadStartPositionY
    scrollPadVisibleCols = scrollPadVisibleWidth - scrollPadStartPositionX
    
    # Split everything up into lines - todo: account for console width
    lines = []
    thisSectionStartChar = 0
    thisCharI = 0
    
    for x in OBJ_CONTENTSCREEN_SCROLL_TEXT:
        if x == "\n":
            lines.extend(textwrap.wrap(
                OBJ_CONTENTSCREEN_SCROLL_TEXT[thisSectionStartChar:thisCharI], width = scrollPadVisibleCols - 1)
            )
            
            lines.append("") # Paragraph break
            thisSectionStartChar = thisCharI + 1
         
        thisCharI += 1
    
    if direction == "up":
        OBJ_CONTENTSCREEN_SCROLL_POSITION -= 1
        
        if OBJ_CONTENTSCREEN_SCROLL_POSITION < 0:
            OBJ_CONTENTSCREEN_SCROLL_POSITION = 0
        
    elif direction == "down":
        OBJ_CONTENTSCREEN_SCROLL_POSITION += 1
        
        if OBJ_CONTENTSCREEN_SCROLL_POSITION >= len(lines) - scrollPadVisibleLines:
            OBJ_CONTENTSCREEN_SCROLL_POSITION = len(lines) - scrollPadVisibleLines
    
    # Setup the scrollbar
    OBJ_CONTENTSCREEN_SCROLL = curses.newpad(len(lines) + 1, 1000)
    OBJ_CONTENTSCREEN_SCROLL.bkgd(1, AppCommon.COLOR_BLOCKTEXT)
    
    i = 0
    for x in lines:
        try:
            OBJ_CONTENTSCREEN_SCROLL.addstr(i, 1, x, AppCommon.COLOR_BLOCKTEXT)
        except Exception, e:
            print e
            OBJ_CONTENTSCREEN_SCROLL.addstr(i, 1, "ERR")
        i += 1
    
    if  OBJ_CONTENTSCREEN_SCROLL_POSITION > len(lines) - scrollPadVisibleLines:
        lastLineIsVisible = True
    else:
        lastLineIsVisible = False
    
    
    if lastLineIsVisible is False:
        # Scroll
        OBJ_CONTENTSCREEN_SCROLL.refresh(OBJ_CONTENTSCREEN_SCROLL_POSITION, 0, scrollPadStartPositionY, scrollPadStartPositionX, scrollPadVisibleHeight, scrollPadVisibleWidth)
    else:
        # Don't scroll - still refresh the screen to ensure it's always rendered
        OBJ_CONTENTSCREEN_SCROLL.refresh(OBJ_CONTENTSCREEN_SCROLL_POSITION, 0, scrollPadStartPositionY, scrollPadStartPositionX, scrollPadVisibleHeight, scrollPadVisibleWidth)
    

