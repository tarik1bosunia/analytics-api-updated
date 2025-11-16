# from pydantic import SQLModel, Field
from sqlmodel import SQLModel, Field
from typing import List, Optional

"""
id
page
description
"""


class EventModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    page: Optional[str] = Field(default="")
    description: Optional[str] = Field(default="")

class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")

class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int = 0