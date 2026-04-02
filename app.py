import streamlit as st
from pawpal_system import Owner, Task, Scheduler, Pet, Category, Priority

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
    st.session_state.owner = Owner(name="Jordan")

st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

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

col5, col6, col7, col8 = st.columns(4)
with col5:
    task_time = st.time_input("Time", value=None)
with col6:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
with col7:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Pet", options=["None"] + pet_names)
with col8:
    notes = st.text_input("Notes", value="")

if st.button("Add task"):
    selected_pet = next((p for p in st.session_state.owner.pets if p.name == selected_pet_name), None)
    task = Task(
        title=task_title,
        category=category,
        duration_minutes=int(duration),
        priority=priority,
        time=task_time,
        frequency=frequency,
        pet=selected_pet,
        notes=notes,
    )
    st.session_state.owner.add_task(task)

owner = st.session_state.owner
if owner.get_all_tasks():
    st.write("Current tasks:")
    st.table(
        [
            {
                "Title": t.title,
                "Category": t.category.name.capitalize(),
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority.name.capitalize(),
                "Time": t.time.strftime("%H:%M") if t.time else "N/A",
                "Frequency": t.frequency,
                "Pet": t.pet.name if t.pet else "N/A",
                "Status": t.status.name.capitalize(),
            }
            for t in owner.get_all_tasks()
        ]
    )
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
        schedule = scheduler.sort_by_priority(pending)
        schedule = scheduler.sort_by_time(schedule)

        conflicts = scheduler.detect_conflicts(pending)
        if conflicts:
            for c in conflicts:
                st.warning(c)

        st.write("Today's Schedule:")
        st.table(
            [
                {
                    "Time": t.time.strftime("%H:%M") if t.time else "N/A",
                    "Title": t.title,
                    "Pet": t.pet.name if t.pet else "N/A",
                    "Category": t.category.name.capitalize(),
                    "Priority": t.priority.name.capitalize(),
                    "Duration": f"{t.duration_minutes} min",
                }
                for t in schedule
            ]
        )

