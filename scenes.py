# One draw function per weather type + the house renderer
# Each scene function signature:
#   draw_<type>_scene(win, particles, frame)
#
# "particles" is a namespace so each scene only unpacks what it needs.

import curses
import math

from assets import (
    HOUSE, SUN_FRAMES,
    STORM_CLOUD_ROWS, LIGHTNING_BOLTS,
)
from colors import (
    rain_color, ripple_color, general_color, sun_color,
    ground_color, dim_color, house_color, snow_color,
    flash_color
)


# House
def draw_house(win, start_y: int, start_x: int, weather_type: str):
    """Render the ASCII house. Windows glow yellow on sunny days."""
    h, w = win.getmaxyx()
    window_lit = curses.color_pair(4)
    window_dim = curses.color_pair(4) | curses.A_DIM

    for row, line in enumerate(HOUSE):
        y = start_y + row
        if y >= h - 1:
            break
        for col, ch in enumerate(line):
            x = start_x + col
            if not 0 <= x < w - 1:
                continue
            try:
                if ch in r"/\|_":
                    win.addch(y, x, ch, house_color())
                elif ch in "[]":
                    color = window_lit if weather_type == "sun" else window_dim
                    win.addch(y, x, ch, color)
                elif ch == "*":
                    win.addch(y, x, ch, curses.color_pair(4) | curses.A_BOLD)
                else:
                    win.addch(y, x, ch, house_color())
            except curses.error:
                pass


# Rain
def draw_rain_scene(win, drops: list, frame: int):
    """
    Calm drizzle: soft cyan sky, scrolling fluffy clouds,
    gentle vertical drops, expanding puddle ripples on the ground.
    """
    h, w = win.getmaxyx()
    sky_height = h - 14

    # Soft cyan sky — slightly darker at top, lighter near horizon
    for row in range(sky_height):
        attr = curses.A_DIM if row < sky_height // 2 else 0
        try:
            win.addstr(row, 0, " " * (w - 1), ripple_color() | attr)
        except curses.error:
            pass

    # Two scrolling cloud bands
    _draw_scrolling_cloud_band(win, row=1, band=".-.(  ).-.  .-.(   ).  .-(    )-.  .(  ).", frame=frame // 2,   width=w)
    _draw_scrolling_cloud_band(win, row=4, band=" '---'  '--' '----'  '--'  '---'  '--'  ", frame=frame // 3, width=w)

    # Rain drops — thin vertical bars, barely any wind
    for drop in drops:
        iy, ix = int(drop.y), int(drop.x)
        if 0 <= iy < sky_height and 0 <= ix < w - 1:
            try:
                win.addch(iy, ix, ord("|"), rain_color())
            except curses.error:
                pass

    # Puddle ripples cycling . -> o -> O -> o -> .
    ground_y   = sky_height
    ripple_seq = [".", "o", "O", "o", "."]
    for col in range(3, w - 3, 9):
        phase = (frame + col * 3) // 6 % len(ripple_seq)
        try:
            win.addstr(ground_y, col, ripple_seq[phase], ripple_color() | curses.A_BOLD)
            if col + 2 < w - 1:
                win.addstr(ground_y, col + 2, ripple_seq[phase], rain_color())
        except curses.error:
            pass


# Thunder
def draw_thunder_scene(win, drops: list, frame: int):
    """
    Violent storm: near-black sky, heavy storm cloud bands, diagonal slashing rain,
    periodic full-screen lightning flash, jagged bolt strike, screen shake, flood water.
    """
    h, w = win.getmaxyx()
    sky_height = h - 14

    # Timing windows within an 90-frame (~4.5 s) cycle
    cycle    = frame % 90
    is_flash = cycle < 4
    is_bolt  = cycle < 6
    shake    = 1 if (cycle < 3 and frame % 2 == 0) else 0   # 1 row shake during strike

    # Sky background
    if is_flash:
        for row in range(sky_height):
            try:
                win.addstr(row + shake, 0, "░" * (w - 1), flash_color())
            except curses.error:
                pass
    else:
        for row in range(sky_height):
            try:
                win.addstr(row, 0, " " * (w - 1), rain_color() | curses.A_DIM)
            except curses.error:
                pass

    # Heavy storm cloud bands across the top
    for ci, band in enumerate(STORM_CLOUD_ROWS):
        row   = ci + shake
        if not 0 <= row < sky_height:
            continue
        offset  = (frame // 4 + ci * 7) % len(band)
        segment = (band * 2)[offset: offset + w - 1]
        attr    = curses.A_DIM if ci == 2 else 0
        try:
            win.addstr(row, 0, segment, dim_color() | attr)
        except curses.error:
            pass

    # Lightning bolt strike
    if is_bolt:
        bolt   = LIGHTNING_BOLTS[(frame // 90) % len(LIGHTNING_BOLTS)]
        bolt_x = (w // 3) + ((frame // 90 * 17) % (w // 2))
        bolt_y = len(STORM_CLOUD_ROWS) + 1 + shake
        for bi, line in enumerate(bolt):
            by = bolt_y + bi
            bx = min(bolt_x, w - len(line) - 1)
            if 0 <= by < sky_height:
                try:
                    win.addstr(by, bx, line, curses.color_pair(4) | curses.A_BOLD)
                except curses.error:
                    pass

    # Heavy diagonal rain "/" chars, fast, dense, double-height streaks
    for drop in drops:
        iy, ix = int(drop.y) + shake, int(drop.x)
        ch     = "/" if int(drop.x * 7) % 3 != 0 else "|"
        color  = general_color() | curses.A_BOLD if is_flash else rain_color()
        if 0 <= iy < sky_height and 0 <= ix < w - 1:
            try:
                win.addch(iy, ix, ord(ch), color)
            except curses.error:
                pass
        if 0 <= iy + 1 < sky_height and 0 <= ix < w - 1:
            try:
                win.addch(iy + 1, ix, ord("/"), rain_color() | curses.A_DIM)
            except curses.error:
                pass

    # Animated flood water on ground
    ground_y = sky_height
    wave     = "".join(["~", "~", "≈", "~", "~", "≈"][(col + frame // 2) % 6] for col in range(w - 1))
    try:
        win.addstr(ground_y, 0, wave, rain_color() | curses.A_BOLD)
    except curses.error:
        pass
    if ground_y + 1 < h - 1:
        try:
            win.addstr(ground_y + 1, 0, "░" * (w - 1), rain_color() | curses.A_DIM)
        except curses.error:
            pass


# Snow
def draw_snow_scene(win, flakes: list):
    """Cold, quiet snowfall with gentle side-drifting flakes and a snow ground line."""
    h, w = win.getmaxyx()
    sky_height = h - 14

    # Cold white-gray sky
    for row in range(sky_height):
        try:
            win.addstr(row, 0, " " * (w - 1), general_color() | curses.A_DIM)
        except curses.error:
            pass

    # Snowflakes
    for flake in flakes:
        iy, ix = int(flake.y), int(flake.x)
        if 0 <= iy < sky_height and 0 <= ix < w - 1:
            ch = flake.char if ord(flake.char) < 128 else "*"
            try:
                win.addch(iy, ix, ord(ch), snow_color())
            except curses.error:
                pass

    # Snow accumulation line
    try:
        win.addstr(sky_height, 0, "~*~*~*~*~" * (w // 9 + 1), snow_color())
    except curses.error:
        pass


# Sun
def draw_sun_scene(win, clouds: list, frame: int, _weather_data):
    """Bright sunny sky with a rotating sun, a few drifting clouds, and green grass."""
    h, w = win.getmaxyx()
    sky_height = h - 14

    # Bright yellow tinted sky
    for row in range(sky_height):
        try:
            win.addstr(row, 0, " " * (w - 1), sun_color() | curses.A_DIM)
        except curses.error:
            pass

    # Rotating sun (3 frame animation, changes every 15 frames)
    sun_frame = SUN_FRAMES[(frame // 15) % len(SUN_FRAMES)]
    sun_x     = max(0, w // 2 - 10)
    for i, line in enumerate(sun_frame):
        sy = 3 + i
        if 0 <= sy < sky_height:
            try:
                win.addstr(sy, sun_x, line, sun_color())
            except curses.error:
                pass

    # A couple of lazy clouds drifting across
    for cloud in clouds:
        _draw_cloud(win, cloud, sky_height, w, general_color() | curses.A_BOLD)

    # Green grass ground
    try:
        win.addstr(sky_height, 0, "^" * (w - 1), ground_color())
    except curses.error:
        pass


# Cloud
def draw_cloud_scene(win, clouds: list):
    """Overcast sky packed with slow-moving clouds."""
    h, w = win.getmaxyx()
    sky_height = h - 14

    # Gray overcast sky
    for row in range(sky_height):
        try:
            win.addstr(row, 0, " " * (w - 1), dim_color() | curses.A_DIM)
        except curses.error:
            pass

    for cloud in clouds:
        _draw_cloud(win, cloud, sky_height, w, dim_color() | curses.A_BOLD)


# Fog
def draw_fog_scene(win, frame: int):
    """Dense scrolling fog using block characters."""
    h, w = win.getmaxyx()
    sky_height = h - 14
    t = frame * 0.02

    for row in range(sky_height):
        # Slightly wavy horizontal density
        offset = int(math.sin(t + row * 0.3) * 3)
        fog    = ("░" * (w + abs(offset)))[abs(offset): abs(offset) + w - 1]
        try:
            win.addstr(row, 0, fog, dim_color() | curses.A_DIM)
        except curses.error:
            pass


# Private helpers
def _draw_cloud(win, cloud, sky_height: int, w: int, color):
    """Render a single Cloud object onto the window."""
    for ci, line in enumerate(cloud.shape):
        cy = int(cloud.y) + ci
        cx = int(cloud.x)
        if cy >= sky_height or cy < 0:
            continue
        if cx < 0:
            line = line[min(abs(cx), len(line)):]
            cx   = 0
        if cx + len(line) >= w:
            line = line[:w - 1 - cx]
        try:
            win.addstr(cy, cx, line, color)
        except curses.error:
            pass


def _draw_scrolling_cloud_band(win, row: int, band: str, frame: int, width: int):
    """Tile a cloud band string and scroll it horizontally over time."""
    offset  = frame % len(band)
    segment = (band * 3)[len(band) - offset:]
    try:
        win.addstr(row, 0, segment[:width - 1], general_color() | curses.A_BOLD)
    except curses.error:
        pass
