import os
from typing import Dict, List

import httpx
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

DISCLAIMER = "Ce systeme ne remplace pas une consultation medicale."


def _answers_as_text(answers: List[str]) -> str:
    if not answers:
        return "Aucune reponse patient fournie."

    return "\n".join(f"{index + 1}. {answer}" for index, answer in enumerate(answers))


def _call_ollama(prompt: str) -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.2")

    response = httpx.post(
        f"{base_url}/api/chat",
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant IA dans un projet academique de simulation "
                        "d'orientation clinique preliminaire. Tu ne fournis jamais de "
                        "diagnostic definitif, tu ne remplaces pas un medecin, et tu "
                        "formules uniquement des syntheses prudentes destinees a etre "
                        "validees par un professionnel de sante."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"].strip()


def _generate_with_llm(prompt: str, fallback: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "fallback").lower()

    if provider == "ollama":
        try:
            return _call_ollama(prompt)
        except Exception:
            return fallback

    return fallback


def generate_diagnostic_summary(patient_case: str, patient_answers: List[str]) -> str:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "Tu aides a produire une synthese clinique preliminaire pour un TP. "
                    "Tu dois rester prudent, ne pas donner de diagnostic definitif, "
                    "et recommander une validation par un medecin."
                ),
            ),
            (
                "user",
                (
                    "Cas initial:\n{patient_case}\n\n"
                    "Reponses patient:\n{patient_answers}\n\n"
                    "Redige une synthese courte avec ces sections:\n"
                    "- Elements rapportes\n"
                    "- Points de vigilance\n"
                    "- Orientation preliminaire prudente"
                ),
            ),
        ]
    )
    prompt = prompt_template.format(
        patient_case=patient_case,
        patient_answers=_answers_as_text(patient_answers),
    )
    fallback = (
        "Elements rapportes: le patient presente les elements decrits dans le cas initial "
        "et les reponses collectees pendant l'entretien. "
        f"Cas initial: {patient_case}. "
        f"Reponses patient: {_answers_as_text(patient_answers)}. "
        "Points de vigilance: surveiller l'evolution des symptomes et rechercher toute aggravation. "
        "Orientation preliminaire prudente: une revue par un medecin est necessaire avant toute conduite definitive."
    )

    return _generate_with_llm(prompt, fallback)


def generate_final_report(state: Dict) -> str:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "Tu generes un rapport academique d'orientation clinique preliminaire. "
                    "Le rapport doit etre clair, structure, prudent, et ne doit jamais remplacer "
                    "une consultation medicale."
                ),
            ),
            (
                "user",
                (
                    "Cas initial:\n{patient_case}\n\n"
                    "Synthese preliminaire:\n{diagnostic_summary}\n\n"
                    "Recommandation intermediaire:\n{interim_care}\n\n"
                    "Revue medecin:\n{physician_treatment}\n\n"
                    "Redige un rapport final concis avec les sections: "
                    "Cas initial, Synthese, Recommandation intermediaire, Revue medecin, Avertissement."
                ),
            ),
        ]
    )
    prompt = prompt_template.format(
        patient_case=state.get("patient_case", ""),
        diagnostic_summary=state.get("diagnostic_summary", ""),
        interim_care=state.get("interim_care", ""),
        physician_treatment=state.get("physician_treatment", ""),
    )
    fallback = f"""
# Rapport final d'orientation clinique preliminaire

## Cas initial
{state.get("patient_case", "")}

## Synthese clinique preliminaire
{state.get("diagnostic_summary", "")}

## Recommandation intermediaire
{state.get("interim_care", "")}

## Revue du medecin
{state.get("physician_treatment", "")}

## Avertissement
{DISCLAIMER}
"""

    report = _generate_with_llm(prompt, fallback.strip())

    if "Rapport final" not in report:
        report = f"# Rapport final d'orientation clinique preliminaire\n\n{report.lstrip()}"

    if DISCLAIMER not in report:
        report = f"{report.rstrip()}\n\n## Avertissement\n{DISCLAIMER}"

    return report
