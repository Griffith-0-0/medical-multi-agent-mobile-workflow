from uuid import uuid4

from fastapi import FastAPI, HTTPException

from app.graph import graph
from app.schemas.consultation import ResumeConsultationRequest, StartConsultationRequest

app = FastAPI(title="Medical Multi-Agent Workflow")

SESSIONS = {}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/sessions/start")
def start_session():
    thread_id = str(uuid4())
    SESSIONS[thread_id] = {"thread_id": thread_id}
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
    SESSIONS[thread_id] = result
    return result


@app.post("/consultation/resume")
def resume_consultation(payload: ResumeConsultationRequest):
    state = SESSIONS.get(payload.thread_id)

    if not state:
        raise HTTPException(status_code=404, detail="Consultation introuvable")

    if payload.patient_answer:
        answers = state.get("patient_answers", [])
        state["patient_answers"] = answers + [payload.patient_answer]

    if payload.physician_treatment:
        state["physician_treatment"] = payload.physician_treatment
        state["needs_physician_review"] = False

    result = graph.invoke(state)
    SESSIONS[payload.thread_id] = result
    return result


@app.get("/consultation/{thread_id}")
def get_consultation(thread_id: str):
    state = SESSIONS.get(thread_id)

    if not state:
        raise HTTPException(status_code=404, detail="Consultation introuvable")

    return state


@app.get("/consultation/{thread_id}/report")
def get_report(thread_id: str):
    state = SESSIONS.get(thread_id)

    if not state:
        raise HTTPException(status_code=404, detail="Consultation introuvable")

    return {"final_report": state.get("final_report")}


