from typing import Annotated, Literal

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class MedicalState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    thread_id: str
    next: Literal["diagnostic_agent", "physician_review", "report_agent", "FINISH"]
    patient_case: str
    questions: list[str]
    patient_answers: list[str]
    question_count: int
    diagnostic_summary: str
    interim_care: str
    physician_treatment: str
    final_report: str
    needs_physician_review: bool