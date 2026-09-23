from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.contact import EmergencyContact
from app.schemas.contact import EmergencyContactCreate, EmergencyContactUpdate, EmergencyContactResponse
from app.repositories.contact_repository import ContactRepository

router = APIRouter()

@router.get("", response_model=List[EmergencyContactResponse])
async def list_emergency_contacts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ContactRepository(db)
    return await repo.get_user_contacts(current_user.id)

@router.post("", response_model=EmergencyContactResponse, status_code=status.HTTP_201_CREATED)
async def create_emergency_contact(contact_in: EmergencyContactCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ContactRepository(db)
    contact = EmergencyContact(
        user_id=current_user.id,
        name=contact_in.name,
        phone=contact_in.phone,
        relationship=contact_in.relationship,
        priority=contact_in.priority,
        receive_sos=contact_in.receive_sos,
        receive_location=contact_in.receive_location,
        receive_checkin_alert=contact_in.receive_checkin_alert
    )
    return await repo.create(contact)

@router.put("/{contact_id}", response_model=EmergencyContactResponse)
async def update_emergency_contact(contact_id: int, contact_update: EmergencyContactUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ContactRepository(db)
    contact = await repo.get_by_id(contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, val in contact_update.model_dump(exclude_unset=True).items():
        setattr(contact, field, val)
    return await repo.update(contact)

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emergency_contact(contact_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ContactRepository(db)
    contact = await repo.get_by_id(contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    await repo.delete(contact)
    return None
