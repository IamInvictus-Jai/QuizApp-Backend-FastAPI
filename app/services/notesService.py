from fastapi import status, HTTPException
from app.utils.audioTranscriber import transcribe_audio
from app.utils.pdfExtractor import extract_text_from_pdf
from app.schema.exceptions import FailedToGenerateResponse, FailedToTranscribeAudio, FailedToExtractTextFromPDF
from app.schema.dbModel import Note
from app.schema.requestModel import NotesResponse

from logging import Logger
from app.utils.readInstructions import LoadInstructions
from app.core.LLM import LLM


class NotesService:
    def __init__(self, logger: Logger, loader: LoadInstructions, llm: LLM) -> None:
        self.loader = loader
        self.logger = logger
        self.notes_prompt = self.loader.load('notes_prompt.txt')
        self.llm = llm
    
    async def generate_notes(self, audio, pdf, title, description):
        
        try:
            audio_transcription, audio_io_stream = await transcribe_audio(audio, self.logger)
            pdf_text, pdf_io = await extract_text_from_pdf(pdf, self.logger)
            user_prompt = "pdf_data:" + pdf_text + "\n" + "teacher_transcript:" + audio_transcription

            notes = self.llm.generate_content(user_prompt, self.notes_prompt)
            notesDB = Note(
                title=title,
                description=description,
            )
            notesDB.audio.put(audio_io_stream, filename=audio.filename, content_type=audio.content_type)
            notesDB.pdf.put(pdf_io, filename=pdf.filename, content_type=pdf.content_type)
            notesDB.save()
            return NotesResponse(
                title=title,
                description=description,
                audio=str(notesDB.audio),
                pdf=str(notesDB.pdf),
                notes=notes
            )

        except FailedToGenerateResponse as e:
            self.logger.error(f"Failed to get response from the LLM: {str(e)}")
            return HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to generate notes. Please try again later."
            )
        
        except FailedToTranscribeAudio as e:
            return HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to transcribe audio. Please try again later."
            )
        
        except FailedToExtractTextFromPDF as e:
            return HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to extract text from PDF. Please try again later."
            )
