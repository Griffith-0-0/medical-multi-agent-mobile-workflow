from langgraph.graph import END, START, StateGraph

from app.nodes.diagnostic_agent import diagnostic_agent_node
from app.nodes.physician_review import physician_review_node
from app.nodes.report_agent import report_agent_node
from app.nodes.supervisor import supervisor_node
from app.state import MedicalState


def route_from_supervisor(state: MedicalState) -> str:
    next_step = state.get("next")

    if next_step == "diagnostic_agent":
        return "diagnostic_agent"

    if next_step == "physician_review":
        return "physician_review"

    if next_step == "report_agent":
        return "report_agent"

    return END


def build_graph():
    builder = StateGraph(MedicalState)

    builder.add_node("supervisor", supervisor_node)
    builder.add_node("diagnostic_agent", diagnostic_agent_node)
    builder.add_node("physician_review", physician_review_node)
    builder.add_node("report_agent", report_agent_node)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges("supervisor", route_from_supervisor)
    builder.add_edge("diagnostic_agent", "supervisor")
    builder.add_edge("physician_review", "supervisor")
    builder.add_edge("report_agent", "supervisor")

    return builder.compile()


graph = build_graph()