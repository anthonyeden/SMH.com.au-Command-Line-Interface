"""
 
 SMH.com.au Command Line Interface
 ------------------------------------------------------------------
 
 For those times you want to read your favourite Sydney newspaper
 from the comfort and convenience of your command line
 
 Built by Anthony Eden (http://mediarealm.com.au)
 on a lovely Sydney Sunday afternoon. Just for fun.
 
"""

import os
import curses
import textwrap

import AppCommon
import ArticleMenu
import ContentScreen
import Content_SMH

def runapp(stdscr):
    
    AppCommon.renderTopBar(stdscr)
    ArticleMenu.renderArticleMenu(stdscr)
    AppCommon.renderBottomBar(stdscr)
    
    while 1:
        c = stdscr.getch()
        
        if c == ord('q'):
            break  # Exit the while()
            
        elif c == curses.KEY_HOME:
            pass
            
        elif c == curses.KEY_RESIZE and AppCommon.SCREEN_CURRENT is "articlemenu":
            AppCommon.renderTopBar(stdscr)
            ArticleMenu.renderArticleMenu(stdscr)
            AppCommon.renderBottomBar(stdscr)
        
        elif c == curses.KEY_DOWN and AppCommon.SCREEN_CURRENT is "articlemenu":
            ArticleMenu.renderArticleMenuScroll(stdscr, "down")
            
        elif c == curses.KEY_UP and AppCommon.SCREEN_CURRENT is "articlemenu":
            ArticleMenu.renderArticleMenuScroll(stdscr, "up")
        
        elif c == 10 and AppCommon.SCREEN_CURRENT is "articlemenu":
            ContentScreen.renderContentScreen(stdscr)
            AppCommon.renderBottomBar(stdscr)
        
        elif c == curses.KEY_RESIZE and AppCommon.SCREEN_CURRENT is "content":
            AppCommon.renderTopBar(stdscr)
            ContentScreen.renderContentScreen(stdscr)
            AppCommon.renderBottomBar(stdscr)
        
        elif c == curses.KEY_DOWN and AppCommon.SCREEN_CURRENT is "content":
            ContentScreen.renderContentScreenScroll(stdscr, "down")
            
        elif c == curses.KEY_UP and AppCommon.SCREEN_CURRENT is "content":
            ContentScreen.renderContentScreenScroll(stdscr, "up")
        
        elif c == ord('r') and AppCommon.SCREEN_CURRENT is "content":
            # go back - return to the article index
            ArticleMenu.renderArticleMenu(stdscr)
            AppCommon.renderBottomBar(stdscr)



if __name__ == "__main__":
    
    print """
          _____                    _____                    _____          
         /\    \                  /\    \                  /\    \         
        /::\    \                /::\____\                /::\____\        
       /::::\    \              /::::|   |               /:::/    /        
      /::::::\    \            /:::::|   |              /:::/    /         
     /:::/\:::\    \          /::::::|   |             /:::/    /          
    /:::/__\:::\    \        /:::/|::|   |            /:::/____/           
    \:::\   \:::\    \      /:::/ |::|   |           /::::\    \           
  ___\:::\   \:::\    \    /:::/  |::|___|______    /::::::\    \   _____  
 /\   \:::\   \:::\    \  /:::/   |::::::::\    \  /:::/\:::\    \ /\    \ 
/::\   \:::\   \:::\____\/:::/    |:::::::::\____\/:::/  \:::\    /::\____\

\:::\   \:::\   \::/    /\::/    / ~~~~~/:::/    /\::/    \:::\  /:::/    /
 \:::\   \:::\   \/____/  \/____/      /:::/    /  \/____/ \:::\/:::/    / 
  \:::\   \:::\    \                  /:::/    /            \::::::/    /  
   \:::\   \:::\____\                /:::/    /              \::::/    /   
    \:::\  /:::/    /               /:::/    /               /:::/    /    
     \:::\/:::/    /               /:::/    /               /:::/    /     
      \::::::/    /               /:::/    /               /:::/    /      
       \::::/    /               /:::/    /               /:::/    /       
        \::/    /                \::/    /                \::/    /        
         \/____/                  \/____/                  \/____/         
                                                                           
    """
    
    stdscr = curses.initscr()
    curses.noecho() # Don't display text input on the screen
    curses.cbreak() # Allow processing keys before 'enter' is pressed
    stdscr.keypad(1) # Detect special key presses
    curses.start_color() # We want to use colours
    curses.setsyx(0, 0) # Set the cursor default position to 0,0
    
    curses.init_pair(1, curses.COLOR_WHITE, 24)
    curses.init_pair(2, curses.COLOR_WHITE, 1)
    curses.init_pair(3, 4, curses.COLOR_WHITE)
    
    AppCommon.COLOR_MENU = curses.color_pair(2)
    AppCommon.COLOR_BODY = curses.color_pair(1)
    AppCommon.COLOR_BLOCKTEXT = curses.color_pair(3)
    
    # Fetch index content before we properly load the app
    ArticleMenu.OBJ_ARTICLEMENU_SCROLL_ITEMS = Content_SMH.fetchArticleIndex()
    
    # Load the app via a wrapper
    curses.wrapper(runapp)
    
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    
    