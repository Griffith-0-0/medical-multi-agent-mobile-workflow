from app.state import MedicalState


def supervisor_node(state: MedicalState) -> dict:
    questions = state.get("questions", [])
    answers = state.get("patient_answers", [])

    if len(questions) > len(answers):
        return {"next": "FINISH"}

    if not state.get("diagnostic_summary"):
        return {"next": "diagnostic_agent"}

    if state.get("needs_physician_review") and not state.get("physician_treatment"):
        return {"next": "FINISH"}

    if not state.get("physician_treatment"):
        return {"next": "physician_review"}

    if not state.get("final_report"):
        return {"next": "report_agent"}

    return {"next": "FINISH"}