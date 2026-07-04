from app.state import MedicalState
from app.llm import generate_diagnostic_summary
from app.tools.care_tools import recommend_interim_care
from app.tools.patient_tools import get_next_patient_question, has_completed_patient_questions


def diagnostic_agent_node(state: MedicalState) -> dict:
    question_count = state.get("question_count", 0)
    questions = state.get("questions", [])

    if not has_completed_patient_questions(question_count):
        next_question = get_next_patient_question(question_count)
        return {
            "questions": questions + [next_question],
            "question_count": question_count + 1,
        }

    answers = state.get("patient_answers", [])
    summary = generate_diagnostic_summary(state.get("patient_case", ""), answers)
    interim_care = recommend_interim_care(state.get("patient_case", ""), answers)

    return {
        "diagnostic_summary": summary,
        "interim_care": interim_care,
    }
