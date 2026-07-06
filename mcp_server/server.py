from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "medical-care-tools",
    instructions=(
        "Expose des outils pedagogiques pour un workflow academique "
        "d'orientation clinique preliminaire."
    ),
    host="127.0.0.1",
    port=9000,
    streamable_http_path="/mcp",
    stateless_http=True,
)


def _has_breathing_negation(text: str) -> bool:
    return (
        "pas de difficulte a respirer" in text
        or "pas de difficulte respiratoire" in text
        or "pas d'essoufflement" in text
    )


@mcp.tool()
def recommend_interim_care(patient_case: str, patient_answers: list[str]) -> str:
    """Produit une recommandation intermediaire prudente.

    Cette fonction est pedagogique et ne remplace pas une consultation medicale.
    """

    text = " ".join([patient_case, *patient_answers]).lower()
    red_flags = ["douleur thoracique", "malaise", "confusion", "perte de connaissance"]

    if any(flag in text for flag in red_flags) or (
        "difficulte a respirer" in text and not _has_breathing_negation(text)
    ):
        return (
            "Presence possible de signaux d'alerte. Recommandation prudente: "
            "consultation medicale rapide ou service d'urgence selon l'intensite des symptomes."
        )

    if "fievre" in text or "toux" in text:
        return (
            "Repos, hydratation, surveillance de la temperature et consultation rapide "
            "en cas d'aggravation ou de persistance des symptomes."
        )

    return (
        "Surveillance des symptomes, repos si necessaire, hydratation et avis medical "
        "si les symptomes persistent ou s'aggravent."
    )


app = mcp.streamable_http_app()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
