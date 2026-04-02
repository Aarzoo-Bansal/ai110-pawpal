import streamlit as st
from datetime import date
from pawpal_system import Owner, Task, Scheduler, Pet, Category, Priority, TaskStatus

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
schedular = Scheduler()
st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Name")

st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value="")
pet_name = st.text_input("Pet name", value="Pet Name")
species = st.selectbox("Species", ["Dog", "Cat", "Other"])

if st.button("Add pet"):
    pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(pet)

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table([{"Name": p.name, "Species": p.species} for p in st.session_state.owner.pets])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", options=list(Priority), format_func=lambda p: p.name.capitalize())
with col4:
    category = st.selectbox("Category", options=list(Category), format_func=lambda c: c.name.capitalize())

col5, col6, col7, col8, col9 = st.columns(5)
with col5:
    task_time = st.time_input("Time", value=None)
with col6:
    task_date = st.date_input("Date")
with col7:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
with col8:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Pet", options=["None"] + pet_names)
with col9:
    notes = st.text_input("Notes", value="")

if st.button("Add task"):
    if task_date < date.today():
        st.error("Cannot create a task in the past. Please select today or a future date.")
    else:
        selected_pet = next((p for p in st.session_state.owner.pets if p.name == selected_pet_name), None)
        task = Task(
            title=task_title,
            category=category,
            duration_minutes=int(duration),
            priority=priority,
            time=task_time,
            date=task_date,
            frequency=frequency,
            pet=selected_pet,
            notes=notes,
        )
        st.session_state.owner.add_task(task)

owner = st.session_state.owner
if owner.get_all_tasks():
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        pet_filter_options = ["All"] + [p.name for p in owner.pets] + ["None"]
        selected_filter = st.selectbox("Filter by pet", options=pet_filter_options, key="pet_filter")
    with filter_col2:
        status_filter_options = ["All"] + [s.name.capitalize() for s in TaskStatus]
        selected_status = st.selectbox("Filter by status", options=status_filter_options, key="status_filter")

    all_tasks = owner.get_all_tasks()
    if selected_filter == "All":
        filtered_tasks = all_tasks
    elif selected_filter == "None":
        filtered_tasks = [t for t in all_tasks if t.pet is None]
    else:
        pet = next(p for p in owner.pets if p.name == selected_filter)
        filtered_tasks = schedular.filter_by_pet(all_tasks, pet)

    if selected_status != "All":
        status = TaskStatus[selected_status.upper()]
        filtered_tasks = schedular.filter_by_status(filtered_tasks, status)

    st.write("Current tasks:")
    if filtered_tasks:
        st.table(
            [
                {
                    "Title": t.title,
                    "Category": t.category.name.capitalize(),
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": t.priority.name.capitalize(),
                    "Time": t.time.strftime("%H:%M") if t.time else "N/A",
                    "Date": t.date.strftime("%Y-%m-%d"),
                    "Frequency": t.frequency,
                    "Pet": t.pet.name if t.pet else "N/A",
                    "Status": t.status.name.capitalize(),
                }
                for t in filtered_tasks
            ]
        )
    else:
        st.info(f"No tasks for '{selected_filter}'.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    all_tasks = owner.get_all_tasks()
    pending = scheduler.get_today_tasks(all_tasks)

    if not pending:
        st.warning("No pending tasks to schedule.")
    else:
        schedule = sorted(pending, key=lambda t: (t.time, -t.priority.value))
        conflicts = scheduler.detect_conflicts(pending)
        st.session_state.schedule = schedule
        st.session_state.conflicts = conflicts

if "schedule" in st.session_state and st.session_state.schedule:
    conflicts = st.session_state.get("conflicts", [])
    if conflicts:
        for c in conflicts:
            st.warning(c)

    st.write("Today's Schedule:")
    for t in st.session_state.schedule:
        col_check, col_time, col_title, col_pet, col_cat, col_pri, col_dur = st.columns([0.5, 1, 2, 1, 1, 1, 1])
        with col_check:
            checked = st.checkbox("✓", key=t.id, label_visibility="collapsed")
        with col_time:
            st.write(t.time.strftime("%H:%M") if t.time else "N/A")
        with col_title:
            st.write(t.title)
        with col_pet:
            st.write(t.pet.name if t.pet else "N/A")
        with col_cat:
            st.write(t.category.name.capitalize())
        with col_pri:
            st.write(t.priority.name.capitalize())
        with col_dur:
            st.write(f"{t.duration_minutes} min")
        if checked and t.status != t.status.COMPLETED:
            t.mark_complete()
            new_task = schedular.handle_recurring(t)
            if new_task:
                owner.add_task(new_task)
            st.rerun()

