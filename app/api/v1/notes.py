from fastapi import APIRouter, status, Form, UploadFile
from dependency_injector.wiring import inject
from app.utils.dependencyManager import Dependencies

from app.schema.requestModel import *
from app.schema.exceptions import *

notes_router = APIRouter(
    prefix='/api/v1/notes',
    tags=['Notes'],
    responses={404: {"description": "Not found"}}
)

@notes_router.post(
        "/create",
        response_model=NotesResponse,
        status_code=status.HTTP_201_CREATED,
    )
@inject
async def create_note(
    notes_service:Dependencies.NotesServiceDependency,
    title:str=Form(...),
    description:str=Form(...),
    pdf:UploadFile=UploadFile(...),
    audio:UploadFile=UploadFile(...)
    ):
    return await notes_service.generate_notes(audio, pdf, title, description)
