from app.native.android_location import native_location

def test_native_location_fallback():
    coords = native_location.get_current_coordinates()
    assert len(coords) == 2
    assert isinstance(coords[0], float)
    assert isinstance(coords[1], float)
