from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler, Category, Priority, TaskStatus


def main():
    # Create owner
    owner = Owner(name="Aarzoo", email="aarzoo@test.com")

    # Create pets
    dog = Pet(name="Buddy", species="dog", breed="Golden Retriever", age_years=2, weight_lbs=65)
    cat = Pet(name="Whiskers", species="cat", breed="Ragdoll", age_years=1, weight_lbs=6, health_conditions=["sensitive stomach"])

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks — mix of pets, priorities, and times
    tasks = [
        Task(title="Morning walk", category=Category.EXERCISE, duration_minutes=30,
             priority=Priority.HIGH, time=time(7, 0), frequency="daily", pet=dog),
        Task(title="Breakfast - Buddy", category=Category.FEEDING, duration_minutes=15,
             priority=Priority.CRITICAL, time=time(7, 30), frequency="daily", pet=dog),
        Task(title="Breakfast - Whiskers", category=Category.FEEDING, duration_minutes=10,
             priority=Priority.CRITICAL, time=time(7, 30), frequency="daily", pet=cat),
        Task(title="Give medication", category=Category.MEDICATION, duration_minutes=5,
             priority=Priority.CRITICAL, time=time(8, 0), frequency="daily", pet=cat),
        Task(title="Play session", category=Category.ENRICHMENT, duration_minutes=20,
             priority=Priority.MEDIUM, time=time(12, 0), pet=dog),
        Task(title="Evening walk", category=Category.EXERCISE, duration_minutes=30,
             priority=Priority.HIGH, time=time(17, 0), frequency="daily", pet=dog),
        Task(title="Grooming", category=Category.GROOMING, duration_minutes=45,
             priority=Priority.LOW, time=time(15, 0), pet=cat),
        Task(title="Refill water bowls", category=Category.OTHER, duration_minutes=5,
             priority=Priority.MEDIUM, time=time(9, 0), frequency="daily"),
    ]

    for task in tasks:
        owner.add_task(task)

    scheduler = Scheduler()

    # --- Today's Schedule ---
    print(f"=== {owner.name}'s PawPal+ Schedule ===\n")
    print(f"Pets: {', '.join(p.name for p in owner.pets)}\n")

    today_tasks = scheduler.get_today_tasks(owner.get_all_tasks())
    sorted_tasks = scheduler.sort_by_time(today_tasks)

    print("--- Today's Tasks (sorted by time) ---")
    for t in sorted_tasks:
        pet_name = t.pet.name if t.pet else "Household"
        print(f"  {t.time.strftime('%H:%M')} | {t.title} ({pet_name}) - {t.priority.name} priority")

    # --- Sort by priority ---
    print("\n--- Tasks by Priority ---")
    priority_tasks = scheduler.sort_by_priority(today_tasks)
    for t in priority_tasks:
        pet_name = t.pet.name if t.pet else "Household"
        print(f"  [{t.priority.name}] {t.title} ({pet_name}) at {t.time.strftime('%H:%M')}")

    # --- Filter by pet ---
    print(f"\n--- Buddy's Tasks ---")
    buddy_tasks = scheduler.filter_by_pet(today_tasks, dog)
    for t in buddy_tasks:
        print(f"  {t.time.strftime('%H:%M')} | {t.title}")

    print(f"\n--- Whiskers' Tasks ---")
    whiskers_tasks = scheduler.filter_by_pet(today_tasks, cat)
    for t in whiskers_tasks:
        print(f"  {t.time.strftime('%H:%M')} | {t.title}")

    # --- Conflict detection ---
    print("\n--- Conflict Check ---")
    conflicts = scheduler.detect_conflicts(today_tasks)
    if conflicts:
        for c in conflicts:
            print(f"  ⚠ {c}")
    else:
        print("  No conflicts found!")

    # --- Mark a task complete and test recurring ---
    print("\n--- Completing 'Morning walk' ---")
    morning_walk = tasks[0]
    morning_walk.mark_complete()
    print(f"  Status: {morning_walk.status.value}")

    new_task = scheduler.handle_recurring(morning_walk)
    if new_task:
        print(f"  Recurring task created: '{new_task.title}' (status: {new_task.status.value})")

    # --- Filter by status ---
    print("\n--- Pending Tasks ---")
    pending = scheduler.filter_by_status(owner.get_all_tasks(), TaskStatus.PENDING)
    print(f"  {len(pending)} tasks remaining")


if __name__ == "__main__":
    main()
