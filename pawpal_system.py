from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import uuid
from datetime import date, time, timedelta


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
    category: str  # "feeding", "exercise", "medication", "grooming", "enrichment", "other"
    duration_minutes: int
    priority: str  # "low", "medium", "high", "critical"
    time: time  # datetime.time object
    frequency: str = "once"  # "daily", "weekly", "once"
    pet: Optional[Pet] = None
    status: TaskStatus = TaskStatus.PENDING
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def mark_complete(self):
        self.status = TaskStatus.COMPLETED

    def mark_postponed(self):
        self.status = TaskStatus.POSTPONED

    def mark_cancelled(self):
        self.status = TaskStatus.CANCELLED

    def is_recurring(self) -> bool:
        return self.frequency in ("daily", "weekly")


class Owner:
    def __init__(self, name: str, email: str = ""):
        self.name = name
        self.email = email
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        self.pets = [p for p in self.pets if p.name != pet_name]

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_all_tasks(self) -> list[Task]:
        return self.tasks

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        return [t for t in self.tasks if t.pet == pet]


class Scheduler:
    def get_today_tasks(self, tasks: list[Task]) -> list[Task]:
        return [t for t in tasks if t.status == TaskStatus.PENDING]

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: t.time)

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority, 4))

    def filter_by_pet(self, tasks: list[Task], pet: Pet) -> list[Task]:
        return [t for t in tasks if t.pet == pet]

    def filter_by_status(self, tasks: list[Task], status: TaskStatus) -> list[Task]:
        return [t for t in tasks if t.status == status]

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        conflicts = []
        sorted_tasks = self.sort_by_time(tasks)
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                task_a = sorted_tasks[i]
                task_b = sorted_tasks[j]
                if task_a.time == task_b.time:
                    conflicts.append(
                        f"Conflict: '{task_a.title}' and '{task_b.title}' are both scheduled at {task_a.time.strftime('%H:%M')}"
                    )
        return conflicts

    def handle_recurring(self, task: Task) -> Optional[Task]:
        if not task.is_recurring():
            return None
        new_task = Task(
            title=task.title,
            category=task.category,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            time=task.time,
            frequency=task.frequency,
            pet=task.pet,
            notes=task.notes,
        )
        return new_task