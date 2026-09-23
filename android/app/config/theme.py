"""AlertX Stitch Visual System & Design Tokens."""
from kivy.utils import get_color_from_hex

# Core Dark Palette (from stitch_alertx_safety_app_ui DESIGN.md)
COLOR_SURFACE = get_color_from_hex("#111316")
COLOR_SURFACE_CONTAINER_LOW = get_color_from_hex("#1A1C1F")
COLOR_SURFACE_CONTAINER = get_color_from_hex("#1E2023")
COLOR_SURFACE_CONTAINER_HIGH = get_color_from_hex("#282A2D")
COLOR_SURFACE_CONTAINER_HIGHEST = get_color_from_hex("#333538")

# Tactical Emergency & Semantic Accents
COLOR_EMERGENCY_RED = get_color_from_hex("#D92D20")
COLOR_EMERGENCY_BEACON = get_color_from_hex("#EF4444")
COLOR_EMERGENCY_LIGHT = get_color_from_hex("#FFB4A8")

COLOR_TRACKING_BLUE = get_color_from_hex("#8BCEFF")
COLOR_TRACKING_CONTAINER = get_color_from_hex("#00A2E8")

COLOR_TIMER_AMBER = get_color_from_hex("#F79009")
COLOR_SAFE_GREEN = get_color_from_hex("#12B76A")

# Typography Colors
COLOR_TEXT_PRIMARY = get_color_from_hex("#E2E2E6")
COLOR_TEXT_MUTED = get_color_from_hex("#A0A2A6")
COLOR_TEXT_ON_RED = get_color_from_hex("#FFF6F5")

# Spacing & Radii
RADIUS_SM = 4
RADIUS_MD = 8
RADIUS_LG = 16
RADIUS_XL = 24
RADIUS_FULL = 9999
