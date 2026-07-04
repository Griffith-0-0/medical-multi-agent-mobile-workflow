from app.graph import graph


def test_graph_generates_first_question():
    result = graph.invoke({
        "patient_case": "Patient avec toux et fievre",
        "questions": [],
        "patient_answers": [],
        "question_count": 0,
    })

    assert result["question_count"] == 1
    assert len(result["questions"]) == 1
    assert result["next"] == "FINISH"