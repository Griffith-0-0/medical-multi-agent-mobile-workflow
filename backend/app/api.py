import os
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, Response

from app.db import get_consultation_state, init_db, save_consultation
from app.graph import graph
from app.pdf import build_report_pdf
from app.schemas.consultation import ResumeConsultationRequest, StartConsultationRequest

app = FastAPI(title="Medical Multi-Agent Workflow")

init_db()


def _require_physician_token(token: str | None) -> None:
    expected_token = os.getenv("PHYSICIAN_REVIEW_TOKEN", "demo-physician-token")

    if token != expected_token:
        raise HTTPException(status_code=401, detail="Token medecin invalide")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/sessions/start")
def start_session():
    thread_id = str(uuid4())
    save_consultation(thread_id, {"thread_id": thread_id})
    return {"thread_id": thread_id}


@app.post("/consultation/start")
def start_consultation(payload: StartConsultationRequest):
    thread_id = str(uuid4())
    initial_state = {
        "thread_id": thread_id,
        "patient_case": payload.patient_case,
        "questions": [],
        "patient_answers": [],
        "question_count": 0,
    }

    result = graph.invoke(initial_state)
    save_consultation(thread_id, result)
    return result


@app.post("/consultation/resume")
def resume_consultation(
    payload: ResumeConsultationRequest,
    x_physician_token: str | None = Header(default=None),
):
    state = get_consultation_state(payload.thread_id)

    if not state:
        raise HTTPException(status_code=404, detail="Consultation introuvable")

    if payload.patient_answer:
        answers = state.get("patient_answers", [])
        state["patient_answers"] = answers + [payload.patient_answer]

    if payload.physician_treatment:
        _require_physician_token(x_physician_token)
        state["physician_treatment"] = payload.physician_treatment
        state["needs_physician_review"] = False

    result = graph.invoke(state)
    save_consultation(payload.thread_id, result)
    return result


@app.get("/consultation/{thread_id}")
def get_consultation(thread_id: str):
    state = get_consultation_state(thread_id)

    if not state:
        raise HTTPException(status_code=404, detail="Consultation introuvable")

    return state


@app.get("/consultation/{thread_id}/report")
def get_report(thread_id: str):
    state = get_consultation_state(thread_id)

    if not state:
        raise HTTPException(status_code=404, detail="Consultation introuvable")

    return {"final_report": state.get("final_report")}


@app.get("/consultation/{thread_id}/report/pdf")
def get_report_pdf(thread_id: str):
    state = get_consultation_state(thread_id)

    if not state:
        raise HTTPException(status_code=404, detail="Consultation introuvable")

    if not state.get("final_report"):
        raise HTTPException(status_code=400, detail="Rapport final indisponible")

    pdf_bytes = build_report_pdf(state)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="rapport-{thread_id}.pdf"',
        },
    )

