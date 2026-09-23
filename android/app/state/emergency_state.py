class EmergencyState:
    def __init__(self):
        self.is_sos_active = False
        self.active_incident_uuid = None
        self.last_known_lat = 0.0
        self.last_known_lng = 0.0
        self.battery_level = 100

emergency_state = EmergencyState()
