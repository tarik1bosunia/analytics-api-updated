from fastapi import APIRouter, Depends, HTTPException
from api.db.session import get_session

from sqlmodel import Session, desc, select, asc

import os
from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema,
    get_utc_now
)
from api.db.config import DATABASE_URL
router = APIRouter()

# GET /api/events/
@router.get("/", response_model=EventListSchema)
def get_events(session: Session = Depends(get_session)):
    query = select(EventModel).order_by(desc(EventModel.updated_at)).limit(200)
    results = session.exec(query).all()
    return EventListSchema(results=list(results), count=len(results))
# POST /api/events/
@router.post("/", response_model=EventModel)
def create_event(
    payload: EventCreateSchema, 
    session: Session = Depends(get_session)
    ):
    print("Received data:", payload)
    print(type(payload))
    print("Page value:", payload.page)
    data = payload.model_dump()
    print("Model dump data:", data)
    obj = EventModel.model_validate(data)
    print("Validated model object:", obj)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# GET /api/events/{event_id}
@router.get("/{event_id}", response_model=EventModel)
def get_event(
    event_id: int,
    session: Session = Depends(get_session)
):
    query = select(EventModel).where(EventModel.id == event_id)
    event = session.exec(query).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


# PUT /api/events/{event_id}
@router.put("/{event_id}", response_model=EventModel)
def update_event(
    event_id: int, 
    payload: EventUpdateSchema,
    session: Session = Depends(get_session)
    ):
    print("Received data for update:", payload)
    print(type(payload))
    print("Description value:", payload.description)
    
    query = select(EventModel).where(EventModel.id == event_id)
    event = session.exec(query).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    

    data = payload.model_dump()
    
    for k, v in data.items():
        setattr(event, k, v)
        
    event.updated_at = get_utc_now()
    
    session.add(event)
    session.commit()
    session.refresh(event)
    
    return event



# DELETE /api/events/{event_id}
@router.delete("/{event_id}", response_model=EventModel)
def delete_event(
    event_id: int,
    session: Session = Depends(get_session),
):
    event = session.get(EventModel, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    session.delete(event)
    session.commit()
    return event

