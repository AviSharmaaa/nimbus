from __future__ import annotations
import curses
from assets import WEATHER_ASCII_LABELS
from colors import (
    title_color, general_color, rain_color, sun_color,
    ground_color, dim_color, error_color, status_color,
)


# Loading screen
def draw_loading(win, frame: int):
    """Centered splash screen shown while weather data is being fetched."""
    h, w    = win.getmaxyx()
    cx, cy  = w // 2, h // 2
    title   = "  Nimbus  "
    spinner = "|/-\\"[frame // 3 % 4]

    try:
        win.clear()
        win.addstr(cy - 3, cx - len(title) // 2, "╔" + "═" * len(title) + "╗", sun_color())
        win.addstr(cy - 2, cx - len(title) // 2, "║" + title               + "║", sun_color())
        win.addstr(cy - 1, cx - len(title) // 2, "╚" + "═" * len(title) + "╝", sun_color())
        win.addstr(cy + 1, cx - 12, "Fetching weather data...", general_color())
        win.addstr(cy + 2, cx, spinner, sun_color())
    except curses.error:
        pass


# Status bar
def draw_status_bar(win, frame: int):
    """Single-line status bar pinned to the bottom of the screen."""
    h, w = win.getmaxyx()
    text = f" [R] Refresh  [Q] Quit  |  Nimbus v1.0  |  Frame: {frame} "
    try:
        win.addstr(h - 1, 0, text[:w - 1].ljust(w - 1), status_color())
    except curses.error:
        pass


# Info panel
def draw_info_panel(win, weather_data: dict | None, frame: int):
    """
    Draws the panel occupying the bottom ~13 rows of the screen.
    Shows either a loading indicator, an error message, or three info cards.
    """
    h, w      = win.getmaxyx()
    panel_top = h - 13

    # Separator line
    try:
        win.addstr(panel_top, 0, "─" * (w - 1), sun_color())
    except curses.error:
        pass

    if weather_data is None:
        _draw_loading_placeholder(win, panel_top, frame)
        return

    if "error" in weather_data:
        _draw_error(win, panel_top, weather_data["error"])
        return

    _draw_weather_cards(win, panel_top, weather_data, w)


# Private helpers

def _draw_loading_placeholder(win, panel_top: int, frame: int):
    dots = "." * (frame // 10 % 4)
    try:
        win.addstr(panel_top + 1, 2, f"  Fetching weather data{dots}", general_color())
    except curses.error:
        pass


def _draw_error(win, panel_top: int, message: str):
    try:
        win.addstr(panel_top + 1, 2, f"  Error: {message}", error_color())
        win.addstr(panel_top + 2, 2, "  Tip: pass a city name -- e.g.  python nimbus Bengaluru", general_color())
    except curses.error:
        pass


def _draw_weather_cards(win, panel_top: int, data: dict, w: int):
    wtype    = data.get("type", "sun")
    label    = WEATHER_ASCII_LABELS.get(wtype, "?")
    location = data.get("location", "Unknown")
    desc     = data.get("desc", "")

    # Location + description header
    header = f"  {label}  {location}"
    try:
        win.addstr(panel_top + 1, 0, header[:w - 1], title_color())
        suffix = f"  [{desc}]"
        win.addstr(panel_top + 1, len(header), suffix[:w - 1 - len(header)], general_color())
    except curses.error:
        pass

    # Three cards: Temperature, Wind & Humidity, Visibility
    row2  = panel_top + 3
    col_w = (w - 2) // 3

    draw_card(win, row2, 1, col_w - 1, [
        ("  TEMPERATURE  ",                 sun_color()),
        (f"  {data['temp_c']}°C  /  {data['temp_f']}°F  ", general_color() | curses.A_BOLD),
        (f"  Feels like: {data['feels_c']}°C  ",            general_color()),
    ])

    draw_card(win, row2, col_w + 1, col_w - 1, [
        ("  WIND & HUMIDITY  ",             rain_color() | curses.A_BOLD),
        (f"  Humidity: {data['humidity']}%  ", general_color()),
        (f"  Wind: {data['wind_kmph']} km/h  ", general_color()),
    ])

    draw_card(win, row2, col_w * 2 + 1, col_w - 2, [
        ("  VISIBILITY  ",                  ground_color() | curses.A_BOLD),
        (f"  {data['visibility']} km  ",    general_color() | curses.A_BOLD),
        ("  Press Q to quit  ",             dim_color()),
    ])


def draw_card(win, y: int, x: int, w: int, lines: list[tuple]):
    """
    Render a bordered card at (y, x) with the given width.
    Each entry in `lines` is (text, curses_color_attr).
    """
    h_win, w_win = win.getmaxyx()
    if x >= w_win or y >= h_win or w < 3:
        return

    border = dim_color()

    try:
        win.addstr(y, x, "┌" + "─" * (w - 2) + "┐", border)
    except curses.error:
        pass

    for i, (text, color) in enumerate(lines):
        row = y + 1 + i
        if row >= h_win - 1:
            break
        padded = text[:w - 2].ljust(w - 2)
        try:
            win.addstr(row, x,             "│",     border)
            win.addstr(row, x + 1,         padded,  color)
            if x + w - 1 < w_win - 1:
                win.addstr(row, x + w - 1, "│",     border)
        except curses.error:
            pass

    bottom = y + 1 + len(lines)
    if bottom < h_win - 1:
        try:
            win.addstr(bottom, x, "└" + "─" * (w - 2) + "┘", border)
        except curses.error:
            pass
