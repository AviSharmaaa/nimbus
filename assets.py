HOUSE = [
    r"         /\         ",
    r"        /  \        ",
    r"       / __ \       ",
    r"      /|    |\      ",
    r"     / |    | \     ",
    r"    /__|____|__\    ",
    r"    |  | __ |  |    ",
    r"    |  ||  ||  |    ",
    r"    |  ||  ||  |    ",
    r"    |__|____|__|    ",
    r"  __________________",
    r" /                  ",
]

# Sun rotates through 3 animation frames
SUN_FRAMES = [
    [
        r"     \   |   /    ",
        r"      \  |  /     ",
        r"  ---  (   )  --- ",
        r"      /  |  \     ",
        r"     /   |   \    ",
    ],
    [
        r"      \  |  /     ",
        r"    \  \ | /  /   ",
        r"  ---  (   )  --- ",
        r"    /  / | \  \   ",
        r"      /  |  \     ",
    ],
    [
        r"   \     |     /  ",
        r"     \   |   /    ",
        r"  ---  (   )  --- ",
        r"     /   |   \    ",
        r"   /     |     \  ",
    ],
]

# Fluffy clouds used in sunny / rain scenes
CLOUD_SHAPES = [
    r"   .--.  .--.",
    r"  (    ''    )",
    r"   '--'--'--' ",
]

CLOUD_SHAPES_2 = [
    r"  .---... ",
    r" (       )",
    r"  '-----' ",
]

# Heavy storm cloud bands used in thunder scene
STORM_CLOUD_ROWS = [
    "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
    "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
    "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
]

# Lightning bolt shapes for thunder scene — cycles through on each strike
LIGHTNING_BOLTS = [
    ["   /", "  / ", " /  ", " \\  ", "  \\ "],
    ["  \\  ", "   \\ ", "    \\", "   / ", "  /  "],
    ["  |  ", "  |  ", " /   ", "/    ", "\\    "],
]

# Short display labels shown in the info panel
WEATHER_ASCII_LABELS = {
    "sun":     "( SUN )",
    "cloud":   "~CLOUDS~",
    "rain":    "///RAIN\\\\\\",
    "snow":    "* SNOW *",
    "thunder": "!STORM!",
    "fog":     "...FOG...",
}
