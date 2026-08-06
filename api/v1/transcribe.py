from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from adapters.stt.factory import get_stt_adapter
from api.schemas import TranscriptionResponse
from services.transcription_service import TranscriptionService

router = APIRouter()

MAX_AUDIO_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB
ALLOWED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
ALLOWED_LANGUAGES = {"bn", "en", "auto"}


@router.post(
    "/transcribe",
    response_model=TranscriptionResponse,
    status_code=status.HTTP_200_OK,
)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form("auto"),
) -> TranscriptionResponse:
    filename = file.filename or "audio.wav"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "UNSUPPORTED_FILE_FORMAT",
                "message": f"Unsupported audio file format '{ext}'. Allowed: {', '.join(sorted(ALLOWED_AUDIO_EXTENSIONS))}",
            },
        )

    lang = language.lower().strip() if language else "auto"
    if lang not in ALLOWED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "INVALID_LANGUAGE_PARAMETER",
                "message": f"Unsupported language '{language}'. Allowed values: bn, en, auto",
            },
        )

    audio_bytes = await file.read()
    if len(audio_bytes) > MAX_AUDIO_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error": "FILE_TOO_LARGE",
                "message": f"Audio file size exceeds maximum limit of 25 MB ({len(audio_bytes)} bytes uploaded).",
            },
        )

    stt_adapter = get_stt_adapter()
    service = TranscriptionService(stt_adapter=stt_adapter)
    result = service.transcribe_audio(
        audio_bytes=audio_bytes, filename=filename, language=lang
    )

    return TranscriptionResponse(**result)
