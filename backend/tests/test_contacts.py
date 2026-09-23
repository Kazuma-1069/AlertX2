from app.schemas.contact import EmergencyContactCreate

def test_contact_schema_validation():
    contact = EmergencyContactCreate(
        name="Jane Doe",
        phone="+15551234567",
        relationship="Sister",
        priority=1,
        receive_sos=True,
        receive_location=True
    )
    assert contact.name == "Jane Doe"
    assert contact.priority == 1
    assert contact.receive_sos is True
