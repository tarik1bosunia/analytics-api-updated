from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.events.routing import router as events_router
from api.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    init_db()
    yield
    # Shutdown code
    # cleanup tasks
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(events_router, prefix="/api/events")


@app.get("/")
def read_root():
    return {"Hello": "Word"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}

