from io import BytesIO
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def build_report_pdf(state: dict[str, Any]) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4, title="Rapport final")
    styles = getSampleStyleSheet()
    story = []

    sections = [
        ("Rapport final d'orientation clinique preliminaire", None),
        ("Cas initial", state.get("patient_case", "")),
        ("Synthese clinique preliminaire", state.get("diagnostic_summary", "")),
        ("Recommandation intermediaire", state.get("interim_care", "")),
        ("Revue du medecin", state.get("physician_treatment", "")),
        ("Avertissement", "Ce systeme ne remplace pas une consultation medicale."),
    ]

    for title, body in sections:
        story.append(Paragraph(title, styles["Heading1" if body is None else "Heading2"]))
        if body:
            story.append(Paragraph(str(body).replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 12))

    document.build(story)
    return buffer.getvalue()
