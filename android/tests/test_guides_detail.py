import pytest

def test_guides_dictionary_completeness():
    # Test GUIDES data without requiring Kivy UI initialization
    try:
        from app.screens.guide_detail import GUIDES, GuideDetailScreen
    except ModuleNotFoundError:
        pytest.skip("Kivy / KivyMD not installed in current environment")

    required_guides = ["cpr", "earthquake", "fire", "first_aid", "flood", "heimlich"]
    for g in required_guides:
        assert g in GUIDES, f"Missing required guide: {g}"
        guide = GUIDES[g]
        assert "title" in guide
        assert "category" in guide
        assert "steps" in guide
        assert len(guide["steps"]) > 0


def test_guide_detail_format_steps():
    try:
        from app.screens.guide_detail import GuideDetailScreen
    except ModuleNotFoundError:
        pytest.skip("Kivy / KivyMD not installed in current environment")

    steps = ["Check responsiveness", "Call 112", "Deliver compressions"]
    formatted = GuideDetailScreen._format_steps(steps)
    assert "1. Check responsiveness" in formatted
    assert "2. Call 112" in formatted
    assert "3. Deliver compressions" in formatted
