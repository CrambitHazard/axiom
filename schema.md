# Axiom Core Schema

This document defines the immutable conceptual schema of Axiom.

Axiom models why software changes, not how it is edited.
Anything that does not fit this schema does not belong in the system.

This file is intentionally strict.

---

## Foundational Principle

Code is a consequence, not a source of truth.

Axiom treats intent, assumptions, and decisions as first class artifacts.
Git remains a reference layer. Axiom models reasoning above it.

---

## Core Primitives

Axiom is built on four and only four primitives.

1. Intent
2. Assumption
3. Decision
4. Evidence

All higher level features must be derived from these.

---

## Intent

An Intent represents a reason to change the system.

An Intent exists before code and may continue to exist even if no code is written.
If code changes without an Intent, it is considered a smell.

### Semantics

* An Intent expresses purpose
* It frames a problem within constraints
* It may succeed, fail, or become invalid without code changes

### Fields

* id: unique identifier (uuid)
* title: short, human readable summary
* problem: what is broken, missing, or inadequate
* context: why this problem matters now
* constraints: technical, temporal, business, ethical, or resource limits
* status: draft | active | satisfied | invalidated
* created_at: timestamp
* last_updated_at: timestamp

### Relationships

* Has many Assumptions
* Has many Decisions
* Links to zero or more Git commits
* Links to zero or more files or paths

---

## Assumption

An Assumption is a belief about reality that may be false.

Assumptions are tracked explicitly because unexamined assumptions are the primary cause of long term system decay.

### Semantics

* Assumptions introduce uncertainty
* They age over time
* They can invalidate an Intent without any code change

### Fields

* id: unique identifier
* intent_id: parent Intent
* statement: the belief being assumed
* confidence: numeric confidence level from 0.0 to 1.0
* risk_if_false: consequences if the assumption fails
* created_at: timestamp
* last_validated_at: timestamp or null

### Notes

* Confidence is subjective but explicit
* Validation is human driven, not automated

---

## Decision

A Decision represents a committed choice among alternatives.

Decisions are append only. They are never edited or deleted.
If a decision is reversed, a new Decision must be created.

### Semantics

* Decisions bind the system to a path
* They trade optionality for progress
* They are historically authoritative

### Fields

* id: unique identifier
* intent_id: parent Intent
* summary: concise description of the choice
* rationale: why this option was selected
* alternatives_considered: rejected options and brief reasons
* tradeoffs: costs, risks, and compromises accepted
* created_at: timestamp

---

## Evidence

Evidence represents observable signals that support or challenge Intents, Assumptions, or Decisions.

Evidence is descriptive, not interpretive.

### Semantics

* Evidence does not decide outcomes
* It informs human judgment
* It may support or contradict prior reasoning

### Fields

* id: unique identifier
* related_type: intent | assumption | decision
* related_id: identifier of the related entity
* description: what was observed
* source: commit | issue | metric | user_report | manual
* timestamp: when the evidence occurred

---

## System Invariants

The following invariants must always hold.

1. An Intent may exist without code.
2. Code may not exist without an Intent without being flagged.
3. Decisions are immutable and append only.
4. Assumptions must age and may become invalid implicitly.
5. AI may suggest content but cannot create or validate truth.
6. Git is a reference layer, not a source of reasoning.
7. History is never rewritten. It is only extended.

Violating these invariants breaks the system’s purpose.

---

## Explicit Non Goals (v0)

Axiom intentionally does not model the following.

* Users or identities
* Permissions or access control
* Teams or organizations
* Ratings, reputation, or gamification
* Hosting, syncing, or cloud storage
* CI/CD or deployment concerns

These are excluded to preserve conceptual clarity.

---

## Evolution Rules

* The schema may evolve only by addition, not mutation
* Breaking changes require explicit migration intent
* Convenience must never override conceptual integrity

---

## Closing Note

Axiom treats software as a record of decisions made under uncertainty.

If that uncertainty is not remembered, systems rot silently.

This schema exists to prevent that.