from typing import Optional

from pydantic import BaseModel


class StartConsultationRequest(BaseModel):
    patient_case: str


class ResumeConsultationRequest(BaseModel):
    thread_id: str
    patient_answer: Optional[str] = None
    physician_treatment: Optional[str] = None