"""
AlertX – Incident History Screen (Phase 7).

Loads all past SOS incidents from the local JSON store and presents them
in a scrollable, tappable list.  Tapping a row navigates to
IncidentDetailScreen via app.switch_incident(incident_id).
"""

import os
import json
from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

from app.utils.local_store import local_store
from app.utils.logger import app_logger
from app.config.theme import (
    COLOR_SURFACE,
    COLOR_SURFACE_CONTAINER,
    COLOR_SURFACE_CONTAINER_LOW,
    COLOR_SURFACE_CONTAINER_HIGH,
    COLOR_EMERGENCY_RED,
    COLOR_TIMER_AMBER,
    COLOR_SAFE_GREEN,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    RADIUS_MD,
    RADIUS_LG,
)

# Status → (label text, colour)
_STATUS_MAP = {
    "RESOLVED":  ("RESOLVED",  COLOR_SAFE_GREEN),
    "CANCELLED": ("CANCELLED", COLOR_TIMER_AMBER),
    "ACTIVE":    ("ACTIVE",    COLOR_EMERGENCY_RED),
}
_DEFAULT_STATUS = ("UNKNOWN", get_color_from_hex("#8B949E"))


def _fmt_dt(iso_str: str) -> str:
    """Return a human-readable date/time string from an ISO-8601 timestamp."""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d %b %Y  %H:%M")
    except Exception:
        return iso_str or "—"


def _fmt_duration(seconds) -> str:
    """Format a duration given as seconds (int/float) into m:ss."""
    try:
        secs = int(seconds)
        mins, secs = divmod(secs, 60)
        return f"{mins}m {secs:02d}s"
    except Exception:
        return str(seconds) if seconds else "—"


class IncidentRowCard(MDCard):
    """A single tappable incident row displayed in the history list."""

    incident_id = StringProperty("")

    def __init__(self, incident: dict, nav_callback, **kwargs):
        super().__init__(**kwargs)

        self.incident_id = incident.get("id", incident.get("incident_uuid", ""))
        self._nav_callback = nav_callback

        # Card visual style
        self.md_bg_color = COLOR_SURFACE_CONTAINER
        self.radius = [RADIUS_MD] * 4
        self.padding = [dp(14), dp(12), dp(14), dp(12)]
        self.size_hint_y = None
        self.height = dp(88)
        self.ripple_behavior = True

        status_key = incident.get("status", "").upper()
        status_label, status_color = _STATUS_MAP.get(status_key, _DEFAULT_STATUS)

        # ── Root row ──────────────────────────────────────────────────────────
        root_row = MDBoxLayout(orientation="horizontal", spacing=dp(10))

        # Left: icon column
        icon_col = MDBoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(36),
            padding=[0, dp(4), 0, 0],
        )
        icon_lbl = MDLabel(
            text="⚠",
            font_size="22sp",
            theme_text_color="Custom",
            text_color=status_color,
            halign="center",
            valign="top",
        )
        icon_col.add_widget(icon_lbl)

        # Middle: text column
        text_col = MDBoxLayout(orientation="vertical", spacing=dp(4))

        dt_str = _fmt_dt(incident.get("started_at", incident.get("timestamp", "")))
        date_lbl = MDLabel(
            text=dt_str,
            font_style="Subtitle2",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
            bold=True,
            size_hint_y=None,
            height=dp(22),
        )

        duration_str = _fmt_duration(incident.get("duration_seconds", incident.get("duration", "")))
        dur_lbl = MDLabel(
            text=f"Duration: {duration_str}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(18),
        )

        trigger = incident.get("trigger_type", incident.get("trigger", "Manual"))
        trigger_lbl = MDLabel(
            text=f"Trigger: {trigger}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(18),
        )

        text_col.add_widget(date_lbl)
        text_col.add_widget(dur_lbl)
        text_col.add_widget(trigger_lbl)

        # Right: status badge
        badge_col = MDBoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(80),
            padding=[0, dp(8), 0, 0],
        )
        badge = MDCard(
            md_bg_color=status_color,
            radius=[dp(4)] * 4,
            size_hint=(None, None),
            size=(dp(76), dp(22)),
        )
        badge_inner = MDBoxLayout(padding=[dp(4), 0, dp(4), 0])
        badge_lbl = MDLabel(
            text=status_label,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=get_color_from_hex("#FFFFFF"),
            bold=True,
            halign="center",
        )
        badge_inner.add_widget(badge_lbl)
        badge.add_widget(badge_inner)
        badge_col.add_widget(badge)

        root_row.add_widget(icon_col)
        root_row.add_widget(text_col)
        root_row.add_widget(badge_col)
        self.add_widget(root_row)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self._nav_callback(self.incident_id)
            return True
        return super().on_touch_up(touch)


class IncidentScreen(MDScreen):
    """
    Incident History Screen.

    Reads incidents from local JSON store and renders each one as a
    tappable card.  Navigates to IncidentDetailScreen on row tap.
    """

    incidents: ListProperty = ListProperty([])
    total_count: NumericProperty = NumericProperty(0)

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def on_enter(self):
        """Called every time this screen becomes active."""
        app_logger.info("IncidentScreen: on_enter – loading incidents")
        Clock.schedule_once(self._load_incidents, 0)

    def on_leave(self):
        """Clean up any transient state when navigating away."""
        app_logger.debug("IncidentScreen: on_leave")

    # ── Data loading ──────────────────────────────────────────────────────────

    def _load_incidents(self, *_args):
        """
        Load incidents from the local store (key: 'incidents').
        Falls back to reading ``local_data/incidents.json`` directly if the
        store key is empty, so the screen works both when an SOS has been
        triggered in-session and when the app starts fresh with pre-existing
        data.
        """
        incidents = local_store.get("incidents", [])

        if not incidents:
            incidents = self._load_from_file()

        # Sort newest first
        def _sort_key(inc):
            raw = inc.get("started_at", inc.get("timestamp", ""))
            try:
                return datetime.fromisoformat(raw)
            except Exception:
                return datetime.min

        incidents = sorted(incidents, key=_sort_key, reverse=True)

        self.incidents = incidents
        self.total_count = len(incidents)
        app_logger.info(f"IncidentScreen: loaded {self.total_count} incidents")

        # Re-render list
        self._render_list()

    def _load_from_file(self) -> list:
        """Read incidents.json from local_data/ directory if present."""
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(base, "local_data", "incidents.json")
        if not os.path.exists(path):
            app_logger.debug(f"IncidentScreen: no file at {path}")
            return []
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                if isinstance(data, list):
                    return data
                if isinstance(data, dict) and "incidents" in data:
                    return data["incidents"]
                return []
        except Exception as exc:
            app_logger.error(f"IncidentScreen: failed reading {path}: {exc}")
            return []

    # ── UI rendering ──────────────────────────────────────────────────────────

    def _render_list(self):
        """Populate the incident list container (id: incident_list) from KV."""
        try:
            container = self.ids.incident_list
        except AttributeError:
            app_logger.warning("IncidentScreen: 'incident_list' id not found – using fallback layout")
            self._build_fallback_layout()
            return

        container.clear_widgets()

        # Update the stat label
        try:
            self.ids.stat_label.text = f"{self.total_count}  Total Incidents"
        except AttributeError:
            pass

        if not self.incidents:
            empty_lbl = MDLabel(
                text="No incidents recorded yet.",
                halign="center",
                theme_text_color="Custom",
                text_color=COLOR_TEXT_MUTED,
                font_style="Body1",
                size_hint_y=None,
                height=dp(80),
            )
            container.add_widget(empty_lbl)
            return

        for incident in self.incidents:
            card = IncidentRowCard(
                incident=incident,
                nav_callback=self._open_incident,
            )
            container.add_widget(card)

        # Adjust container height so ScrollView works
        container.height = sum(
            child.height + dp(10) for child in container.children
        ) + dp(20)

    def _build_fallback_layout(self):
        """
        Emergency fallback: build the entire screen layout in pure Python
        when the KV file ids aren't available.  This ensures the screen is
        always functional even if kv/incident.kv fails to load.
        """
        self.clear_widgets()
        self.md_bg_color = COLOR_SURFACE

        root = MDBoxLayout(orientation="vertical")

        # ── Top bar ──
        topbar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            padding=[dp(8), dp(8), dp(16), dp(8)],
            md_bg_color=COLOR_SURFACE_CONTAINER_LOW,
            spacing=dp(4),
        )
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
        )
        back_btn.bind(on_release=lambda *_: self._go_back())
        title_lbl = MDLabel(
            text="Incident History",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
        )
        topbar.add_widget(back_btn)
        topbar.add_widget(title_lbl)
        root.add_widget(topbar)

        # ── Stat card ──
        stat_card = MDCard(
            md_bg_color=COLOR_EMERGENCY_RED,
            radius=[RADIUS_MD] * 4,
            size_hint_y=None,
            height=dp(56),
            padding=[dp(16), dp(8)],
        )
        stat_lbl = MDLabel(
            text=f"{self.total_count}  Total Incidents",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex("#FFFFFF"),
        )
        stat_card.add_widget(stat_lbl)

        stat_wrapper = MDBoxLayout(
            size_hint_y=None, height=dp(72), padding=[dp(16), dp(8)]
        )
        stat_wrapper.add_widget(stat_card)
        root.add_widget(stat_wrapper)

        # ── Scrollable list ──
        scroll = ScrollView()
        container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(10),
            padding=[dp(16), dp(8), dp(16), dp(16)],
        )
        container.bind(minimum_height=container.setter("height"))
        scroll.add_widget(container)
        root.add_widget(scroll)

        self.add_widget(root)

        # Render rows
        if not self.incidents:
            container.add_widget(
                MDLabel(
                    text="No incidents recorded yet.",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=COLOR_TEXT_MUTED,
                    size_hint_y=None,
                    height=dp(80),
                )
            )
        else:
            for incident in self.incidents:
                card = IncidentRowCard(
                    incident=incident,
                    nav_callback=self._open_incident,
                )
                container.add_widget(card)

    # ── Navigation helpers ────────────────────────────────────────────────────

    def _open_incident(self, incident_id: str):
        """Navigate to IncidentDetailScreen for the given incident_id."""
        app_logger.info(f"IncidentScreen: opening incident {incident_id}")
        app = self.manager.get_screen
        # Try the canonical app.switch_incident path first
        from kivy.app import App as _KivyApp
        kapp = _KivyApp.get_running_app()
        if hasattr(kapp, "switch_incident"):
            kapp.switch_incident(incident_id)
            return

        # Fallback: add IncidentDetailScreen dynamically if not yet registered,
        # then navigate to it.
        try:
            detail_screen = self.manager.get_screen("incident_detail")
        except Exception:
            from app.screens.incident_detail import IncidentDetailScreen
            detail_screen = IncidentDetailScreen(name="incident_detail")
            self.manager.add_widget(detail_screen)

        detail_screen.load_incident(incident_id)
        self.manager.current = "incident_detail"

    def _go_back(self):
        """Navigate back to home screen."""
        if self.manager:
            self.manager.current = "home"

    # ── Public helpers called from KV ─────────────────────────────────────────

    def go_back(self):
        """Called from KV back button."""
        self._go_back()
