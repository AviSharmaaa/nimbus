from __future__ import annotations
import curses
import random
import time
import threading

from assets import CLOUD_SHAPES, CLOUD_SHAPES_2, HOUSE
from colors import setup_colors
from particles import RainDrop, Snowflake, Cloud
from scenes import (
    draw_house,
    draw_rain_scene, draw_thunder_scene, draw_snow_scene,
    draw_sun_scene, draw_cloud_scene, draw_fog_scene,
)
from ui import draw_loading, draw_info_panel, draw_status_bar
from weather import fetch_weather, make_demo_data

# How many particles to spawn (capped so small terminals aren't overwhelmed)
MAX_DROPS  = 60
MAX_FLAKES = 40

# Target frame rate
FPS        = 20
FRAME_TIME = 1.0 / FPS


def _spawn_particles(w: int, h: int) -> dict:
    """Create the initial particle pools and cloud fleet."""
    num_drops  = min(MAX_DROPS,  w // 2)
    num_flakes = min(MAX_FLAKES, w // 2)
    return {
        "drops":  [RainDrop(w, h)    for _ in range(num_drops)],
        "flakes": [Snowflake(w, h)   for _ in range(num_flakes)],
        "clouds": [
            Cloud(w, random.randint(1, 6), CLOUD_SHAPES),
            Cloud(w, random.randint(2, 5), CLOUD_SHAPES_2),
            Cloud(w, random.randint(1, 4), CLOUD_SHAPES),
            Cloud(w, random.randint(3, 7), CLOUD_SHAPES_2),
            Cloud(w, random.randint(1, 5), CLOUD_SHAPES),
        ],
    }


def _update_particles(particles: dict, wtype: str):
    """Advance all particles one step. Thunder drops are faster and more diagonal."""
    for drop in particles["drops"]:
        if wtype == "thunder":
            if drop.speed < 2.5:
                drop.speed = random.uniform(2.5, 4.0)
            drop.update(wind=0.9)
        else:
            if drop.speed > 2.5:
                drop.speed = random.uniform(1.2, 2.0)
            drop.update(wind=0.15)

    for flake in particles["flakes"]:
        flake.update()

    for cloud in particles["clouds"]:
        cloud.update()


def _draw_scene(win, wtype: str, particles: dict, frame: int, weather_data: dict):
    """Route to the correct scene renderer based on weather type."""
    drops  = particles["drops"]
    flakes = particles["flakes"]
    clouds = particles["clouds"]

    scene_map = {
        "rain":    lambda: draw_rain_scene(win, drops, frame),
        "thunder": lambda: draw_thunder_scene(win, drops, frame),
        "snow":    lambda: draw_snow_scene(win, flakes),
        "sun":     lambda: draw_sun_scene(win, clouds[:2], frame, weather_data),
        "cloud":   lambda: draw_cloud_scene(win, clouds),
        "fog":     lambda: draw_fog_scene(win, frame),
    }
    scene_map.get(wtype, scene_map["sun"])()


def _start_fetch(city: str | None, demo_mode: str | None, result_box: list):
    """Kick off a background thread to fetch weather without blocking the UI."""
    def _worker():
        if demo_mode:
            result_box[0] = make_demo_data(demo_mode)
        else:
            result_box[0] = fetch_weather(city)

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    return thread


def run(stdscr, city: str | None, demo_mode: str | None):
    """Main curses loop — called via curses.wrapper()."""
    setup_colors()
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(int(FRAME_TIME * 1000))

    h, w         = stdscr.getmaxyx()
    particles    = _spawn_particles(w, h)
    frame        = 0
    weather_data = None
    loading      = True
    result_box   = [None]

    _start_fetch(city, demo_mode, result_box)

    while True:
        h, w = stdscr.getmaxyx()

        # Guard: terminal too small for scenes (need ~50×20 to show info panel + house)
        if h < 20 or w < 50:
            stdscr.clear()
            try:
                stdscr.addstr(0, 0, f"Terminal too small — need 50×20, got {w}×{h}", curses.color_pair(7))
            except curses.error:
                pass
            stdscr.refresh()
            time.sleep(0.1)
            if stdscr.getch() in (ord("q"), ord("Q"), 27):
                break
            continue

        # Input
        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            break
        if key in (ord("r"), ord("R")):
            result_box[0] = None
            loading       = True
            _start_fetch(city, demo_mode, result_box)

        # Check if fetch finished
        if loading and result_box[0] is not None:
            weather_data = result_box[0]
            loading      = False

        stdscr.erase()

        # Loading screen
        if loading:
            draw_loading(stdscr, frame)
            stdscr.refresh()
            frame += 1
            time.sleep(FRAME_TIME)
            continue

        # Determine weather type
        wtype = (
            weather_data.get("type", "sun")
            if weather_data and "error" not in weather_data
            else "sun"
        )

        # Draw
        _draw_scene(stdscr, wtype, particles, frame, weather_data)

        house_x = (w - 22) // 2
        house_y = h - 14 - len(HOUSE) + 2
        draw_house(stdscr, max(1, house_y), max(0, house_x), wtype)

        draw_info_panel(stdscr, weather_data, frame)
        draw_status_bar(stdscr, frame)

        stdscr.refresh()

        # Tick
        _update_particles(particles, wtype)
        frame += 1
        time.sleep(FRAME_TIME)
