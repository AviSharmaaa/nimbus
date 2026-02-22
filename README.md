# 🌤 Nimbus

An animated ASCII weather app that runs entirely in your terminal. Fetches live weather and renders a scene — rain, snow, sun, clouds, or a thunderstorm — complete with a house, particles, and real-time weather data.

---

## Preview

```
                    \   |   /
                     \  |  /
                 ---  (   )  ---
                     /  |  \
                    /   |   /

              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         /\
        /  \
       / __ \
      /|    |\
     / |    | \
    /__|____|__\
    |  | __ |  |
    |  ||  ||  |
    |__|____|__|
  __________________

──────────────────────────────────────────────────────
  ( SUN )  Bengaluru, India  [Sunny]
 ┌──────────────────┐ ┌──────────────────┐ ┌─────────────────┐
 │  TEMPERATURE     │ │  WIND & HUMIDITY │ │  VISIBILITY     │
 │  28°C  /  82°F   │ │  Humidity: 60%   │ │  10 km          │
 │  Feels like: 30°C│ │  Wind: 12 km/h   │ │  Press Q to quit│
 └──────────────────┘ └──────────────────┘ └─────────────────┘
```

---

## Features

- **6 animated weather scenes** — sun, rain, snow, clouds, thunderstorm, fog
- **Live weather data** from [wttr.in](https://wttr.in) — no API key needed
- **Smart location detection** via [ipinfo.io](https://ipinfo.io) — actually finds your city, not your ISP's
- **Distinct animations per scene** — gentle puddle ripples for rain vs diagonal slashing rain + lightning flash for thunder
- **Real-time info panel** — temperature, feels like, humidity, wind speed, visibility
- **Demo mode** — run any scene offline without internet
- **Refreshable** — press `R` to re-fetch live weather anytime

---

## Scenes

| Weather        | What you see                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------- |
| ☀ **Sun**      | Rotating sun rays, drifting clouds, green grass                                                       |
| 🌧 **Rain**    | Soft blue sky, scrolling clouds, vertical drops, ripple puddles                                       |
| ❄ **Snow**     | Sinusoidal drifting flakes, snow accumulation line                                                    |
| ☁ **Cloud**    | Overcast sky, multiple cloud banks drifting across                                                    |
| ⚡ **Thunder** | Near-black sky, heavy diagonal rain, storm clouds, screen flash + shake, lightning bolts, flood water |
| 🌫 **Fog**     | Scrolling dense fog blocks                                                                            |

---

## Installation

**Requirements:** Python 3.10+ and a terminal that supports color.

```bash
# Clone or download the project
cd nimbus

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate.bat       # Windows

# Install the only dependency
pip install requests
```

---

## Usage

```bash
# Auto-detect your location
python main.py

# Specific city
python main.py "Bengaluru"
python main.py "New York"
python main.py "Tokyo"

# Demo mode — no internet needed
python main.py --demo sun
python main.py --demo rain
python main.py --demo snow
python main.py --demo cloud
python main.py --demo thunder
python main.py --demo fog
```

---

## Controls

| Key          | Action               |
| ------------ | -------------------- |
| `R`          | Refresh weather data |
| `Q` or `Esc` | Quit                 |

---

## How It Works

1. **Location** — On startup, hits `ipinfo.io` to resolve your real city from your IP (much more accurate than letting `wttr.in` guess, which often returns your ISP's city)
2. **Weather fetch** — Calls `wttr.in/{city}?format=j1` in a background thread so the UI stays animated while loading
3. **Classification** — Maps the description string (e.g. `"Heavy Rain Shower"`) to an internal scene type (`rain`, `snow`, `thunder`, etc.)
4. **Rendering** — Uses Python's `curses` library to draw and animate directly in the terminal at ~20 fps

---

## Built With

- [`curses`](https://docs.python.org/3/library/curses.html) — Python standard library terminal UI
- [`wttr.in`](https://wttr.in) — Weather data, no API key required
- [`ipinfo.io`](https://ipinfo.io) — IP geolocation for accurate city detection
- [`requests`](https://docs.python-requests.org) — HTTP client

---

## Tips

- **Bigger terminal = better experience** — minimum 50×20, but the larger the better
- **Font matters** — use a monospace font like JetBrains Mono, Fira Code, or SF Mono for the ASCII art to render cleanly

---

## License


This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.
