from typing import Optional


DEFAULT_QUESTIONS = [
    "Depuis quand les symptomes ont-ils commence ?",
    "Avez-vous de la fievre ?",
    "Ressentez-vous une douleur importante ?",
    "Avez-vous des difficultes a respirer ou un malaise ?",
    "Avez-vous des antecedents medicaux importants ?",
]


def get_next_patient_question(question_count: int) -> Optional[str]:
    if question_count >= len(DEFAULT_QUESTIONS):
        return None

    return DEFAULT_QUESTIONS[question_count]


def has_completed_patient_questions(question_count: int) -> bool:
    return question_count >= len(DEFAULT_QUESTIONS)