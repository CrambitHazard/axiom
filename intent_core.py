"""
Core functionality for Axiom intent system.

Shared utilities for finding repo root, managing database schema,
and initializing the .intent/ directory structure.
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def find_repo_root(start_path: Path) -> Path:
    """
    Walk up directories until .git is found.

    Args:
        start_path: The starting directory path to search from.

    Returns:
        The repository root directory path.

    Raises:
        SystemExit: If .git directory is not found.
    """
    current = start_path.resolve()

    while current != current.parent:
        git_dir = current / '.git'
        if git_dir.exists() and git_dir.is_dir():
            return current
        current = current.parent

    sys.exit("ERROR: .git directory not found. Not in a git repository.")


def get_intent_dir() -> Path:
    """
    Get the .intent directory path for the current repo.

    Returns:
        Path to .intent directory.

    Raises:
        SystemExit: If not in a git repository.
    """
    repo_root = find_repo_root(Path.cwd())
    return repo_root / '.intent'


def create_database_schema(db_path: Path) -> None:
    """
    Create SQLite database with intents, assumptions, and decisions tables.

    Args:
        db_path: Path to the intent.db file.
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intents (
            id TEXT PRIMARY KEY,
            title TEXT,
            problem TEXT,
            context TEXT,
            constraints TEXT,
            status TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assumptions (
            id TEXT PRIMARY KEY,
            intent_id TEXT,
            statement TEXT,
            confidence REAL,
            risk_if_false TEXT,
            created_at TEXT,
            last_validated_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id TEXT PRIMARY KEY,
            intent_id TEXT,
            summary TEXT,
            rationale TEXT,
            alternatives TEXT,
            tradeoffs TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def ensure_database_schema(db_path: Path) -> None:
    """
    Ensure database exists with correct schema.

    Args:
        db_path: Path to the intent.db file.

    Raises:
        SystemExit: If database creation fails or schema mismatch detected.
    """
    if not db_path.exists():
        create_database_schema(db_path)
    else:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('intents', 'assumptions', 'decisions')
        """)
        existing_tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        required_tables = {'intents', 'assumptions', 'decisions'}
        if existing_tables != required_tables:
            missing = required_tables - existing_tables
            extra = existing_tables - required_tables
            error_msg = "ERROR: Database schema mismatch detected.\n"
            if missing:
                error_msg += f"  Missing tables: {', '.join(missing)}\n"
            if extra:
                error_msg += f"  Unexpected tables: {', '.join(extra)}\n"
            error_msg += "\n"
            error_msg += "This indicates a schema version conflict.\n"
            error_msg += "Do not attempt automatic migration.\n"
            error_msg += "Manual intervention required.\n"
            error_msg += "\n"
            error_msg += "If you need to reset, backup your data and delete intent.db"
            sys.exit(error_msg)


def ensure_meta_json(intent_dir: Path, repo_root: Path) -> None:
    """
    Ensure meta.json exists with correct structure.

    Args:
        intent_dir: Path to .intent directory.
        repo_root: Path to repository root.

    Raises:
        SystemExit: If meta.json creation fails.
    """
    meta_json = intent_dir / 'meta.json'

    needs_init = False
    if not meta_json.exists():
        needs_init = True
    else:
        try:
            content = meta_json.read_text(encoding='utf-8').strip()
            if not content:
                needs_init = True
            else:
                data = json.loads(content)
                required_fields = ["repo_path", "created_at", "schema_version"]
                if not all(field in data for field in required_fields):
                    needs_init = True
        except (json.JSONDecodeError, OSError):
            needs_init = True

    if needs_init:
        try:
            meta_data = {
                "repo_path": str(repo_root.resolve()),
                "created_at": datetime.now().isoformat(),
                "schema_version": "0.1"
            }
            meta_json.write_text(json.dumps(meta_data, indent=2), encoding='utf-8')
        except OSError as e:
            sys.exit(f"ERROR: Failed to create meta.json: {e}")


def init_intent_structure() -> Path:
    """
    Initialize .intent/ directory structure.

    Returns:
        Path to .intent directory.

    Raises:
        SystemExit: If initialization fails or not in a git repository.
    """
    repo_root = find_repo_root(Path.cwd())
    intent_dir = repo_root / '.intent'

    try:
        intent_dir.mkdir(exist_ok=True)
    except OSError as e:
        sys.exit(f"ERROR: Failed to create .intent directory: {e}")

    intent_db = intent_dir / 'intent.db'
    try:
        ensure_database_schema(intent_db)
    except (OSError, sqlite3.Error) as e:
        sys.exit(f"ERROR: Failed to create intent.db: {e}")

    ensure_meta_json(intent_dir, repo_root)

    return intent_dir

