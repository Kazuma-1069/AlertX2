class MapsService:
    def get_maps_url(self, lat, lng):
        return f"https://maps.google.com/?q={lat},{lng}"

maps_service = MapsService()
