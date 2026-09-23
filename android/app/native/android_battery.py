class NativeBatteryManager:
    def get_battery_level(self) -> int:
        try:
            from plyer import battery
            status = battery.status
            return status.get("percentage", 95)
        except Exception:
            return 95

native_battery = NativeBatteryManager()
