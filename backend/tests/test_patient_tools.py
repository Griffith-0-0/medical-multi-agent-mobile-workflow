from app.tools.patient_tools import (
    DEFAULT_QUESTIONS,
    get_next_patient_question,
    has_completed_patient_questions,
)


def test_default_questions_count():
    assert len(DEFAULT_QUESTIONS) == 5


def test_get_next_patient_question_returns_question():
    assert get_next_patient_question(0) == DEFAULT_QUESTIONS[0]
    assert get_next_patient_question(4) == DEFAULT_QUESTIONS[4]


def test_get_next_patient_question_returns_none_after_five_questions():
    assert get_next_patient_question(5) is None


def test_has_completed_patient_questions():
    assert has_completed_patient_questions(0) is False
    assert has_completed_patient_questions(4) is False
    assert has_completed_patient_questions(5) is True