from fastapi import FastAPI
from app.routers import addresses
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API", description="Address Book with FastAPI and TDD")

app.include_router(addresses.router)
