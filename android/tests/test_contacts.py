from app.models.contact import ContactModel

def test_contact_model():
    c = ContactModel(id=1, name="John", phone_number="+1234567890", relationship="Brother")
    assert c.name == "John"
    assert c.relationship == "Brother"
