from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import User, Lab, Equipment, Reservation
from app.database import Base, engine
from app.api import api

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api)


@app.get('/')
def root():
    return {'message': 'FastAPI工程运行中'}
