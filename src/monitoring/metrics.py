import sqlite3
import uuid
import pandas as pd

from datetime import datetime

DB = "metrics.db"


def log_request(
    question,
    latency,
    retrieval_latency,
    llm_latency,
):
    init_db()  # Ensure the database and table are initialized
    request_id = str(uuid.uuid4())

    conn = sqlite3.connect(DB)

    conn.execute(
        """
        INSERT INTO metrics
        (
            id,
            timestamp,
            question,
            latency,
            retrieval_latency,
            llm_latency,
            feedback
        )
        VALUES (?, ?, ?, ?, ?, ?, NULL)
        """,
        (
            request_id,
            datetime.now().isoformat(),
            question,
            latency,
            retrieval_latency,
            llm_latency,
        ),
    )

    conn.commit()
    conn.close()

    return request_id


def save_feedback(request_id: str, feedback: str):
    conn = sqlite3.connect(DB)

    conn.execute(
        """
        UPDATE metrics
        SET feedback = ?
        WHERE id = ?
        """,
        (
            feedback,
            request_id,
        ),
    )

    conn.commit()
    conn.close()

def get_metrics():
    init_db()  # Ensure the database and table are initialized
    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM metrics",
        conn,
    )

    conn.close()

    return df.to_dict(orient="records")

def init_db():
    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            question TEXT NOT NULL,
            latency REAL NOT NULL,
            retrieval_latency REAL NOT NULL,
            llm_latency REAL NOT NULL,
            feedback TEXT
        )
    """)

    conn.commit()
    conn.close()