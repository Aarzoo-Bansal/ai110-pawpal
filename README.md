# PawPal+

A pet care planning assistant built with **Streamlit** that helps pet owners organize and schedule daily care tasks for their pets.

## Demo

![PawPal+ Demo](https://github.com/Aarzoo-Bansal/ai110-pawpal/blob/main/gif.gif?raw=true)

## Features

### Algorithms & Scheduling Logic

- **Composite sorting** — Tasks are sorted by time first, then by priority (critical > high > medium > low) within the same time slot, ensuring urgent tasks always surface first
- **Duration-aware conflict detection** — Identifies overlapping tasks by computing time ranges (start time + duration in minutes) rather than comparing exact start times
- **Daily and weekly recurrence** — Recurring tasks automatically appear on future dates; completing a recurring task clones a new pending instance for the next occurrence (next day or same weekday next week)
- **Date-based filtering** — Uses `_falls_on_date()` to determine whether a task should appear on a given date, handling one-time, daily, and weekly frequencies
- **Graceful unscheduled task handling** — Tasks without a set time are placed at the bottom of the schedule sorted by priority, and are excluded from conflict detection

### Task Management

- **Multi-pet support** — Manage multiple pets (dogs, cats, and more) under a single owner profile
- **Full task lifecycle** — Tasks transition through four states: Pending, Completed, Postponed, and Cancelled
- **Six task categories** — Feeding, Exercise, Medication, Grooming, Enrichment, and Other
- **Four priority levels** — Low, Medium, High, and Critical with numeric weighting for sort comparisons
- **Flexible filtering** — Filter the task list by pet, status, or date independently
- **Past date validation** — Prevents creating tasks with a date in the past

### User Interface

- **Tabbed layout** — Three-tab structure (My Pets, Tasks, Schedule) for a clean, focused workflow
- **Custom themed UI** — Warm, pet-friendly color palette with gradient backgrounds, styled tabs, and rounded components
- **Color-coded priority and status badges** — Visual indicators using background colors (red for Critical, green for Completed, etc.)
- **Interactive schedule** — Mark tasks complete directly from the schedule view with checkboxes
- **Sortable task table** — Powered by `st.dataframe()` with per-cell styling for priority and status columns
- **Species and category emojis** — Visual cues throughout the interface

## Tech Stack

| Layer | Tool |
|-------|------|
| UI | Streamlit |
| Styling | Custom CSS via `st.markdown` |
| Data | Python dataclasses, enums |
| Data display | pandas (styled DataFrames) |
| Testing | pytest |

## Getting Started

### Prerequisites

- Python 3.10+

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

### Run Tests

```bash
python -m pytest tests/test_pawpal.py -v
```

## Architecture

The system is composed of four core classes:

| Class | Responsibility |
|-------|---------------|
| `Owner` | Manages pets and tasks |
| `Pet` | Stores pet metadata (name, species, breed, weight, health conditions) |
| `Task` | Represents a care task with status lifecycle, category, priority, and optional recurrence |
| `Scheduler` | Sorts, filters, detects conflicts, and handles recurring task logic |

Three enums define constrained values: `Category`, `Priority`, and `TaskStatus`.

See [uml_diagram.md](uml_diagram.md) for the full class diagram.

## Test Coverage

The test suite includes **22 tests** covering:

- Task status lifecycle (complete, postpone, cancel)
- Owner/pet management (add, remove)
- Sorting (by time, by priority, composite)
- Date-based scheduling and recurring task logic
- Conflict detection (overlapping, non-overlapping, back-to-back)
- Filtering by pet and by status

## Project Structure

```
ai110-pawpal/
├── app.py               # Streamlit UI
├── pawpal_system.py     # Core domain logic
├── main.py              # Standalone demo script
├── requirements.txt     # Dependencies
├── uml_diagram.md       # Class diagram (Mermaid)
├── reflection.md        # Developer reflection
└── tests/
    └── test_pawpal.py   # Unit tests
```
