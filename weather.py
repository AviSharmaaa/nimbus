
from __future__ import annotations
try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

# Maps keywords in the weather description → internal scene type
_CONDITION_KEYWORDS = [
    ("thunder", ["thunder", "storm", "lightning"]),
    ("rain",    ["rain", "drizzle", "shower"]),
    ("snow",    ["snow", "sleet", "blizzard", "ice"]),
    ("sun",     ["sunny", "clear"]),
    ("cloud",   ["cloud", "overcast"]),
    ("fog",     ["fog", "mist", "haze"]),
]

_HEADERS = {"User-Agent": "WeatherTerm/1.0"}

DEMO_DATA = {
    "type": "sun",
    "desc": "Demo Mode",
    "temp_c": "22", "temp_f": "72", "feels_c": "21",
    "humidity": "65", "wind_kmph": "15",
    "visibility": "10", "location": "Demo City",
}


def classify_condition(description: str) -> str:
    """Map a weather description string to an internal scene type."""
    desc_lower = description.lower()
    for scene_type, keywords in _CONDITION_KEYWORDS:
        if any(kw in desc_lower for kw in keywords):
            return scene_type
    return "sun"  # default fallback


def get_real_location() -> str | None:
    """
    Use ipinfo.io to resolve the user's actual city from their IP.
    wttr.in's own auto-detect uses the ISP's registered IP, which is
    often wrong (e.g. resolves to a data-center city instead of yours).
    """
    try:
        resp = requests.get("https://ipinfo.io/json", timeout=5, headers=_HEADERS)
        data = resp.json()
        city    = data.get("city", "")
        country = data.get("country", "")
        if city:
            return f"{city},{country}" if country else city
    except Exception:
        pass
    return None


def fetch_weather(city: str | None = None) -> dict:
    """
    Fetch current weather from wttr.in for the given city (or auto-detected
    location). Returns a flat dict with typed weather info, or {"error": ...}
    if something goes wrong.
    """
    if not REQUESTS_OK:
        return {"error": "'requests' library not installed. Run: pip install requests"}

    try:
        if not city:
            city = get_real_location()

        url  = f"https://wttr.in/{city or ''}?format=j1"
        resp = requests.get(url, timeout=8, headers=_HEADERS)
        data = resp.json()

        current = data["current_condition"][0]
        desc    = current["weatherDesc"][0]["value"]

        area     = data["nearest_area"][0]
        location = f"{area['areaName'][0]['value']}, {area['country'][0]['value']}"

        return {
            "type":       classify_condition(desc),
            "desc":       desc,
            "temp_c":     current["temp_C"],
            "temp_f":     current["temp_F"],
            "feels_c":    current["FeelsLikeC"],
            "humidity":   current["humidity"],
            "wind_kmph":  current["windspeedKmph"],
            "visibility": current["visibility"],
            "location":   location,
        }

    except Exception as exc:
        return {"error": str(exc)}


def make_demo_data(weather_type: str) -> dict:
    """Return a fake weather dict for the given demo type (no network needed)."""
    return {**DEMO_DATA, "type": weather_type, "desc": f"{weather_type.title()} (Demo)"}
