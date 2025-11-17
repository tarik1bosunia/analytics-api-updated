# from pydantic import SQLModel, Field
from sqlmodel import SQLModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import sqlmodel

"""
id
page
description
"""

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    page: Optional[str] = Field(default="")
    description: Optional[str] = Field(default="")
    
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )
    
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )

class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")

class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int = 0