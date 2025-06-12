from pydantic import BaseModel
from typing import Dict, List


class ExceptionResponse(BaseModel):
    detail: str

class NotesResponse(BaseModel):
    title:str
    description:str
    audio:str
    pdf:str
    notes:str

class BaseQuizResponse(BaseModel):
    prompt:str
    pdf:str

class QuizResponse(BaseQuizResponse):
    questions:List[Dict]