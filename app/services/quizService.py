from fastapi import status, HTTPException
from app.utils.pdfExtractor import extract_text_from_pdf
from logging import Logger
from app.utils.readInstructions import LoadInstructions
from app.core.LLM import LLM
from app.schema.exceptions import FailedToGenerateResponse, FailedToExtractTextFromPDF
from app.schema.requestModel import QuizResponse
from app.schema.dbModel import Quiz
from json import loads, JSONDecodeError

class QuizService:
    def __init__(self, logger: Logger, loader: LoadInstructions, llm: LLM) -> None:
        self.loader = loader
        self.logger = logger
        self.quiz_prompt = self.loader.load('quiz_prompt.txt')
        self.llm = llm
    
    async def generate_quiz(self, pdf, user_prompt):
        
        try:
            pdf_text, pdf_bytesIO = await extract_text_from_pdf(pdf, self.logger)
            prompt = f"User prompt: {user_prompt}\n\npdf_data: {pdf_text}"
            quizDB = Quiz(
                prompt=prompt,
            )
            quizDB.pdf.put(pdf_bytesIO, filename=pdf.filename, content_type=pdf.content_type)

            quiz_unformatted = self.llm.generate_content(prompt, self.quiz_prompt, use_func_call=True)
            quiz_json = loads(quiz_unformatted)

            if isinstance(quiz_json, str):
                self.logger.error(f"Expected an array of questions from the LLM but got a single string instead: {quiz_json}")
                raise JSONDecodeError(
                    "Expecting array of obj format but Got single json string",
                    "Got single json string",
                    0
                )
            if isinstance(quiz_json, dict):                
                quizDB.save()
                return QuizResponse(
                    prompt=prompt,
                    pdf=str(quizDB.pdf),
                    questions=quiz_json['questions']
                )
            
            self.logger.error("Invalid json content from the LLM. Failed to parse the content")
            raise JSONDecodeError(
                "Expecting array of obj format but got invalid json content here",
                "Got invalid json content",
                0
            )           
        except JSONDecodeError as e:
            regenerated_quiz = self.llm.fallback_generate_content(quiz_unformatted)
            quiz_json = loads(regenerated_quiz)
            quizDB = Quiz(
                prompt=prompt,
            )
            quizDB.pdf.put(pdf_bytesIO, filename=pdf.filename, content_type=pdf.content_type)

            if not isinstance(quiz_json, dict):
                self.logger.error(f"Failed to generate a valid quiz after regenerating. Error: {e}")
                return HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Failed to generate quiz. Please try again later."
                )
            
            quizDB.save()
            return QuizResponse(
                prompt=prompt,
                pdf=str(quizDB.pdf),
                questions=quiz_json["questions"]
            )
        
        except FailedToGenerateResponse as e:
            self.logger.error(f"Failed to get response from the LLM: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to generate notes. Please try again later."
            )
        
        except FailedToExtractTextFromPDF as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to generate notes. Please try again later."
            )