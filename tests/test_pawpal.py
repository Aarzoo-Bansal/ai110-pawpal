from datetime import time
from pawpal_system import Task, Pet, Owner, Category, Priority, TaskStatus


def test_mark_complete_changes_status():
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


def test_add_task_increases_pet_task_count():
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
