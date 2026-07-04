from app.tools.care_tools import recommend_interim_care


def test_recommend_interim_care_fallback_for_simple_case(monkeypatch):
    monkeypatch.setenv("MCP_SERVER_URL", "http://localhost:9999/mcp")

    result = recommend_interim_care(
        "Patient avec toux et fievre",
        ["Depuis 2 jours", "Pas de difficulte a respirer"],
    )

    assert "Repos" in result


def test_recommend_interim_care_fallback_for_red_flags(monkeypatch):
    monkeypatch.setenv("MCP_SERVER_URL", "http://localhost:9999/mcp")

    result = recommend_interim_care(
        "Patient avec douleur thoracique",
        ["Malaise", "Difficulte a respirer"],
    )

    assert "signaux d'alerte" in result
