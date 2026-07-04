# Rapport technique - Medical Multi-Agent Mobile Workflow

## 1. Contexte

Ce projet est une application academique simulant un workflow d'orientation clinique preliminaire avec une architecture multi-agents.

L'application ne constitue pas un dispositif medical. Elle ne fournit pas de diagnostic definitif et doit toujours afficher l'avertissement suivant :

```text
Ce systeme ne remplace pas une consultation medicale.
```

## 2. Objectifs

Les objectifs principaux sont :

- modeliser un workflow multi-agents avec LangGraph ;
- gerer un etat partage entre agents ;
- integrer un LLM compatible via LangChain et Ollama ;
- ajouter une etape Human-in-the-Loop pour la revue medecin ;
- exposer le workflow via FastAPI ;
- utiliser un outil externe via MCP ;
- connecter le backend a une application mobile React Native ;
- tester le workflow avec Pytest et LangGraph Studio.

## 3. Architecture globale

Le systeme est compose de quatre parties :

```text
frontend/     Application mobile React Native avec Expo
backend/      API FastAPI + workflow LangGraph
mcp_server/   Serveur d'outil externe pour la recommandation intermediaire
docs/         Documentation technique et support de demonstration
```

Flux principal :

```text
Utilisateur mobile
    -> FastAPI
    -> LangGraph Supervisor
    -> Diagnostic Agent
    -> LLM Ollama pour la synthese
    -> MCP tool pour la recommandation
    -> Physician Review
    -> Report Agent
    -> LLM Ollama pour le rapport final
    -> Application mobile
```

## 4. Etat partage LangGraph

Le workflow utilise `MedicalState`, defini dans `backend/app/state.py`.

Champs principaux :

- `thread_id` : identifiant de consultation ;
- `patient_case` : cas initial saisi par l'utilisateur ;
- `questions` : questions posees au patient ;
- `patient_answers` : reponses patient ;
- `question_count` : nombre de questions posees ;
- `diagnostic_summary` : synthese clinique preliminaire ;
- `interim_care` : recommandation intermediaire ;
- `physician_treatment` : conduite a tenir saisie par le medecin ;
- `final_report` : rapport final ;
- `needs_physician_review` : marqueur d'attente de revue humaine ;
- `next` : prochaine etape du graphe.

## 5. Agents

### Supervisor

Le `Supervisor` decide la prochaine etape.

Il arrete temporairement le workflow :

- quand une question patient attend une reponse ;
- quand la revue medecin est requise.

Ces arrets representent le Human-in-the-Loop.

### Diagnostic Agent

Le `Diagnostic Agent` :

1. pose 5 questions au patient ;
2. attend les reponses ;
3. genere une synthese clinique preliminaire via LLM ;
4. appelle un outil MCP pour obtenir une recommandation intermediaire.

Les questions patient sont definies dans `backend/app/tools/patient_tools.py`.

### Physician Review

Le noeud `Physician Review` marque l'etape ou un medecin doit intervenir manuellement.

Cette etape est obligatoire pour eviter que le systeme produise directement une conduite finale sans validation humaine.

### Report Agent

Le `Report Agent` genere le rapport final avec un prompt LLM.

Le rapport contient :

- le cas initial ;
- la synthese clinique preliminaire ;
- la recommandation intermediaire ;
- la revue du medecin ;
- l'avertissement ethique obligatoire.

## 6. Integration LLM

Le projet utilise `LangChain` pour construire les prompts et `Ollama` comme fournisseur LLM local.

Configuration :

```text
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

Le module `backend/app/llm.py` contient :

- `generate_diagnostic_summary` ;
- `generate_final_report` ;
- un fallback prudent si le LLM est indisponible.

Le fallback permet de garder l'application fonctionnelle pendant une demonstration ou pendant les tests.

## 7. Integration MCP

Le TP demande l'integration d'au moins un outil via MCP.

Dans ce projet, l'outil expose est :

```text
recommend_interim_care
```

Il recoit :

- `patient_case` ;
- `patient_answers`.

Il retourne une recommandation intermediaire prudente.

Fichiers concernes :

```text
mcp_server/server.py
backend/app/tools/mcp_client.py
backend/app/tools/care_tools.py
```

Le serveur MCP utilise une interface JSON-RPC avec les methodes :

- `initialize` ;
- `tools/list` ;
- `tools/call`.

Note : le SDK MCP officiel n'a pas ete utilise car l'environnement local est en Python 3.9. Le projet fournit donc une implementation JSON-RPC simple, compatible avec l'esprit MCP et suffisante pour demontrer l'appel d'un outil externe.

## 8. API FastAPI

L'API est definie dans `backend/app/api.py`.

Endpoints :

```text
GET  /health
POST /sessions/start
POST /consultation/start
POST /consultation/resume
GET  /consultation/{thread_id}
GET  /consultation/{thread_id}/report
```

Le stockage utilise actuellement un dictionnaire en memoire :

```python
SESSIONS = {}
```

Cela simplifie le TP, mais les donnees disparaissent au redemarrage du serveur.

## 9. Application mobile

Le frontend est une application React Native avec Expo.

Ecrans :

- `PatientCaseScreen` : saisie du cas initial ;
- `PatientQuestionsScreen` : reponses aux 5 questions ;
- `PhysicianReviewScreen` : validation medecin ;
- `FinalReportScreen` : affichage du rapport final.

Le frontend appelle FastAPI via `frontend/src/api/consultationApi.ts`.

## 10. Tests

Les tests sont situes dans `backend/tests/`.

Ils couvrent :

- les tools patient ;
- les noeuds LangGraph ;
- le graphe ;
- l'API FastAPI ;
- le fallback du tool MCP.

Commande :

```bash
cd backend
../.venv/bin/python -m pytest
```

Les tests forcent `LLM_PROVIDER=fallback` afin d'eviter des appels LLM longs ou non deterministes.

## 11. LangGraph Studio

Le fichier `backend/langgraph.json` expose le graphe :

```json
{
  "dependencies": ["."],
  "graphs": {
    "medical_workflow": "./app/graph.py:graph"
  },
  "env": ".env"
}
```

LangGraph Studio permet de visualiser :

- les noeuds ;
- les transitions ;
- les arrets temporaires ;
- l'etat partage ;
- la progression du workflow.

## 12. Choix techniques

### Pourquoi LangGraph ?

LangGraph permet de representer explicitement le workflow sous forme de graphe. Il est adapte aux systemes multi-agents avec etat partage et transitions conditionnelles.

### Pourquoi FastAPI ?

FastAPI permet d'exposer le graphe via une API REST claire, testable et documentee automatiquement avec Swagger.

### Pourquoi React Native ?

React Native permet de transformer le TP en application mobile, ce qui rend le projet plus concret et valorisable.

### Pourquoi Ollama ?

Ollama permet d'executer un LLM localement, sans dependance a une cle API externe.

### Pourquoi MCP ?

MCP separe les capacites du LLM et les outils externes. Le LLM genere du texte, tandis que le tool MCP fournit une recommandation intermediaire structuree.

## 13. Limites

- Pas de persistance en base de donnees.
- Pas d'authentification medecin.
- MCP implemente en JSON-RPC simple, pas avec le SDK officiel.
- Le systeme ne doit pas etre considere comme un outil medical.
- Les recommandations restent pedagogiques et prudentes.

## 14. Ameliorations futures

- Migrer vers Python 3.11.
- Utiliser le SDK MCP officiel.
- Ajouter PostgreSQL ou SQLite.
- Ajouter export PDF.
- Ajouter Docker Compose.
- Ajouter historique des consultations.
- Ajouter authentification et roles patient/medecin.
- Ajouter captures d'ecran et video de demonstration.

## 15. Conclusion

Le projet respecte les principaux objectifs du TP :

- workflow multi-agents LangGraph ;
- etat partage ;
- Human-in-the-Loop ;
- LLM compatible ;
- outil MCP ;
- API FastAPI ;
- frontend mobile ;
- tests automatises ;
- configuration LangGraph Studio.

Il constitue une base solide pour un projet portfolio oriente IA agentique, backend API et mobile.
