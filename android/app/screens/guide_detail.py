"""
guide_detail.py -- Detailed safety-guide viewer for AlertX.

Loads full step-by-step content from a built-in offline dictionary and
renders it as a scrollable numbered list so users can act even without
an internet connection.
"""

from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

from app.utils.logger import app_logger

# ---------------------------------------------------------------------------
# Built-in offline guide data
# ---------------------------------------------------------------------------
GUIDES = {
    "cpr": {
        "title": "CPR - Cardiopulmonary Resuscitation",
        "category": "Medical",
        "steps": [
            "Ensure the scene is safe before approaching the victim.",
            "Check responsiveness -- tap their shoulder and shout 'Are you OK?'",
            "Call emergency services (or ask a bystander to call) immediately.",
            "Place the person flat on their back on a firm surface.",
            "Kneel beside the person's chest.",
            "Interlace fingers; place heel of dominant hand on centre of chest (lower half of sternum).",
            "Keep arms straight, compress the chest at least 5 cm (2 inches) deep.",
            "Deliver 30 chest compressions at a rate of 100-120 per minute.",
            "After 30 compressions, tilt head back and lift chin to open the airway.",
            "Pinch the nose shut, take a normal breath and make a complete seal over the mouth.",
            "Give 2 rescue breaths -- each breath should last ~1 second and make the chest rise visibly.",
            "Immediately resume 30 chest compressions after the 2 breaths.",
            "Continue the 30:2 cycle until: an AED is available, help arrives, the person shows signs of life, or you are unable to continue.",
            "If an AED arrives, power it on and follow voice prompts immediately.",
            "Do NOT stop CPR to check for a pulse more than once every 2 minutes.",
        ],
    },
    "earthquake": {
        "title": "Earthquake - Drop, Cover & Hold On",
        "category": "Natural Disaster",
        "steps": [
            "DROP to hands and knees immediately when shaking begins -- do not try to run.",
            "Take COVER under a sturdy desk or table, or against an interior wall away from windows.",
            "HOLD ON to your shelter and protect your head and neck with your free arm.",
            "Stay in position until the shaking completely stops -- do not run outside during shaking.",
            "If no table is nearby, drop to the floor against an interior wall; cover head with arms.",
            "NEVER shelter in a doorway -- modern frames offer no special protection.",
            "After shaking stops, expect aftershocks -- be ready to DROP again.",
            "Check yourself and others for injuries; apply first aid as needed.",
            "Check for gas leaks -- if you smell gas, open windows, leave the building and call the gas company.",
            "Check for electrical damage -- if sparks or frayed wires are visible, switch off the main power.",
            "Inspect the building for structural damage before re-entering. If unsafe, evacuate.",
            "Stay away from damaged buildings, downed power lines and debris.",
            "Use text messages instead of calls to preserve emergency network capacity.",
            "Listen to official broadcasts on a battery-powered or hand-crank radio.",
            "Do NOT use candles or open flames if a gas leak is possible.",
        ],
    },
    "fire": {
        "title": "Fire Emergency - RACE Protocol & Evacuation",
        "category": "Fire",
        "steps": [
            "RESCUE: Remove anyone in immediate danger if it is safe to do so.",
            "ALARM: Activate the nearest fire alarm pull station and call emergency services.",
            "CONFINE: Close all doors and windows to slow the spread of fire and smoke.",
            "EVACUATE / EXTINGUISH: Evacuate immediately; only use an extinguisher on small, contained fires.",
            "Use PASS for extinguisher: Pull the pin, Aim at the base, Squeeze the handle, Sweep side-to-side.",
            "Never use an elevator during a fire -- always use the stairs.",
            "Feel doors before opening -- if the door is hot or smoke is visible underneath, do NOT open it.",
            "Stay low to the floor where the air is cooler and less smoky.",
            "Close doors between you and the fire to slow its spread.",
            "If your clothes catch fire: STOP, DROP and ROLL until the flames are extinguished.",
            "Once outside, move to the designated assembly point and stay there.",
            "Never go back into a burning building for any reason.",
            "If you cannot escape, seal gaps under doors with clothing or towels to block smoke.",
            "Signal for help from a window with a light-coloured cloth or phone torch.",
            "Wait for firefighters -- do not jump unless instructed by emergency services.",
        ],
    },
    "first_aid": {
        "title": "First Aid - Bleeding & Shock",
        "category": "Medical",
        "steps": [
            "Ensure your personal safety -- wear gloves if available before touching blood.",
            "Call emergency services for serious bleeding or suspected internal bleeding.",
            "Apply firm, direct pressure to the wound using a clean cloth or bandage.",
            "Do NOT remove the cloth if it becomes soaked -- add more material on top and keep pressing.",
            "Maintain continuous pressure for at least 10-15 minutes without lifting the cloth.",
            "If the wound is on a limb and bleeding is severe, elevate the limb above heart level.",
            "Apply a tourniquet 5-7 cm above the wound as a last resort for life-threatening limb bleeding.",
            "Note the time of tourniquet application and do NOT remove it.",
            "For shock: lay the person flat, elevate legs 30 cm unless a head/neck injury is suspected.",
            "Keep the person warm with a blanket to prevent heat loss.",
            "Do NOT give food or water to a person in shock.",
            "Loosen tight clothing around the neck, chest and waist.",
            "Reassure the person -- calmly talk to them to reduce anxiety.",
            "Monitor breathing and pulse every 2 minutes; be ready to start CPR if needed.",
            "Stay with the person until professional medical help arrives.",
        ],
    },
    "flood": {
        "title": "Flood Safety & Evacuation",
        "category": "Natural Disaster",
        "steps": [
            "Monitor official weather alerts and heed evacuation orders immediately.",
            "Do NOT wait for water to reach your home -- evacuate early if advised.",
            "Turn off utilities at the main switches before leaving if time allows.",
            "Disconnect electrical appliances -- do NOT touch them if wet or while standing in water.",
            "Move important documents, medicines and valuables to upper floors or a waterproof bag.",
            "Never walk through moving flood water -- 15 cm of fast-moving water can knock you down.",
            "Never drive through a flooded road -- 30 cm of water can sweep away most vehicles.",
            "If your vehicle stalls in water, abandon it immediately and move to higher ground.",
            "If caught indoors during rapid flooding, move to the highest level of the building.",
            "Do NOT enter an attic unless you have a way to break through to the roof if water rises.",
            "Signal for rescue from a window or rooftop using a torch, bright cloth or mirror.",
            "Avoid contact with flood water -- it may be contaminated with sewage and chemicals.",
            "After flood recedes, do NOT re-enter a building until authorities declare it safe.",
            "Photograph damage for insurance purposes before cleaning up.",
            "Boil drinking water or use bottled water until mains supply is confirmed safe.",
        ],
    },
    "heimlich": {
        "title": "Heimlich Manoeuvre - Choking Response",
        "category": "Medical",
        "steps": [
            "Ask 'Are you choking?' -- if they cannot speak, cough or breathe, act immediately.",
            "Call emergency services (or ask someone else to call) right away.",
            "Encourage the person to cough forcefully if they are still able -- this may dislodge the object.",
            "If coughing fails, stand behind the person and lean them slightly forward.",
            "Give up to 5 sharp back blows between the shoulder blades using the heel of your hand.",
            "After each back blow, check if the obstruction has cleared.",
            "If 5 back blows fail, perform abdominal thrusts (Heimlich manoeuvre).",
            "Make a fist; place the thumb side against the abdomen just above the navel and below the breastbone.",
            "Grasp your fist with the other hand.",
            "Give up to 5 quick, firm inward-and-upward thrusts.",
            "Alternate 5 back blows and 5 abdominal thrusts until the object is expelled or the person loses consciousness.",
            "If the person becomes unconscious, gently lower them to the ground and call for help.",
            "Begin CPR if the person is unresponsive and not breathing normally.",
            "Each time you open the airway for rescue breaths, look for the object -- remove it only if clearly visible.",
            "For pregnant or obese individuals: use chest thrusts instead of abdominal thrusts.",
        ],
    },
}


# ---------------------------------------------------------------------------
class GuideDetailScreen(MDScreen):
    """
    Detailed safety-guide viewer.

    Call load_guide(guide_id) before or after pushing this screen to
    populate the title and step-by-step content.
    """

    guide_title = StringProperty("Safety Guide")
    guide_category = StringProperty("General")
    guide_content = StringProperty("")
    guide_id = StringProperty("")

    # -- Public API -----------------------------------------------------------
    def load_guide(self, guide_id: str):
        """
        Populate the screen with guide data identified by guide_id.
        Falls back to a user-friendly error message when the guide is unknown.
        """
        self.guide_id = guide_id
        data = GUIDES.get(guide_id)

        if data is None:
            app_logger.warning("GuideDetailScreen: unknown guide_id '%s'", guide_id)
            self.guide_title = "Guide Not Found"
            self.guide_category = "--"
            self.guide_content = (
                "This guide is not available offline.\n"
                "Please connect to the internet and try again."
            )
            self._update_ui()
            return

        self.guide_title = data["title"]
        self.guide_category = data["category"]
        self.guide_content = self._format_steps(data["steps"])
        app_logger.info("GuideDetailScreen: loaded guide '%s'", guide_id)
        self._update_ui()

    # -- Lifecycle ------------------------------------------------------------
    def on_enter(self, *args):
        """Reload guide content when the screen becomes active."""
        if self.guide_id:
            self.load_guide(self.guide_id)

    # -- Formatting -----------------------------------------------------------
    @staticmethod
    def _format_steps(steps: list) -> str:
        """Return a numbered multi-line string from steps list."""
        return "\n\n".join(f"{i + 1}. {step}" for i, step in enumerate(steps))

    # -- UI update ------------------------------------------------------------
    def _update_ui(self):
        """Push current property values into the KV widgets."""
        try:
            self.ids.guide_title_label.text = self.guide_title
            self.ids.category_chip_label.text = self.guide_category
            self.ids.content_label.text = self.guide_content
        except Exception as exc:
            app_logger.warning("GuideDetailScreen._update_ui: %s", exc)

    # -- Navigation -----------------------------------------------------------
    def go_back(self):
        try:
            self.manager.current = "guides"
        except Exception as exc:
            app_logger.error("GuideDetailScreen.go_back: %s", exc)
            try:
                self.manager.current = "home"
            except Exception:
                pass

    # -- Emergency dial -------------------------------------------------------
    def call_emergency(self):
        """Attempt to open the phone dialer with the emergency number."""
        try:
            from plyer import call as plyer_call
            plyer_call.makecall(tel="112")
            app_logger.info("Emergency call initiated.")
        except Exception as exc:
            app_logger.warning("Could not initiate emergency call: %s", exc)
            try:
                from kivymd.uix.snackbar import Snackbar
                sb = Snackbar(text="Dial 112 for emergency services.")
                sb.open()
            except Exception:
                pass
