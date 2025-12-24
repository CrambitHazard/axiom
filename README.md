# Axiom

**Axiom** is an intent-first, local-first memory layer for software development.

Git records *what* changed.
Axiom preserves *why* it changed.

Over time, software systems lose their original reasoning. Assumptions fade, decisions become implicit, and future contributors are left guessing. Axiom exists to make intent, assumptions, and decisions first-class artifacts—so software can remember itself.

---

## Table of Contents

* [Installation](#installation)
* [Quick Start](#quick-start)
* [The Problem](#the-problem)
* [The Thesis](#the-thesis)
* [What Axiom Is](#what-axiom-is)
* [What Axiom Is Not](#what-axiom-is-not)
* [Core Concepts](#core-concepts)
* [Design Principles](#design-principles)
* [Project Status](#project-status)
* [Non-Goals (v0)](#non-goals-v0)
* [Philosophy](#philosophy)

---

## Installation

### Prerequisites

* Python 3.7 or higher
* Git (to work within a Git repository)

### Quick Installation

**Windows (PowerShell):**

```powershell
# Navigate to the axiom directory
cd path\to\axiom

# Run the installer (adds to PATH automatically)
.\install.ps1

# Close and reopen your terminal, then use axiom!
```

**Linux / macOS:**

```bash
# Navigate to the axiom directory
cd path/to/axiom

# Make installer executable and run it
chmod +x install.sh
./install.sh

# Reload your shell
source ~/.bashrc  # or source ~/.zshrc
```

The installer automatically adds Axiom to your PATH. **That's it!** After closing and reopening your terminal, you can use `axiom` from anywhere.

### Manual Installation (Alternative)

If you prefer to set up PATH manually:

#### Windows

1. Open System Properties:
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Or: Settings → System → About → Advanced system settings
2. Click "Environment Variables"
3. Under "User variables", find and select "Path", then click "Edit"
4. Click "New" and add the full path to this repository (e.g., `C:\Users\YourName\axiom`)
5. Click "OK" on all dialogs
6. **Restart your terminal/PowerShell** for changes to take effect

#### Linux / macOS

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export PATH="$PATH:/path/to/axiom"
```

Then reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

### Verify Installation

After adding to PATH, verify it works:

```bash
axiom --help
```

You should see the Axiom CLI help text.

---

## Quick Start

1. **Initialize Axiom in your Git repository:**

```bash
axiom init
```

This creates `.intent/` directory with `intent.db` and `meta.json`.

2. **Create your first intent:**

```bash
axiom new
```

Follow the prompts to enter title, problem, context, and constraints.

3. **List all intents:**

```bash
axiom list
```

4. **View a specific intent:**

```bash
axiom show <intent_id>
```

---

## The Problem

Modern development workflows treat code as the source of truth.

But code alone cannot answer questions like:

* Why was this system designed this way?
* What assumptions does this logic rely on?
* Which alternatives were rejected, and why?
* What will break if we change this?

Git diffs capture edits, not reasoning.
Documentation drifts.
Institutional memory decays.

This is not a tooling problem, it is a **memory problem**.

---

## The Thesis

Axiom is built on a simple premise:

> **Code is a consequence, not the source of truth.**

In Axiom:

* **Intent** exists before code
* **Assumptions** are explicitly tracked
* **Decisions** are recorded as commitments
* **Code changes are linked to reasoning**, not the other way around

Git remains unchanged.
Axiom sits above it.

---

## What Axiom Is

Axiom is:

* A local-first tool that lives *inside* a Git repository
* A structured system for capturing intent, assumptions, and decisions
* A long-term memory layer for serious software projects
* Opinionated by design

Axiom does **not** replace Git or GitHub.
It exposes what they structurally cannot represent.

---

## What Axiom Is Not

Axiom is intentionally **not**:

* A code editor
* An AI coding assistant
* A collaboration platform
* A project management tool
* A social or reputation system

AI may assist, but it is never the authority.

---

## Core Concepts

### Intent

A reason to change the system.

An Intent exists independently of code.
Code is produced to satisfy an Intent, not the other way around.

---

### Assumption

A belief about reality that may be false.

Assumptions are tracked explicitly because unexamined assumptions are where systems decay.

---

### Decision

A committed choice among alternatives.

Decisions are append-only. History is never rewritten, only superseded.

---

## Design Principles

* **Local-first**
  All data lives with the repository.

* **Append-only reasoning**
  Decisions and intent history are preserved, not overwritten.

* **Explicit assumptions**
  Hidden beliefs are treated as risk.

* **Human accountability**
  AI can suggest; humans decide.

* **Minimal surface area**
  Fewer features, sharper intent.

---

## Project Status

Axiom is in early development.

Current focus:

* Defining a rigorous ontology
* Binding reasoning to real repositories
* Building a CLI-first workflow
* Dogfooding Axiom on Axiom itself

This project prioritizes correctness of thought over speed of adoption.

---

## Non-Goals (v0)

The following are consciously excluded:

* User accounts
* Permissions or roles
* Hosting or syncing
* CI/CD integration
* Metrics, ratings, or gamification

These exclusions are intentional and protective.

---

## Philosophy

Axiom treats software as a sequence of commitments made under uncertainty.

If those commitments are not remembered, systems decay, not because developers are careless, but because the tools forget.

Axiom exists to change that.