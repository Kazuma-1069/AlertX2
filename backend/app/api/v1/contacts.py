from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from app.repositories.contact_repository import ContactRepository

router = APIRouter()

@router.get("", response_model=List[ContactResponse])
async def list_contacts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ContactRepository(db)
    return await repo.get_user_contacts(current_user.id)

@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact_in: ContactCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ContactRepository(db)
    contact = Contact(
        user_id=current_user.id,
        name=contact_in.name,
        phone_number=contact_in.phone_number,
        email=contact_in.email,
        relationship=contact_in.relationship,
        is_primary=contact_in.is_primary,
        receive_sms=contact_in.receive_sms,
        receive_call=contact_in.receive_call,
        receive_whatsapp=contact_in.receive_whatsapp
    )
    return await repo.create(contact)

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ContactRepository(db)
    contact = await repo.get_by_id(contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    await repo.delete(contact)
    return None
