#!/usr/bin/env python3
"""
Axiom CLI - Intent-first memory layer for software decisions.

Commands:
    axiom init    - Initialize .intent/ directory structure
    axiom new     - Create a new intent interactively
    axiom list    - List all intents
    axiom show    - Show a specific intent by ID
"""

import argparse
import os
import sqlite3
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Add the script's directory to Python path so intent_core can be imported
# This allows axiom to work from any directory
_script_dir = Path(__file__).resolve().parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

import intent_core


def cmd_init() -> None:
    """
    Initialize .intent/ directory structure.

    Fails if not in a Git repo.
    Creates .intent/, intent.db, and meta.json.
    Is idempotent (safe to re-run).
    """
    intent_dir = intent_core.init_intent_structure()
    print(f"Initialized .intent/ at: {intent_dir}")


def read_multiline(prompt: str) -> str:
    """
    Read multiline input until three consecutive blank lines.

    Uses three consecutive blank lines as finish signal to allow
    users to include blank lines for formatting in their content.

    Args:
        prompt: Prompt to display.

    Returns:
        Collected lines joined with newlines, preserving formatting.
    """
    print(prompt)
    print("(Press Enter three times to finish)")
    lines = []
    empty_count = 0
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 3:
                break
        else:
            empty_count = 0
        lines.append(line)
    # Remove the three trailing empty lines that signaled finish
    for _ in range(3):
        if lines and lines[-1] == "":
            lines.pop()
    return "\n".join(lines)


def cmd_new() -> None:
    """
    Create a new intent interactively.

    Prompts for title, problem, context, constraints.
    Creates intent with status = draft.
    """
    intent_dir = intent_core.get_intent_dir()
    intent_db = intent_dir / 'intent.db'

    if not intent_db.exists():
        sys.exit("ERROR: .intent/ not initialized. Run 'axiom init' first.")

    print("Create a new intent")
    print("=" * 50)

    title = input("Title: ").strip()
    if not title:
        sys.exit("ERROR: Title is required.")

    problem = read_multiline("\nProblem:")

    context = read_multiline("\nContext:")

    constraints = read_multiline("\nConstraints:")

    intent_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    conn = sqlite3.connect(str(intent_db))
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO intents (id, title, problem, context, constraints, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (intent_id, title, problem, context, constraints, 'draft', now, now))
    conn.commit()
    conn.close()

    print(f"\nCreated intent: {intent_id}")
    print(f"  Title: {title}")
    print(f"  Status: draft")


def cmd_list() -> None:
    """
    List all intents.

    Shows: id (shortened), title, status, created_at.
    """
    intent_dir = intent_core.get_intent_dir()
    intent_db = intent_dir / 'intent.db'

    if not intent_db.exists():
        sys.exit("ERROR: .intent/ not initialized. Run 'axiom init' first.")

    conn = sqlite3.connect(str(intent_db))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, status, created_at
        FROM intents
        ORDER BY created_at DESC
    """)
    intents = cursor.fetchall()
    conn.close()

    if not intents:
        print("No intents found.")
        return

    print(f"{'ID':<10} {'Title':<40} {'Status':<12} {'Created'}")
    print("-" * 80)

    for intent_id, title, status, created_at in intents:
        short_id = intent_id[:8]
        title_display = title[:38] + ".." if len(title) > 40 else title
        created_display = created_at[:10] if created_at else ""
        print(f"{short_id:<10} {title_display:<40} {status:<12} {created_display}")


def find_intent_by_prefix(intent_db: Path, prefix: str) -> str:
    """
    Find intent ID by prefix matching.

    Args:
        intent_db: Path to the database.
        prefix: Prefix to match (6-8 chars recommended).

    Returns:
        Full intent ID if exactly one match found.

    Raises:
        SystemExit: If no matches or ambiguous matches.
    """
    conn = sqlite3.connect(str(intent_db))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM intents
        WHERE id LIKE ?
    """, (f"{prefix}%",))
    matches = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not matches:
        sys.exit(f"ERROR: No intent found matching prefix '{prefix}'.")
    
    if len(matches) > 1:
        sys.exit(f"ERROR: Ambiguous prefix '{prefix}' matches {len(matches)} intents:\n  " + 
                 "\n  ".join(matches))
    
    return matches[0]


def cmd_show(intent_id: str) -> None:
    """
    Show a specific intent by ID.

    Supports prefix matching: if 6-8 chars provided, matches exactly one intent.
    Errors if ambiguous.

    Args:
        intent_id: The intent ID or prefix to display.
    """
    intent_dir = intent_core.get_intent_dir()
    intent_db = intent_dir / 'intent.db'

    if not intent_db.exists():
        sys.exit("ERROR: .intent/ not initialized. Run 'axiom init' first.")

    # If short prefix (6-8 chars), use prefix matching
    if len(intent_id) >= 6 and len(intent_id) < 36:
        intent_id = find_intent_by_prefix(intent_db, intent_id)

    conn = sqlite3.connect(str(intent_db))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, problem, context, constraints, status, created_at, updated_at
        FROM intents
        WHERE id = ?
    """, (intent_id,))
    intent = cursor.fetchone()
    conn.close()

    if not intent:
        sys.exit(f"ERROR: Intent '{intent_id}' not found.")

    intent_id_full, title, problem, context, constraints, status, created_at, updated_at = intent

    print(f"Intent: {intent_id_full}")
    print("=" * 80)
    print(f"Title: {title}")
    print(f"Status: {status}")
    print(f"Created: {created_at}")
    print(f"Updated: {updated_at}")
    print()
    if problem:
        print(f"Problem:\n{problem}\n")
    if context:
        print(f"Context:\n{context}\n")
    if constraints:
        print(f"Constraints:\n{constraints}\n")


def main() -> None:
    """
    Main CLI entry point.
    """
    parser = argparse.ArgumentParser(
        description='Axiom CLI - Intent-first memory layer for software decisions',
        prog='axiom'
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    subparsers.add_parser('init', help='Initialize .intent/ directory structure')
    subparsers.add_parser('new', help='Create a new intent interactively')
    subparsers.add_parser('list', help='List all intents')
    show_parser = subparsers.add_parser('show', help='Show a specific intent by ID')
    show_parser.add_argument('intent_id', help='The intent ID to display')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'init':
        cmd_init()
    elif args.command == 'new':
        cmd_new()
    elif args.command == 'list':
        cmd_list()
    elif args.command == 'show':
        cmd_show(args.intent_id)


if __name__ == '__main__':
    main()

