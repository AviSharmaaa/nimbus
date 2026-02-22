# Color pair index map:
#   1  = BLUE fg       (rain drops)
#   2  = CYAN fg       (rain ripples / mist)
#   3  = WHITE fg      (house, snow, general text)
#   4  = YELLOW fg     (sun, lightning flash, title)
#   5  = GREEN fg      (ground / grass)
#   6  = MAGENTA fg    (unused, reserved)
#   7  = RED fg        (error messages)
#   12 = YELLOW on BLACK (status bar)
#   13 = GRAY fg       (clouds, card borders, dim text)

import curses


def setup_colors():
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1,  curses.COLOR_BLUE,    -1)                          # rain
    curses.init_pair(2,  curses.COLOR_CYAN,    -1)                          # ripples
    curses.init_pair(3,  curses.COLOR_WHITE,   -1)                          # general
    curses.init_pair(4,  curses.COLOR_YELLOW,  -1)                          # sun / flash
    curses.init_pair(5,  curses.COLOR_GREEN,   -1)                          # ground
    curses.init_pair(6,  curses.COLOR_MAGENTA, -1)                          # reserved
    curses.init_pair(7,  curses.COLOR_RED,     -1)                          # errors
    curses.init_pair(12, curses.COLOR_YELLOW,  curses.COLOR_BLACK)          # status bar

    # Gray — use extended color if the terminal supports it, fall back to WHITE
    try:
        curses.init_color(16, 600, 600, 600)
        curses.init_pair(13, 16, -1)
    except Exception:
        curses.init_pair(13, curses.COLOR_WHITE, -1)


# Named color helpers
# Using lambdas so they're evaluated lazily (curses must be initialized first).

def rain_color():    return curses.color_pair(1)
def ripple_color():  return curses.color_pair(2)
def general_color(): return curses.color_pair(3)
def sun_color():     return curses.color_pair(4) | curses.A_BOLD
def ground_color():  return curses.color_pair(5)
def error_color():   return curses.color_pair(7)
def status_color():  return curses.color_pair(12)
def dim_color():     return curses.color_pair(13)
def house_color():   return curses.color_pair(3) | curses.A_BOLD
def title_color():   return curses.color_pair(4) | curses.A_BOLD
def flash_color():   return curses.color_pair(4) | curses.A_BOLD
def snow_color():    return curses.color_pair(3) | curses.A_BOLD