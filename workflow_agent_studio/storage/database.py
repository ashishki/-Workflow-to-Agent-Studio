"""SQLite database setup."""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect_database(path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    _ensure_source_metadata_column(connection)


def _ensure_source_metadata_column(connection: sqlite3.Connection) -> None:
    columns = {
        row[1] for row in connection.execute("PRAGMA table_info(source_documents)").fetchall()
    }
    if "metadata_json" not in columns:
        connection.execute(
            "ALTER TABLE source_documents ADD COLUMN metadata_json TEXT NOT NULL DEFAULT '{}'"
        )
        connection.commit()
