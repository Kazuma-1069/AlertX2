from app.schemas.contact import ContactCreate

def test_contact_schema_validation():
    contact = ContactCreate(
        name="Jane Doe",
        phone_number="+15551234567",
        relationship="Sister",
        is_primary=True,
        receive_sms=True,
        receive_call=True
    )
    assert contact.name == "Jane Doe"
    assert contact.is_primary is True
