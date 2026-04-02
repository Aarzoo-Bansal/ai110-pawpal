from datetime import date, time
from pawpal_system import Task, Pet, Owner, Category, Priority, TaskStatus, Scheduler


# --- Task Status ---

def test_mark_complete_changes_status():
    """Verify that a new task starts as PENDING and changes to COMPLETED after mark_complete()."""
    task = Task(
        title="Feed Bella",
        category=Category.FEEDING,
        duration_minutes=15,
        priority=Priority.HIGH,
        time=time(8, 0),
    )
    assert task.status == TaskStatus.PENDING
    task.mark_complete()
    assert task.status == TaskStatus.COMPLETED


def test_mark_postponed_and_cancelled():
    """Verify that mark_postponed() and mark_cancelled() update the task status correctly."""
    task = Task(title="Groom", category=Category.GROOMING, duration_minutes=20, priority=Priority.LOW, time=time(10, 0))
    task.mark_postponed()
    assert task.status == TaskStatus.POSTPONED
    task.mark_cancelled()
    assert task.status == TaskStatus.CANCELLED


# --- Owner / Pet Management ---

def test_add_task_increases_pet_task_count():
    """Verify that adding a task assigned to a pet increases that pet's task count from 0 to 1."""
    owner = Owner(name="Alice")
    pet = Pet(name="Bella", species="Dog")
    owner.add_pet(pet)

    assert len(owner.get_tasks_for_pet(pet)) == 0

    task = Task(
        title="Walk Bella",
        category=Category.EXERCISE,
        duration_minutes=30,
        priority=Priority.MEDIUM,
        time=time(9, 0),
        pet=pet,
    )
    owner.add_task(task)

    assert len(owner.get_tasks_for_pet(pet)) == 1


def test_remove_task_by_id():
    """Verify that removing a task by its unique ID deletes it from the owner's task list."""
    owner = Owner(name="Alice")
    task = Task(title="Feed", category=Category.FEEDING, duration_minutes=10, priority=Priority.HIGH, time=time(8, 0))
    owner.add_task(task)
    assert len(owner.get_all_tasks()) == 1
    owner.remove_task(task.id)
    assert len(owner.get_all_tasks()) == 0


def test_remove_pet_by_name():
    """Verify that removing a pet by name leaves only the other pets in the list."""
    owner = Owner(name="Alice")
    owner.add_pet(Pet(name="Bella", species="Dog"))
    owner.add_pet(Pet(name="Max", species="Cat"))
    owner.remove_pet("Bella")
    assert len(owner.pets) == 1
    assert owner.pets[0].name == "Max"


# --- Sorting ---

def test_sort_by_time():
    """Verify that tasks are sorted in ascending order by their scheduled time."""
    scheduler = Scheduler()
    t1 = Task(title="Evening walk", category=Category.EXERCISE, duration_minutes=30, priority=Priority.MEDIUM, time=time(18, 0))
    t2 = Task(title="Morning feed", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(7, 0))
    t3 = Task(title="Midday meds", category=Category.MEDICATION, duration_minutes=5, priority=Priority.CRITICAL, time=time(12, 0))
    result = scheduler.sort_by_time([t1, t2, t3])
    assert [t.title for t in result] == ["Morning feed", "Midday meds", "Evening walk"]


def test_sort_by_priority():
    """Verify that tasks are sorted in descending order by priority (CRITICAL first, LOW last)."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", category=Category.EXERCISE, duration_minutes=30, priority=Priority.LOW, time=time(9, 0))
    t2 = Task(title="Meds", category=Category.MEDICATION, duration_minutes=5, priority=Priority.CRITICAL, time=time(9, 0))
    t3 = Task(title="Groom", category=Category.GROOMING, duration_minutes=20, priority=Priority.MEDIUM, time=time(9, 0))
    result = scheduler.sort_by_priority([t1, t2, t3])
    assert [t.title for t in result] == ["Meds", "Groom", "Walk"]


def test_composite_sort_time_then_priority():
    """Tasks sorted by time first, then by priority within the same time slot."""
    scheduler = Scheduler()
    t1 = Task(title="Low 9am", category=Category.OTHER, duration_minutes=10, priority=Priority.LOW, time=time(9, 0))
    t2 = Task(title="High 9am", category=Category.OTHER, duration_minutes=10, priority=Priority.HIGH, time=time(9, 0))
    t3 = Task(title="Med 8am", category=Category.OTHER, duration_minutes=10, priority=Priority.MEDIUM, time=time(8, 0))
    # Sort by time, then by priority within the same time
    by_time = scheduler.sort_by_time([t1, t2, t3])
    # Within the 9am group, priority sort should put High before Low
    nine_am_tasks = [t for t in by_time if t.time == time(9, 0)]
    by_priority = scheduler.sort_by_priority(nine_am_tasks)
    assert by_priority[0].title == "High 9am"
    assert by_priority[1].title == "Low 9am"


# --- Schedule Generation for a Specific Date ---

def test_get_tasks_for_specific_date():
    """Verify that only tasks matching the selected date are returned, excluding tasks on other dates."""
    scheduler = Scheduler()
    target = date(2026, 5, 1)
    t1 = Task(title="Walk", category=Category.EXERCISE, duration_minutes=30, priority=Priority.HIGH, time=time(9, 0), date=target)
    t2 = Task(title="Feed", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(8, 0), date=date(2026, 5, 2))
    result = scheduler.get_tasks_for_date([t1, t2], target_date=target)
    assert len(result) == 1
    assert result[0].title == "Walk"


def test_get_tasks_for_date_excludes_completed():
    """Verify that completed tasks are excluded from the schedule even if they match the date."""
    scheduler = Scheduler()
    target = date(2026, 5, 1)
    t1 = Task(title="Walk", category=Category.EXERCISE, duration_minutes=30, priority=Priority.HIGH, time=time(9, 0), date=target)
    t1.mark_complete()
    result = scheduler.get_tasks_for_date([t1], target_date=target)
    assert len(result) == 0


def test_get_tasks_for_date_empty_list():
    """Verify that an empty task list returns an empty schedule without errors."""
    scheduler = Scheduler()
    result = scheduler.get_tasks_for_date([], target_date=date(2026, 5, 1))
    assert result == []


# --- Recurring Tasks ---

def test_daily_task_appears_on_future_date():
    """Verify that a daily recurring task appears on any future date after its start date."""
    scheduler = Scheduler()
    t = Task(title="Feed", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(8, 0), date=date(2026, 5, 1), frequency="daily")
    # Should appear on any future date
    result = scheduler.get_tasks_for_date([t], target_date=date(2026, 5, 10))
    assert len(result) == 1


def test_weekly_task_appears_on_correct_weekday():
    """Verify that a weekly task only appears on the same weekday as its start date, not other days."""
    scheduler = Scheduler()
    # May 1, 2026 is a Friday
    start = date(2026, 5, 1)
    t = Task(title="Grooming", category=Category.GROOMING, duration_minutes=60, priority=Priority.MEDIUM, time=time(10, 0), date=start, frequency="weekly")
    # Next Friday
    next_friday = date(2026, 5, 8)
    not_friday = date(2026, 5, 6)  # Wednesday
    assert len(scheduler.get_tasks_for_date([t], target_date=next_friday)) == 1
    assert len(scheduler.get_tasks_for_date([t], target_date=not_friday)) == 0


def test_once_task_does_not_appear_on_other_dates():
    """Verify that a one-time task only appears on its exact date and not on any other date."""
    scheduler = Scheduler()
    t = Task(title="Vet visit", category=Category.OTHER, duration_minutes=60, priority=Priority.HIGH, time=time(14, 0), date=date(2026, 5, 1), frequency="once")
    assert len(scheduler.get_tasks_for_date([t], target_date=date(2026, 5, 2))) == 0


def test_handle_recurring_daily_creates_next_day():
    """Verify that handling a daily task creates a new PENDING task for the next day with a unique ID."""
    scheduler = Scheduler()
    t = Task(title="Feed", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(8, 0), date=date(2026, 5, 1), frequency="daily")
    new_task = scheduler.handle_recurring(t)
    assert new_task is not None
    assert new_task.date == date(2026, 5, 2)
    assert new_task.status == TaskStatus.PENDING
    assert new_task.id != t.id


def test_handle_recurring_weekly_creates_next_week():
    """Verify that handling a weekly task creates a new task exactly 7 days later."""
    scheduler = Scheduler()
    t = Task(title="Groom", category=Category.GROOMING, duration_minutes=60, priority=Priority.MEDIUM, time=time(10, 0), date=date(2026, 5, 1), frequency="weekly")
    new_task = scheduler.handle_recurring(t)
    assert new_task is not None
    assert new_task.date == date(2026, 5, 8)


def test_handle_recurring_once_returns_none():
    """Verify that a one-time (non-recurring) task returns None and no new task is created."""
    scheduler = Scheduler()
    t = Task(title="Vet", category=Category.OTHER, duration_minutes=60, priority=Priority.HIGH, time=time(14, 0), frequency="once")
    assert scheduler.handle_recurring(t) is None


# --- Conflict Detection ---

def test_detect_overlapping_tasks():
    """Verify that two tasks whose time ranges overlap are detected as a conflict."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", category=Category.EXERCISE, duration_minutes=30, priority=Priority.HIGH, time=time(9, 0))
    t2 = Task(title="Feed", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(9, 15))
    conflicts = scheduler.detect_conflicts([t1, t2])
    assert len(conflicts) == 1
    assert "Walk" in conflicts[0] and "Feed" in conflicts[0]


def test_no_conflict_when_tasks_dont_overlap():
    """Verify that tasks with a gap between them produce no conflict."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", category=Category.EXERCISE, duration_minutes=30, priority=Priority.HIGH, time=time(9, 0))
    t2 = Task(title="Feed", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(10, 0))
    conflicts = scheduler.detect_conflicts([t1, t2])
    assert len(conflicts) == 0


def test_back_to_back_tasks_no_conflict():
    """Tasks ending exactly when the next starts should NOT conflict."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", category=Category.EXERCISE, duration_minutes=30, priority=Priority.HIGH, time=time(9, 0))
    t2 = Task(title="Feed", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(9, 30))
    conflicts = scheduler.detect_conflicts([t1, t2])
    assert len(conflicts) == 0


# --- Filter by Pet and Status ---

def test_filter_by_pet():
    """Verify that filtering by pet returns only tasks assigned to that specific pet."""
    scheduler = Scheduler()
    bella = Pet(name="Bella", species="Dog")
    max_pet = Pet(name="Max", species="Cat")
    t1 = Task(title="Walk Bella", category=Category.EXERCISE, duration_minutes=30, priority=Priority.HIGH, time=time(9, 0), pet=bella)
    t2 = Task(title="Feed Max", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(9, 0), pet=max_pet)
    result = scheduler.filter_by_pet([t1, t2], bella)
    assert len(result) == 1
    assert result[0].title == "Walk Bella"


def test_filter_by_status():
    """Verify that filtering by status returns only tasks matching that status (e.g., COMPLETED)."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", category=Category.EXERCISE, duration_minutes=30, priority=Priority.HIGH, time=time(9, 0))
    t2 = Task(title="Feed", category=Category.FEEDING, duration_minutes=15, priority=Priority.HIGH, time=time(10, 0))
    t2.mark_complete()
    result = scheduler.filter_by_status([t1, t2], TaskStatus.COMPLETED)
    assert len(result) == 1
    assert result[0].title == "Feed"
