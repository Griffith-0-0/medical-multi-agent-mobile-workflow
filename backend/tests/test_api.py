from app.api import app

try:
    from fastapi.testclient import TestClient
except ImportError:
    from starlette.testclient import TestClient


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_consultation_start_returns_first_question():
    response = client.post(
        "/consultation/start",
        json={"patient_case": "Patient avec toux et fievre"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["thread_id"]
    assert data["question_count"] == 1
    assert len(data["questions"]) == 1
    assert data["next"] == "FINISH"


def test_full_consultation_workflow():
    start_response = client.post(
        "/consultation/start",
        json={"patient_case": "Patient de 28 ans avec toux et fievre depuis 2 jours"},
    )
    state = start_response.json()
    thread_id = state["thread_id"]

    patient_answers = [
        "Depuis 2 jours.",
        "Oui, fievre moderee autour de 38 degres.",
        "Non, pas de douleur importante.",
        "Non, pas de difficulte a respirer ni malaise.",
        "Aucun antecedent medical important.",
    ]

    for answer in patient_answers:
        response = client.post(
            "/consultation/resume",
            json={
                "thread_id": thread_id,
                "patient_answer": answer,
            },
        )
        assert response.status_code == 200
        state = response.json()

    assert state["needs_physician_review"] is True
    assert state["diagnostic_summary"]
    assert state["interim_care"]

    review_response = client.post(
        "/consultation/resume",
        json={
            "thread_id": thread_id,
            "physician_treatment": (
                "Repos, hydratation, surveillance de la temperature "
                "et consultation si aggravation."
            ),
        },
    )

    assert review_response.status_code == 200
    final_state = review_response.json()

    assert final_state["final_report"]
    assert "Ce systeme ne remplace pas une consultation medicale." in final_state["final_report"]