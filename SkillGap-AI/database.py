"""
database.py
-----------
SQLite database layer for the AI-Powered Career Skill Gap Analyzer.

Stores:
- User accounts
- Resume analysis history
- Analysis scores and results
"""

import json
import os
import sqlite3
from datetime import datetime


# -------------------------------------------------------------------
# Database configuration
# -------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "career_analyzer.db")


# -------------------------------------------------------------------
# Connection
# -------------------------------------------------------------------

def get_connection():
    """
    Create and return a SQLite connection.

    Row factory allows rows to be accessed using column names.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10,
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign-key support.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# -------------------------------------------------------------------
# Database initialization
# -------------------------------------------------------------------

def init_db():
    """Create all required database tables."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # -----------------------------------------------------------
        # Users
        # -----------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        # -----------------------------------------------------------
        # Analysis history
        # -----------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                filename TEXT,
                target_job TEXT,
                job_description TEXT,

                readiness_score INTEGER DEFAULT 0,
                ats_score INTEGER DEFAULT 0,

                matched_skills TEXT,
                missing_skills TEXT,
                required_skills TEXT,

                suggestions TEXT,
                evidence TEXT,
                roadmap TEXT,
                resources TEXT,

                ai_summary TEXT,
                ai_strengths TEXT,
                ai_gaps TEXT,
                ai_recommendations TEXT,

                result_json TEXT,

                created_at TEXT NOT NULL,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
            """
        )

        # -----------------------------------------------------------
        # Indexes
        # -----------------------------------------------------------

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_users_email
            ON users(email)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_analyses_user
            ON analyses(user_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_analyses_created
            ON analyses(created_at)
            """
        )

        connection.commit()

    finally:
        connection.close()


# -------------------------------------------------------------------
# Utility functions
# -------------------------------------------------------------------

def _json_dumps(value):
    """Safely convert Python data to JSON text."""

    if value is None:
        return json.dumps([])

    try:
        return json.dumps(
            value,
            ensure_ascii=False,
        )
    except (TypeError, ValueError):
        return json.dumps([])


def _json_loads(value, default=None):
    """Safely convert JSON text back to Python data."""

    if default is None:
        default = []

    if not value:
        return default

    try:
        return json.loads(value)
    except (TypeError, ValueError, json.JSONDecodeError):
        return default


def _row_to_dict(row):
    """Convert sqlite3.Row to a normal dictionary."""

    if row is None:
        return None

    return dict(row)


# -------------------------------------------------------------------
# User functions
# -------------------------------------------------------------------

def create_user(name, email, password_hash):
    """
    Create a new user.

    Returns:
        user_id if successful
        None if the email already exists
    """

    name = (name or "").strip()
    email = (email or "").strip().lower()

    if not name or not email or not password_hash:
        return None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                name,
                email,
                password_hash,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                password_hash,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None

    finally:
        connection.close()


def get_user_by_email(email):
    """Return a user by email address."""

    email = (email or "").strip().lower()

    if not email:
        return None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            LIMIT 1
            """,
            (email,),
        )

        row = cursor.fetchone()

        return _row_to_dict(row)

    finally:
        connection.close()


def get_user_by_id(user_id):
    """Return a user by ID."""

    if not user_id:
        return None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE id = ?
            LIMIT 1
            """,
            (user_id,),
        )

        row = cursor.fetchone()

        return _row_to_dict(row)

    finally:
        connection.close()


# -------------------------------------------------------------------
# Analysis history
# -------------------------------------------------------------------

def save_analysis(
    user_id=None,
    filename="",
    target_job="",
    job_description="",
    result=None,
):
    """
    Save a completed resume analysis.

    The complete result dictionary is stored as result_json while
    commonly displayed fields are also stored separately for faster
    history-page access.
    """

    result = result or {}

    readiness_score = result.get(
        "readiness_score",
        result.get("career_readiness_score", 0),
    )

    ats_score = result.get(
        "ats_score",
        0,
    )

    matched_skills = result.get(
        "matched_skills",
        [],
    )

    missing_skills = result.get(
        "missing_skills",
        [],
    )

    required_skills = result.get(
        "required_skills",
        [],
    )

    suggestions = result.get(
        "suggestions",
        [],
    )

    evidence = result.get(
        "evidence",
        {},
    )

    roadmap = result.get(
        "roadmap",
        [],
    )

    resources = result.get(
        "resources",
        {},
    )

    ai_summary = result.get(
        "ai_summary",
        "",
    )

    ai_strengths = result.get(
        "ai_strengths",
        [],
    )

    ai_gaps = result.get(
        "ai_gaps",
        [],
    )

    ai_recommendations = result.get(
        "ai_recommendations",
        [],
    )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO analyses (
                user_id,
                filename,
                target_job,
                job_description,

                readiness_score,
                ats_score,

                matched_skills,
                missing_skills,
                required_skills,

                suggestions,
                evidence,
                roadmap,
                resources,

                ai_summary,
                ai_strengths,
                ai_gaps,
                ai_recommendations,

                result_json,
                created_at
            )
            VALUES (
                ?, ?, ?, ?,
                ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?
            )
            """,
            (
                user_id,
                filename or "",
                target_job or "",
                job_description or "",

                int(readiness_score or 0),
                int(ats_score or 0),

                _json_dumps(matched_skills),
                _json_dumps(missing_skills),
                _json_dumps(required_skills),

                _json_dumps(suggestions),
                _json_dumps(evidence),
                _json_dumps(roadmap),
                _json_dumps(resources),

                ai_summary or "",
                _json_dumps(ai_strengths),
                _json_dumps(ai_gaps),
                _json_dumps(ai_recommendations),

                _json_dumps(result),

                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def _restore_analysis(row):
    """
    Convert a database analysis row into a convenient dictionary.
    """

    if row is None:
        return None

    data = dict(row)

    # Restore JSON fields.
    json_fields = [
        "matched_skills",
        "missing_skills",
        "required_skills",
        "suggestions",
        "evidence",
        "roadmap",
        "resources",
        "ai_strengths",
        "ai_gaps",
        "ai_recommendations",
    ]

    for field in json_fields:
        if field in data:
            default = {}

            if field not in {
                "evidence",
                "resources",
            }:
                default = []

            data[field] = _json_loads(
                data[field],
                default=default,
            )

    # Restore the complete result object.
    if data.get("result_json"):
        data["result"] = _json_loads(
            data["result_json"],
            default={},
        )
    else:
        data["result"] = {}

    return data


def get_history(user_id, limit=100):
    """
    Return analysis history for a user.

    Newest analyses are returned first.
    """

    if not user_id:
        return []

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 100

    limit = max(1, min(limit, 500))

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM analyses
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (
                user_id,
                limit,
            ),
        )

        rows = cursor.fetchall()

        return [
            _restore_analysis(row)
            for row in rows
        ]

    finally:
        connection.close()


def get_analysis(analysis_id, user_id=None):
    """
    Return one analysis.

    If user_id is provided, the analysis must belong to that user.
    """

    if not analysis_id:
        return None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        if user_id is not None:
            cursor.execute(
                """
                SELECT *
                FROM analyses
                WHERE id = ?
                  AND user_id = ?
                LIMIT 1
                """,
                (
                    analysis_id,
                    user_id,
                ),
            )
        else:
            cursor.execute(
                """
                SELECT *
                FROM analyses
                WHERE id = ?
                LIMIT 1
                """,
                (analysis_id,),
            )

        row = cursor.fetchone()

        return _restore_analysis(row)

    finally:
        connection.close()


def delete_analysis(analysis_id, user_id=None):
    """
    Delete an analysis.

    If user_id is provided, only that user's analysis can be deleted.

    Returns:
        True if a row was deleted.
        False otherwise.
    """

    if not analysis_id:
        return False

    connection = get_connection()

    try:
        cursor = connection.cursor()

        if user_id is not None:
            cursor.execute(
                """
                DELETE FROM analyses
                WHERE id = ?
                  AND user_id = ?
                """,
                (
                    analysis_id,
                    user_id,
                ),
            )
        else:
            cursor.execute(
                """
                DELETE FROM analyses
                WHERE id = ?
                """,
                (analysis_id,),
            )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def get_analysis_count(user_id):
    """Return the number of analyses belonging to a user."""

    if not user_id:
        return 0

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM analyses
            WHERE user_id = ?
            """,
            (user_id,),
        )

        row = cursor.fetchone()

        return int(row["count"] or 0)

    finally:
        connection.close()


def get_latest_analysis(user_id):
    """Return the user's most recent analysis."""

    if not user_id:
        return None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM analyses
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT 1
            """,
            (user_id,),
        )

        row = cursor.fetchone()

        return _restore_analysis(row)

    finally:
        connection.close()


# -------------------------------------------------------------------
# Database initialization when running this file directly
# -------------------------------------------------------------------

if __name__ == "__main__":
    init_db()

    print("=" * 50)
    print("Career Skill Gap Analyzer Database")
    print("=" * 50)
    print(f"Database: {DATABASE_PATH}")
    print("Database initialized successfully.")
    print("=" * 50)