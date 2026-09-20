from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.models import User, Lab, Equipment, Reservation
from app.database import Base, engine
from app.api import api
from app.services import ServiceError

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError):
    return JSONResponse(status_code=200, content={'code': exc.code, 'message': exc.message})


app.include_router(api)


@app.get('/')
def root():
    return {'message': 'FastAPI工程运行中'}
