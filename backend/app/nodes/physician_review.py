from app.state import MedicalState


def physician_review_node(state: MedicalState) -> dict:
    return {
        "needs_physician_review": True,
    }