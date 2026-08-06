from fastapi import APIRouter, File, HTTPException, UploadFile, status

from adapters.ocr.factory import get_ocr_adapter
from api.schemas import DocumentExtractionResponse
from services.extraction_service import DocumentExtractionService

router = APIRouter()

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".pdf"}


@router.post(
    "/documents/extract",
    response_model=DocumentExtractionResponse,
    status_code=status.HTTP_200_OK,
)
async def extract_document(file: UploadFile = File(...)) -> DocumentExtractionResponse:
    filename = file.filename or "upload.jpg"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "UNSUPPORTED_FILE_FORMAT",
                "message": f"Unsupported file extension '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            },
        )

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error": "FILE_TOO_LARGE",
                "message": f"File size exceeds maximum limit of 25 MB ({len(file_bytes)} bytes uploaded).",
            },
        )

    ocr_adapter = get_ocr_adapter()
    service = DocumentExtractionService(ocr_adapter=ocr_adapter)
    result = service.extract_document(file_bytes, filename)

    if not result.get("is_lab_report", False):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": result.get("error", "NOT_A_LAB_REPORT"),
                "message": result.get("message", "Uploaded document is not a medical lab report."),
                "confidence": result.get("confidence", 0.0),
            },
        )

    return DocumentExtractionResponse(**result)
