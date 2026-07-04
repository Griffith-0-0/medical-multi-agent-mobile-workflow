from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Medical MCP Server")


class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    method: str
    params: Dict[str, Any] = {}


def recommend_interim_care(patient_case: str, patient_answers: List[str]) -> str:
    text = " ".join([patient_case, *patient_answers]).lower()
    has_breathing_negation = (
        "pas de difficulte a respirer" in text
        or "pas de difficulte respiratoire" in text
        or "pas d'essoufflement" in text
    )

    red_flags = ["douleur thoracique", "malaise", "confusion", "perte de connaissance"]

    if any(flag in text for flag in red_flags) or (
        "difficulte a respirer" in text and not has_breathing_negation
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


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "medical-mcp-server"}


@app.post("/mcp")
def handle_mcp_request(request: JsonRpcRequest):
    if request.method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "medical-care-tools",
                    "version": "1.0.0",
                },
                "capabilities": {
                    "tools": {},
                },
            },
        }

    if request.method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {
                "tools": [
                    {
                        "name": "recommend_interim_care",
                        "description": (
                            "Produit une recommandation intermediaire prudente a partir "
                            "du cas initial et des reponses patient."
                        ),
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "patient_case": {"type": "string"},
                                "patient_answers": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                            },
                            "required": ["patient_case", "patient_answers"],
                        },
                    }
                ]
            },
        }

    if request.method == "tools/call":
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})

        if tool_name != "recommend_interim_care":
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {
                    "code": -32601,
                    "message": f"Tool inconnu: {tool_name}",
                },
            }

        recommendation = recommend_interim_care(
            patient_case=arguments.get("patient_case", ""),
            patient_answers=arguments.get("patient_answers", []),
        )
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": recommendation,
                    }
                ]
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "error": {
            "code": -32601,
            "message": f"Methode inconnue: {request.method}",
        },
    }
