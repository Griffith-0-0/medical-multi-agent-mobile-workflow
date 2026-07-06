import json
import os
import sqlite3
from pathlib import Path
from typing import Any


DB_PATH = Path(os.getenv("DATABASE_URL", "data/consultations.sqlite3"))


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS consultations (
                thread_id TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_consultation(thread_id: str, state: dict[str, Any]) -> None:
    state_json = json.dumps(state, ensure_ascii=False)
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO consultations (thread_id, state_json)
            VALUES (?, ?)
            ON CONFLICT(thread_id) DO UPDATE SET
                state_json = excluded.state_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (thread_id, state_json),
        )


def get_consultation_state(thread_id: str) -> dict[str, Any] | None:
    with _connect() as connection:
        row = connection.execute(
            "SELECT state_json FROM consultations WHERE thread_id = ?",
            (thread_id,),
        ).fetchone()

    if row is None:
        return None

    return json.loads(row["state_json"])
