from app.schemas.guide import SafetyGuideCreate

def test_safety_guide_schema():
    guide = SafetyGuideCreate(
        category="Medical",
        title="Severe Bleeding First Aid",
        summary="Emergency steps to halt major blood loss.",
        steps=["Apply direct pressure", "Elevate limb", "Apply tourniquet if needed"]
    )
    assert len(guide.steps) == 3
