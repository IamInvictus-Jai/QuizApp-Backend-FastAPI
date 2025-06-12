import fitz
from io import BytesIO
from logging import Logger
from app.schema.exceptions import FailedToExtractTextFromPDF


async def extract_text_from_pdf(pdf_file, logger:Logger) -> tuple[str, BytesIO]:

    try:
        text = ""
        content = await pdf_file.read()
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        
        pdf_io = BytesIO(content)
        pdf_io.name = pdf_file.filename
        return text, pdf_io
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {str(e)}")
        raise FailedToExtractTextFromPDF(str(e))