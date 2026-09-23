from typing import List, Dict, Any

class AIService:
    async def get_safety_guidance(self, query: str, context: str = None) -> Dict[str, Any]:
        # Context-aware situational recommendations
        query_lower = query.lower()
        call_services = False
        suggested_actions = ["Move to a populated, well-lit area", "Keep emergency contacts updated"]
        quick_tips = ["Do not confront aggressors", "Trust your instincts"]

        if any(w in query_lower for w in ["follow", "stalk", "shadow"]):
            suggested_actions = [
                "Cross the street or enter an open commercial store immediately.",
                "Trigger AlertX2 SOS button to notify your designated emergency circle.",
                "Call local emergency services (112 / 911) directly."
            ]
            call_services = True
            response = "You may be in imminent danger. Do not head straight home if someone is following you. Head toward a public, open place like a convenience store, police station, or hospital."
        elif any(w in query_lower for w in ["fire", "smoke"]):
            suggested_actions = ["Get low under smoke", "Evacuate building immediately", "Call 101/911"]
            call_services = True
            response = "Immediate evacuation is required. Stay low to the ground to avoid toxic fumes. Feel doors before turning knobs."
        elif any(w in query_lower for w in ["heart", "breath", "bleed", "medical"]):
            suggested_actions = ["Call ambulance immediately", "Apply direct pressure if bleeding", "Keep patient calm"]
            call_services = True
            response = "Medical emergency detected. Contact paramedic response right away and follow the AlertX2 first-aid guides."
        else:
            response = f"AlertX2 Safety Assistant: Stay aware of your surroundings. If you feel uneasy, consider activating a safety countdown timer or alerting your trusted contacts."

        return {
            "response": response,
            "suggested_actions": suggested_actions,
            "call_emergency_services": call_services,
            "quick_tips": quick_tips
        }

ai_service = AIService()
