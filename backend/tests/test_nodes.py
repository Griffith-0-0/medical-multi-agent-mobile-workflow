from app.nodes.diagnostic_agent import diagnostic_agent_node
from app.nodes.report_agent import report_agent_node
from app.nodes.supervisor import supervisor_node


def test_supervisor_starts_with_diagnostic_agent():
    result = supervisor_node({})
    assert result["next"] == "diagnostic_agent"


def test_diagnostic_agent_adds_question():
    result = diagnostic_agent_node({
        "questions": [],
        "question_count": 0,
    })

    assert result["question_count"] == 1
    assert len(result["questions"]) == 1


def test_report_agent_generates_final_report():
    result = report_agent_node({
        "patient_case": "Patient avec toux",
        "diagnostic_summary": "Synthese test",
        "interim_care": "Repos",
        "physician_treatment": "Traitement test",
    })

    assert "Rapport final" in result["final_report"]
    assert "Ce systeme ne remplace pas une consultation medicale." in result["final_report"]