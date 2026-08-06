from typing import List, Optional
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    adapter_mode: str


class LabReportMeta(BaseModel):
    patient_name: Optional[str] = None
    age: Optional[str] = None
    sex: Optional[str] = None
    report_date: Optional[str] = None
    lab_name: Optional[str] = None
    reference_no: Optional[str] = None


class LabResultItem(BaseModel):
    test_name: str
    value: Optional[float] = None
    value_type: str  # numeric, qualitative, bounded_numeric, range, unparsed
    qualitative_value: Optional[str] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    flag: Optional[str] = None
    raw_line: str  # Preserved verbatim from OCR output


class DocumentExtractionResponse(BaseModel):
    is_lab_report: bool
    confidence: float
    meta: LabReportMeta
    results: List[LabResultItem]


class DocumentErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[str] = None
