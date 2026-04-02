from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import uuid
from datetime import date, datetime, time, timedelta


class Category(Enum):
    FEEDING = "feeding"
    EXERCISE = "exercise"
    MEDICATION = "medication"
    GROOMING = "grooming"
    ENRICHMENT = "enrichment"
    OTHER = "other"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age_years: float = 0.0
    weight_lbs: float = 0.0
    health_conditions: list[str] = field(default_factory=list)
    dietary_restrictions: list[str] = field(default_factory=list)


@dataclass
class Task:
    title: str
    category: Category
    duration_minutes: int
    priority: Priority
    time: time  # datetime.time object
    date: date = field(default_factory=date.today)
    frequency: str = "once"  # "daily", "weekly", "once"
    pet: Optional[Pet] = None
    status: TaskStatus = TaskStatus.PENDING
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def mark_complete(self):
        """Set the task status to completed."""
        self.status = TaskStatus.COMPLETED

    def mark_postponed(self):
        """Set the task status to postponed."""
        self.status = TaskStatus.POSTPONED

    def mark_cancelled(self):
        """Set the task status to cancelled."""
        self.status = TaskStatus.CANCELLED

    def is_recurring(self) -> bool:
        """Return True if the task repeats daily or weekly."""
        return self.frequency in ("daily", "weekly")


class Owner:
    def __init__(self, name: str, email: str = ""):
        """Initialize an owner with a name and optional email."""
        self.name = name
        self.email = email
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name from the owner's pet list."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def add_task(self, task: Task) -> None:
        """Add a task to the owner's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task by ID from the owner's task list."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks for this owner."""
        return self.tasks

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return all tasks associated with a specific pet."""
        return [t for t in self.tasks if t.pet == pet]


class Scheduler:
    def _falls_on_date(self, task: Task, target_date: date) -> bool:
        """Check if a task should appear on the given date based on its frequency."""
        if task.date == target_date:
            return True
        if task.date > target_date:
            return False
        if task.frequency == "daily":
            return True
        if task.frequency == "weekly":
            return task.date.weekday() == target_date.weekday()
        return False

    def get_tasks_for_date(self, tasks: list[Task], target_date: date = None) -> list[Task]:
        """Return all pending tasks that should appear on the given date (defaults to today)."""
        if target_date is None:
            target_date = date.today()
        return [t for t in tasks if t.status == TaskStatus.PENDING and self._falls_on_date(t, target_date)]

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by scheduled time."""
        return sorted(tasks, key=lambda t: t.time)

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by priority, highest first."""
        return sorted(tasks, key=lambda t: t.priority.value, reverse=True)

    def filter_by_pet(self, tasks: list[Task], pet: Pet) -> list[Task]:
        """Return tasks associated with a specific pet."""
        return [t for t in tasks if t.pet == pet]

    def filter_by_status(self, tasks: list[Task], status: TaskStatus) -> list[Task]:
        """Return tasks matching the given status."""
        return [t for t in tasks if t.status == status]

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return a list of conflict messages for tasks with overlapping time ranges."""
        conflicts = []
        sorted_tasks = self.sort_by_time(tasks)
        for i in range(len(sorted_tasks)):
            task_a = sorted_tasks[i]
            start_a = datetime.combine(date.today(), task_a.time)
            end_a = start_a + timedelta(minutes=task_a.duration_minutes)
            for j in range(i + 1, len(sorted_tasks)):
                task_b = sorted_tasks[j]
                start_b = datetime.combine(date.today(), task_b.time)
                end_b = start_b + timedelta(minutes=task_b.duration_minutes)
                if start_a < end_b and start_b < end_a:
                    conflicts.append(
                        f"Conflict: '{task_a.title}' ({task_a.time.strftime('%H:%M')}-{end_a.strftime('%H:%M')}) "
                        f"overlaps with '{task_b.title}' ({task_b.time.strftime('%H:%M')}-{end_b.strftime('%H:%M')})"
                    )
        return conflicts

    def handle_recurring(self, task: Task) -> Optional[Task]:
        """Create and return a new instance of a recurring task, or None if not recurring."""
        if not task.is_recurring():
            return None
        next_date = task.date + timedelta(days=1 if task.frequency == "daily" else 7)
        new_task = Task(
            title=task.title,
            category=task.category,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            time=task.time,
            date=next_date,
            frequency=task.frequency,
            pet=task.pet,
            notes=task.notes,
        )
        return new_task