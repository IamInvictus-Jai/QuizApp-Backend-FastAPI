import whisper
import tempfile
from io import BytesIO
from os import path, unlink
from logging import Logger
from app.schema.exceptions import FailedToTranscribeAudio

async def transcribe_audio(audio_file, logger:Logger) -> tuple[str, BytesIO]:
    # Implementation of service
    try:
        model = whisper.load_model("base")
        audio_stream = await audio_file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=path.splitext(audio_file.filename)[1]) as temp_audio_file:
            temp_audio_file.write(audio_stream)
            temp_audio_file.flush()

            transcription = model.transcribe(temp_audio_file.name)

        unlink(temp_audio_file.name)

        audio_io_stream = BytesIO(audio_stream)
        audio_io_stream.name = audio_file.filename

        return transcription["text"], audio_io_stream
    except Exception as e:
        logger.error(f"Failed to transcribe audio: {str(e)}")
        raise FailedToTranscribeAudio(str(e))