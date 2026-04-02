# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

- **Composite sorting**: Tasks are sorted by time first, then by priority within the same time slot, so critical tasks always surface first.
- **Duration-aware conflict detection**: Detects overlapping tasks using time ranges (start + duration), not just exact-time matches.
- **Filter by pet and status**: Task list can be filtered by a specific pet, unassigned tasks, or by status (Pending, Completed, Postponed, Cancelled).
- **Recurring task handling**: When a daily or weekly task is marked complete, a new pending copy is automatically created for the next occurrence.
- **Task completion from schedule**: Checkboxes in the schedule view let users mark tasks complete, updating status in real time.
- **Past date validation**: Prevents creating tasks with a date in the past.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
