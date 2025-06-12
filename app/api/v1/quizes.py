from fastapi import APIRouter, status, Form, UploadFile
from dependency_injector.wiring import inject
from app.utils.dependencyManager import Dependencies

from app.schema.requestModel import *

quiz_router = APIRouter(
    prefix='/api/v1/quizes',
    tags=['Quizes'],
    responses={404: {"description": "Not found"}}
)

@quiz_router.post(
        "/create",
        response_model=QuizResponse,
        status_code=status.HTTP_201_CREATED,
    )
@inject
async def create_quiz(quiz_service:Dependencies.QuizServiceDependency, prompt:str=Form(...), pdf:UploadFile=UploadFile(...)):
    return await quiz_service.generate_quiz(pdf, prompt)