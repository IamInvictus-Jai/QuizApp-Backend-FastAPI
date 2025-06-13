# import whisper
# import tempfile
# from os import path, unlink
from io import BytesIO
from logging import Logger
from app.schema.exceptions import FailedToTranscribeAudio
import requests
from app.config.settings import get_settings

# async def transcribe_audio(audio_file, logger:Logger) -> tuple[str, BytesIO]:
#     # Implementation of service
#     try:
#         model = whisper.load_model("base")
#         audio_stream = await audio_file.read()
#         with tempfile.NamedTemporaryFile(delete=False, suffix=path.splitext(audio_file.filename)[1]) as temp_audio_file:
#             temp_audio_file.write(audio_stream)
#             temp_audio_file.flush()

#             transcription = model.transcribe(temp_audio_file.name)

#         unlink(temp_audio_file.name)

#         audio_io_stream = BytesIO(audio_stream)
#         audio_io_stream.name = audio_file.filename

#         return transcription["text"], audio_io_stream
#     except Exception as e:
#         logger.error(f"Failed to transcribe audio: {str(e)}")
#         raise FailedToTranscribeAudio(str(e))
    
API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3-turbo"
HF_KEY = get_settings().HF_KEY
headers = {
    "Content-Type": "audio/mpeg",
    "Authorization": f"Bearer {HF_KEY}"
}

# Transcribe Audio using Huggingface API
async def transcribe_audio(audio_file, logger:Logger) -> tuple[str, BytesIO]:
    try:
        audio_stream = await audio_file.read()
        audio_io_stream = BytesIO(audio_stream)
        audio_io_stream.name = audio_file.filename

        response = requests.post(API_URL, data=audio_stream, headers=headers)
        if response.ok: return response.json()['text'], audio_io_stream
        else:
            logger.error(f"Audio Transcription Request failed with status code: {response.status_code}")
            raise FailedToTranscribeAudio(f"Audio Transcription Request failed with status code: {response.status_code}")
    
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        logger.error("Raw response:", response.text)
        raise FailedToTranscribeAudio(str(e))

    except Exception as e:
        logger.error(f"Failed to transcribe audio: {str(e)}")
        raise FailedToTranscribeAudio(str(e))
