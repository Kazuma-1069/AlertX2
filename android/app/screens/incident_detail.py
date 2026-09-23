"""
AlertX – Incident Detail / Evidence Vault Screen (Phase 7).

Displays the full timeline of events and evidence items for a single
incident.  Provides 'Record Evidence' (audio capture via Plyer) and
'Export Report' (write JSON to local_data/exports/) actions.
"""

import os
import json
from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, DictProperty
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

# Optional Plyer audio capture – graceful fallback
try:
    from plyer import audio as _plyer_audio
    _PLYER_AVAILABLE = True
except ImportError:
    _plyer_audio = None
    _PLYER_AVAILABLE = False

# Map event types to Material Design icons
_EVENT_ICON = {
    "SOS_TRIGGERED":  "alert-circle",
    "LOCATION_UPDATE": "map-marker",
    "SMS_SENT":        "message-text",
    "CALL_MADE":       "phone",
    "SOS_RESOLVED":    "check-circle",
    "SOS_CANCELLED":   "close-circle",
    "RECORDING_START": "microphone",
    "RECORDING_STOP":  "microphone-off",
    "PHOTO_CAPTURED":  "camera",
}
_DEFAULT_ICON = "information"

# Evidence type → icon
_EVIDENCE_ICON = {
    "AUDIO":  "microphone",
    "IMAGE":  "image",
    "VIDEO":  "video",
    "TEXT":   "text-box",
}
_DEFAULT_EVIDENCE_ICON = "file"


def _fmt_dt(iso_str: str) -> str:
    """Return human-readable datetime from ISO-8601 string."""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d %b %Y  %H:%M:%S")
    except Exception:
        return iso_str or "—"


class IncidentDetailScreen(MDScreen):
    """
    Incident Detail & Evidence Vault Screen.

    Call ``load_incident(incident_id)`` before navigating here.
    """

    current_incident_id = StringProperty("")
    incident_data: DictProperty = DictProperty({})

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def on_enter(self):
        app_logger.info(
            f"IncidentDetailScreen: entered for incident '{self.current_incident_id}'"
        )
        if self.current_incident_id:
            Clock.schedule_once(lambda *_: self._populate_ui(), 0)

    def on_leave(self):
        app_logger.debug("IncidentDetailScreen: on_leave")

    # ── Public API ────────────────────────────────────────────────────────────

    def load_incident(self, incident_id: str):
        """
        Look up an incident by id in the local store (or incidents.json file)
        and store it ready for display.  Call this *before* navigating here.
        """
        app_logger.info(f"IncidentDetailScreen: loading incident '{incident_id}'")
        self.current_incident_id = incident_id
        self.incident_data = {}

        incidents = local_store.get("incidents", [])
        if not incidents:
            incidents = self._load_incidents_from_file()

        for inc in incidents:
            iid = inc.get("id", inc.get("incident_uuid", ""))
            if iid == incident_id:
                self.incident_data = inc
                app_logger.info(f"IncidentDetailScreen: found incident data ({len(inc)} keys)")
                return

        app_logger.warning(
            f"IncidentDetailScreen: incident '{incident_id}' not found in store"
        )

    # ── Data helpers ──────────────────────────────────────────────────────────

    def _load_incidents_from_file(self) -> list:
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(base, "local_data", "incidents.json")
        if not os.path.exists(path):
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
            app_logger.error(f"IncidentDetailScreen: failed reading file: {exc}")
            return []

    # ── UI population ─────────────────────────────────────────────────────────

    def _populate_ui(self):
        """Fill timeline and evidence lists using the stored incident_data."""
        inc = self.incident_data
        if not inc:
            app_logger.warning("IncidentDetailScreen: no incident_data to populate")
            self._build_fallback_layout(incident={})
            return

        # Try KV ids first, fall through to pure-Python fallback
        try:
            # Update header title
            self.ids.incident_title.text = (
                f"Incident  #{self.current_incident_id[:8].upper()}"
            )
            self._fill_timeline(self.ids.timeline_list, inc.get("events", []))
            self._fill_evidence(self.ids.evidence_list, inc.get("evidence", []))
        except (AttributeError, KeyError):
            app_logger.debug("IncidentDetailScreen: KV ids not available – building fallback layout")
            self._build_fallback_layout(incident=inc)

    def _fill_timeline(self, container, events: list):
        """Render event rows into the given container widget."""
        container.clear_widgets()
        if not events:
            container.add_widget(self._empty_label("No timeline events recorded."))
            container.height = dp(60)
            return

        for ev in events:
            row = self._make_event_row(ev)
            container.add_widget(row)

        container.height = len(events) * dp(52) + dp(8)

    def _fill_evidence(self, container, evidence: list):
        """Render evidence item rows into the given container widget."""
        container.clear_widgets()
        if not evidence:
            container.add_widget(self._empty_label("No evidence captured."))
            container.height = dp(60)
            return

        for item in evidence:
            row = self._make_evidence_row(item)
            container.add_widget(row)

        container.height = len(evidence) * dp(56) + dp(8)

    # ── Row builders ──────────────────────────────────────────────────────────

    def _make_event_row(self, event: dict) -> MDBoxLayout:
        event_type = event.get("type", event.get("event_type", "EVENT"))
        timestamp  = _fmt_dt(event.get("timestamp", event.get("ts", "")))
        icon_name  = _EVENT_ICON.get(event_type, _DEFAULT_ICON)

        row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=[dp(4), dp(4), dp(4), dp(4)],
        )

        # Dot / icon
        icon_lbl = MDLabel(
            text=f"[font=Icons]{chr(0xF012B)}[/font]",
            markup=True,
            size_hint_x=None,
            width=dp(32),
            font_size="18sp",
            theme_text_color="Custom",
            text_color=COLOR_EMERGENCY_RED,
            halign="center",
            valign="middle",
        )

        # Use MDIconButton as a static icon (no press needed)
        from kivymd.uix.button import MDIconButton as _MIB
        icon_btn = _MIB(
            icon=icon_name,
            size_hint=(None, None),
            size=(dp(32), dp(32)),
            theme_text_color="Custom",
            text_color=COLOR_EMERGENCY_RED,
            disabled=True,
        )

        # Text column
        text_col = MDBoxLayout(orientation="vertical", spacing=dp(2))
        type_lbl = MDLabel(
            text=event_type.replace("_", " ").title(),
            font_style="Body2",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
            bold=True,
            size_hint_y=None,
            height=dp(22),
        )
        ts_lbl = MDLabel(
            text=timestamp,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(18),
        )
        text_col.add_widget(type_lbl)
        text_col.add_widget(ts_lbl)

        row.add_widget(icon_btn)
        row.add_widget(text_col)
        return row

    def _make_evidence_row(self, item: dict) -> MDCard:
        ev_type   = item.get("type", item.get("evidence_type", "FILE")).upper()
        filename  = item.get("filename", item.get("path", "unknown_file"))
        timestamp = _fmt_dt(item.get("timestamp", item.get("captured_at", "")))
        icon_name = _EVIDENCE_ICON.get(ev_type, _DEFAULT_EVIDENCE_ICON)

        card = MDCard(
            md_bg_color=COLOR_SURFACE_CONTAINER_HIGH,
            radius=[RADIUS_MD] * 4,
            size_hint_y=None,
            height=dp(54),
            padding=[dp(12), dp(8), dp(12), dp(8)],
        )

        row = MDBoxLayout(orientation="horizontal", spacing=dp(10))

        from kivymd.uix.button import MDIconButton as _MIB
        icon_btn = _MIB(
            icon=icon_name,
            size_hint=(None, None),
            size=(dp(36), dp(36)),
            theme_text_color="Custom",
            text_color=COLOR_TIMER_AMBER,
            disabled=True,
        )

        text_col = MDBoxLayout(orientation="vertical", spacing=dp(2))
        name_lbl = MDLabel(
            text=os.path.basename(filename),
            font_style="Body2",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
            size_hint_y=None,
            height=dp(22),
        )
        ts_lbl = MDLabel(
            text=timestamp,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(18),
        )
        text_col.add_widget(name_lbl)
        text_col.add_widget(ts_lbl)

        type_badge = MDCard(
            md_bg_color=COLOR_SURFACE_CONTAINER_HIGH,
            radius=[dp(4)] * 4,
            size_hint=(None, None),
            size=(dp(54), dp(22)),
        )
        type_lbl = MDLabel(
            text=ev_type,
            font_style="Caption",
            bold=True,
            theme_text_color="Custom",
            text_color=COLOR_TIMER_AMBER,
            halign="center",
        )
        type_badge.add_widget(type_lbl)

        row.add_widget(icon_btn)
        row.add_widget(text_col)
        row.add_widget(type_badge)
        card.add_widget(row)
        return card

    def _empty_label(self, text: str) -> MDLabel:
        return MDLabel(
            text=text,
            halign="center",
            font_style="Body2",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(56),
        )

    # ── Actions ───────────────────────────────────────────────────────────────

    def _start_recording(self):
        """
        Begin audio capture via Plyer.
        Falls back to a no-op log message on desktop / when Plyer is absent.
        """
        if not _PLYER_AVAILABLE or _plyer_audio is None:
            app_logger.warning(
                "IncidentDetailScreen: Plyer audio not available – skipping recording"
            )
            self._show_snack("Audio recording not available on this platform.")
            return

        inc_id = self.current_incident_id
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        out_dir = os.path.join(base, "local_data", "evidence")
        os.makedirs(out_dir, exist_ok=True)

        ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(out_dir, f"rec_{inc_id[:8]}_{ts_str}.3gp")

        try:
            _plyer_audio.start(filename=out_path)
            app_logger.info(f"IncidentDetailScreen: recording started → {out_path}")
            self._recording_path = out_path
            # Auto-stop after 60 s as a safety guard
            Clock.schedule_once(self._stop_recording, 60)
            self._show_snack("Recording started…")
        except Exception as exc:
            app_logger.error(f"IncidentDetailScreen: failed to start recording: {exc}")
            self._show_snack(f"Recording error: {exc}")

    def _stop_recording(self, *_args):
        """Stop audio capture and register the file as evidence."""
        if not _PLYER_AVAILABLE or _plyer_audio is None:
            return
        try:
            _plyer_audio.stop()
            app_logger.info("IncidentDetailScreen: recording stopped")
        except Exception as exc:
            app_logger.error(f"IncidentDetailScreen: failed to stop recording: {exc}")
            return

        path = getattr(self, "_recording_path", None)
        if path and os.path.exists(path):
            self._register_evidence(path, ev_type="AUDIO")
            self._show_snack("Recording saved.")
        else:
            app_logger.warning("IncidentDetailScreen: recording file not found after stop")

    def _register_evidence(self, path: str, ev_type: str = "AUDIO"):
        """Append an evidence item to the incident in local_store."""
        incidents = local_store.get("incidents", [])
        for inc in incidents:
            iid = inc.get("id", inc.get("incident_uuid", ""))
            if iid == self.current_incident_id:
                evidence = inc.setdefault("evidence", [])
                evidence.append({
                    "type": ev_type,
                    "filename": path,
                    "timestamp": datetime.now().isoformat(),
                })
                local_store.set("incidents", incidents)
                # Refresh incident_data
                self.incident_data = inc
                Clock.schedule_once(lambda *_: self._populate_ui(), 0)
                app_logger.info(f"IncidentDetailScreen: registered {ev_type} evidence at {path}")
                return
        app_logger.warning(
            f"IncidentDetailScreen: could not register evidence – incident not found"
        )

    def _export_report(self):
        """
        Export the current incident as a JSON file to
        ``local_data/exports/incident_<id>.json``.
        """
        if not self.incident_data:
            self._show_snack("No incident data to export.")
            return

        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        export_dir = os.path.join(base, "local_data", "exports")
        os.makedirs(export_dir, exist_ok=True)

        safe_id = self.current_incident_id.replace("/", "_").replace("\\", "_")
        out_path = os.path.join(export_dir, f"incident_{safe_id}.json")

        report = {
            "exported_at": datetime.now().isoformat(),
            "incident": dict(self.incident_data),
        }

        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(report, fh, indent=2, default=str)
            app_logger.info(f"IncidentDetailScreen: report exported → {out_path}")
            self._show_snack(f"Report saved: incident_{safe_id[:12]}.json")
        except Exception as exc:
            app_logger.error(f"IncidentDetailScreen: export failed: {exc}")
            self._show_snack(f"Export failed: {exc}")

    def _show_snack(self, message: str):
        """Display a brief snackbar / toast message to the user."""
        try:
            from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
            sb = MDSnackbar(
                MDSnackbarText(text=message),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.85,
                duration=2.5,
            )
            sb.open()
        except Exception:
            # Older KivyMD or desktop env – just log
            app_logger.info(f"[Snack] {message}")

    # ── Navigation ────────────────────────────────────────────────────────────

    def go_back(self):
        """Navigate back to incident list screen."""
        if self.manager:
            self.manager.current = "incident"

    # ── KV button callbacks (bound in KV file) ────────────────────────────────

    def on_record_pressed(self):
        self._start_recording()

    def on_export_pressed(self):
        self._export_report()

    # ── Fallback pure-Python layout ───────────────────────────────────────────

    def _build_fallback_layout(self, incident: dict):
        """Build the full screen layout in Python when KV ids are absent."""
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
        back_btn.bind(on_release=lambda *_: self.go_back())

        iid_short = self.current_incident_id[:8].upper() if self.current_incident_id else "—"
        title_lbl = MDLabel(
            text=f"Incident  #{iid_short}",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
        )
        topbar.add_widget(back_btn)
        topbar.add_widget(title_lbl)
        root.add_widget(topbar)

        # ── Scrollable body ──
        scroll = ScrollView()
        body = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(16),
            padding=[dp(16), dp(12), dp(16), dp(24)],
        )
        body.bind(minimum_height=body.setter("height"))
        scroll.add_widget(body)

        # ── Timeline section ──
        body.add_widget(self._section_header("Timeline"))
        timeline_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(4),
        )
        timeline_container.bind(minimum_height=timeline_container.setter("height"))
        events = incident.get("events", [])
        self._fill_timeline(timeline_container, events)
        body.add_widget(timeline_container)

        # ── Evidence section ──
        body.add_widget(self._section_header("Evidence Vault"))
        evidence_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8),
        )
        evidence_container.bind(minimum_height=evidence_container.setter("height"))
        evidence = incident.get("evidence", [])
        self._fill_evidence(evidence_container, evidence)
        body.add_widget(evidence_container)

        # ── Action buttons ──
        btn_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            spacing=dp(12),
            padding=[0, dp(4), 0, dp(4)],
        )
        record_btn = MDRaisedButton(
            text="Record Evidence",
            md_bg_color=COLOR_EMERGENCY_RED,
        )
        record_btn.bind(on_release=lambda *_: self._start_recording())

        export_btn = MDFlatButton(
            text="Export Report",
            theme_text_color="Custom",
            text_color=COLOR_TIMER_AMBER,
        )
        export_btn.bind(on_release=lambda *_: self._export_report())

        btn_row.add_widget(record_btn)
        btn_row.add_widget(export_btn)
        body.add_widget(btn_row)

        root.add_widget(scroll)
        self.add_widget(root)

    def _section_header(self, text: str) -> MDBoxLayout:
        wrapper = MDBoxLayout(
            size_hint_y=None,
            height=dp(36),
            padding=[0, dp(4), 0, dp(4)],
        )
        lbl = MDLabel(
            text=text,
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRIMARY,
        )
        wrapper.add_widget(lbl)
        return wrapper
