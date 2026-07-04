# Demo LangGraph Studio

## Objectif

Visualiser le workflow multi-agents dans LangGraph Studio et observer les transitions entre les noeuds.

## Commande

Depuis le dossier `backend/` :

```bash
langgraph dev
```

Si la commande `langgraph` n'est pas disponible :

```bash
../.venv/bin/python -m langgraph dev
```

## Graphe expose

Le fichier `backend/langgraph.json` expose :

```text
medical_workflow -> ./app/graph.py:graph
```

## State initial pour tester

```json
{
  "patient_case": "Patient de 28 ans avec toux, fievre moderee et fatigue depuis 2 jours.",
  "questions": [],
  "patient_answers": [],
  "question_count": 0
}
```

## Ce qu'il faut montrer

1. `START -> supervisor`
2. `supervisor -> diagnostic_agent`
3. `diagnostic_agent` pose une question.
4. Le graphe s'arrete avec `next = FINISH` pour attendre la reponse patient.
5. Apres 5 reponses, `diagnostic_agent` genere une synthese avec le LLM.
6. Le tool MCP genere la recommandation intermediaire.
7. `physician_review` marque l'attente de validation medecin.
8. Apres validation, `report_agent` genere le rapport final.

## Note importante

Le workflow contient des arrets temporaires volontaires :

- apres chaque question patient ;
- avant la revue medecin.

C'est le comportement attendu pour representer le Human-in-the-Loop.
