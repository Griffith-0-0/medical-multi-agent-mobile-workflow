from typing import List

from app.tools.mcp_client import call_mcp_tool


def _fallback_interim_care(patient_case: str, patient_answers: List[str]) -> str:
    text = " ".join([patient_case, *patient_answers]).lower()
    has_breathing_negation = (
        "pas de difficulte a respirer" in text
        or "pas de difficulte respiratoire" in text
        or "pas d'essoufflement" in text
    )

    if "douleur thoracique" in text or "malaise" in text or (
        "difficulte a respirer" in text and not has_breathing_negation
    ):
        return (
            "Presence possible de signaux d'alerte. Recommandation prudente: "
            "consultation medicale rapide ou service d'urgence selon l'intensite des symptomes."
        )

    return "Repos, hydratation, surveillance et consultation rapide en cas d'aggravation."


def recommend_interim_care(patient_case: str, patient_answers: List[str]) -> str:
    try:
        return call_mcp_tool(
            "recommend_interim_care",
            {
                "patient_case": patient_case,
                "patient_answers": patient_answers,
            },
        )
    except Exception:
        return _fallback_interim_care(patient_case, patient_answers)
