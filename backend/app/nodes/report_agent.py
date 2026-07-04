from app.state import MedicalState
from app.llm import generate_final_report


def report_agent_node(state: MedicalState) -> dict:
    report = generate_final_report(state)

    return {
        "final_report": report,
        "needs_physician_review": False,
    }
