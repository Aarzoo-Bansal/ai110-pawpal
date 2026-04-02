import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pawpal_system import Owner, Task, Scheduler, Pet, Category, Priority, TaskStatus

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# --- Custom CSS Theme ---
st.markdown(
    """
    <style>
    /* Main background and font */
    .stApp {
        background: linear-gradient(135deg, #fdf6ec 0%, #f0e6d3 100%);
    }

    /* Headers */
    h1, h2, h3 {
        color: #5a3e2b !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f5e6d0;
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        color: #5a3e2b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8956b !important;
        color: white !important;
        border-radius: 10px;
    }

    /* Buttons */
    .stButton > button {
        background-color: #e8956b;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #d4784f;
        color: white;
        border: none;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #d4b896;
    }

    /* Cards / containers */
    .pet-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(90, 62, 43, 0.1);
        border-left: 4px solid #e8956b;
    }

    /* Priority badges */
    .badge {
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: 600;
        display: inline-block;
    }
    .badge-critical { background-color: #fee2e2; color: #dc2626; }
    .badge-high { background-color: #ffedd5; color: #ea580c; }
    .badge-medium { background-color: #fef9c3; color: #ca8a04; }
    .badge-low { background-color: #dcfce7; color: #16a34a; }

    .badge-pending { background-color: #dbeafe; color: #2563eb; }
    .badge-completed { background-color: #dcfce7; color: #16a34a; }
    .badge-postponed { background-color: #fef9c3; color: #ca8a04; }
    .badge-cancelled { background-color: #f3f4f6; color: #6b7280; }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Align checkbox with row content in schedule */
    .schedule-row {
        background: white;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        box-shadow: 0 1px 4px rgba(90, 62, 43, 0.08);
        display: flex;
        align-items: center;
    }

    /* Remove top padding from columns in schedule rows so checkbox aligns */
    [data-testid="stHorizontalBlock"] [data-testid="stCheckbox"] {
        margin-top: -8px;
    }

    /* Vertically align all column content */
    [data-testid="stHorizontalBlock"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stHorizontalBlock"] [data-testid="stMarkdownContainer"] span {
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Helper functions for badges ---
PRIORITY_BADGES = {
    "Critical": '<span class="badge badge-critical">Critical</span>',
    "High": '<span class="badge badge-high">High</span>',
    "Medium": '<span class="badge badge-medium">Medium</span>',
    "Low": '<span class="badge badge-low">Low</span>',
}

STATUS_BADGES = {
    "Pending": '<span class="badge badge-pending">Pending</span>',
    "Completed": '<span class="badge badge-completed">Completed</span>',
    "Postponed": '<span class="badge badge-postponed">Postponed</span>',
    "Cancelled": '<span class="badge badge-cancelled">Cancelled</span>',
}

SPECIES_EMOJI = {"Dog": "🐶", "Cat": "🐱", "Other": "🐾"}

CATEGORY_EMOJI = {
    "Feeding": "🍖",
    "Exercise": "🏃",
    "Medication": "💊",
    "Grooming": "✂️",
    "Enrichment": "🧸",
    "Other": "📋",
}


def priority_badge(priority_name: str) -> str:
    return PRIORITY_BADGES.get(priority_name, priority_name)


def status_badge(status_name: str) -> str:
    return STATUS_BADGES.get(status_name, status_name)


# --- Session state ---
scheduler = Scheduler()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Name")

owner = st.session_state.owner

# --- Title ---
st.title("🐾 PawPal+")
st.caption("Your pet care planning assistant")

# --- Tabs ---
tab_pets, tab_tasks, tab_schedule = st.tabs(["🏠 My Pets", "📝 Tasks", "📅 Schedule"])

# ===================== TAB 1: MY PETS =====================
with tab_pets:
    col_form, col_list = st.columns([1, 2])

    with col_form:
        st.subheader("Add a Pet")
        owner_name = st.text_input("Owner name", value="")
        pet_name = st.text_input("Pet name", value="Pet Name")
        species = st.selectbox("Species", ["Dog", "Cat", "Other"])

        if st.button("Add pet", use_container_width=True):
            pet = Pet(name=pet_name, species=species)
            st.session_state.owner.add_pet(pet)
            st.rerun()

    with col_list:
        st.subheader("My Pets")
        if owner.pets:
            for p in owner.pets:
                emoji = SPECIES_EMOJI.get(p.species, "🐾")
                st.markdown(
                    f"""<div class="pet-card">
                        <strong>{emoji} {p.name}</strong> &mdash; {p.species}
                    </div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.info("No pets yet. Add one using the form.")

# ===================== TAB 2: TASKS =====================
with tab_tasks:
    st.subheader("Add a Task")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox(
            "Priority", options=list(Priority), format_func=lambda p: p.name.capitalize()
        )
    with col4:
        category = st.selectbox(
            "Category", options=list(Category), format_func=lambda c: c.name.capitalize()
        )

    col5, col6, col7, col8, col9 = st.columns(5)
    with col5:
        task_time = st.time_input("Time", value=None)
    with col6:
        task_date = st.date_input("Date")
    with col7:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    with col8:
        pet_names = [p.name for p in owner.pets]
        selected_pet_name = st.selectbox("Pet", options=["None"] + pet_names)
    with col9:
        notes = st.text_input("Notes", value="")

    if st.button("Add task", use_container_width=True):
        if task_date < date.today():
            st.error("Cannot create a task in the past. Please select today or a future date.")
        else:
            selected_pet = next(
                (p for p in owner.pets if p.name == selected_pet_name), None
            )
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
            st.rerun()

    st.divider()

    # --- Task list with filters ---
    if owner.get_all_tasks():
        st.subheader("My Tasks")
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            pet_filter_options = ["All"] + [p.name for p in owner.pets] + ["None"]
            selected_filter = st.selectbox(
                "Filter by pet", options=pet_filter_options, key="pet_filter"
            )
        with filter_col2:
            status_filter_options = ["All"] + [s.name.capitalize() for s in TaskStatus]
            selected_status = st.selectbox(
                "Filter by status", options=status_filter_options, key="status_filter"
            )
        with filter_col3:
            task_list_date = st.date_input(
                "Filter by date", value=date.today(), key="task_list_date"
            )

        all_tasks = owner.get_all_tasks()
        filtered_tasks = [t for t in all_tasks if scheduler._falls_on_date(t, task_list_date)]

        if selected_filter == "All":
            pass
        elif selected_filter == "None":
            filtered_tasks = [t for t in filtered_tasks if t.pet is None]
        else:
            pet = next(p for p in owner.pets if p.name == selected_filter)
            filtered_tasks = scheduler.filter_by_pet(filtered_tasks, pet)

        if selected_status != "All":
            status = TaskStatus[selected_status.upper()]
            filtered_tasks = scheduler.filter_by_status(filtered_tasks, status)

        if filtered_tasks:
            df = pd.DataFrame(
                [
                    {
                        "Title": t.title,
                        "Category": f"{CATEGORY_EMOJI.get(t.category.name.capitalize(), '')} {t.category.name.capitalize()}",
                        "Duration": f"{t.duration_minutes} min",
                        "Priority": t.priority.name.capitalize(),
                        "Time": t.time.strftime("%H:%M") if t.time else "N/A",
                        "Date": t.date.strftime("%Y-%m-%d"),
                        "Frequency": t.frequency.capitalize(),
                        "Pet": f"{SPECIES_EMOJI.get(t.pet.species, '')} {t.pet.name}" if t.pet else "N/A",
                        "Status": t.status.name.capitalize(),
                    }
                    for t in filtered_tasks
                ]
            )

            def color_priority(val):
                colors = {
                    "Critical": "background-color: #fee2e2; color: #dc2626; font-weight: 600",
                    "High": "background-color: #ffedd5; color: #ea580c; font-weight: 600",
                    "Medium": "background-color: #fef9c3; color: #ca8a04; font-weight: 600",
                    "Low": "background-color: #dcfce7; color: #16a34a; font-weight: 600",
                }
                return colors.get(val, "")

            def color_status(val):
                colors = {
                    "Pending": "background-color: #dbeafe; color: #2563eb; font-weight: 600",
                    "Completed": "background-color: #dcfce7; color: #16a34a; font-weight: 600",
                    "Postponed": "background-color: #fef9c3; color: #ca8a04; font-weight: 600",
                    "Cancelled": "background-color: #f3f4f6; color: #6b7280; font-weight: 600",
                }
                return colors.get(val, "")

            styled_df = df.style.map(color_priority, subset=["Priority"]).map(
                color_status, subset=["Status"]
            )

            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(f"No tasks for '{selected_filter}'.")
    else:
        st.info("No tasks yet. Add one above.")

# ===================== TAB 3: SCHEDULE =====================
with tab_schedule:
    st.subheader("Build Schedule")

    schedule_date = st.date_input(
        "Schedule for date",
        value=date.today(),
        min_value=date.today(),
        max_value=date.today() + timedelta(days=10),
        key="schedule_date",
    )

    if st.button("Generate schedule", use_container_width=True):
        all_tasks = owner.get_all_tasks()
        pending = scheduler.get_tasks_for_date(all_tasks, schedule_date)

        if not pending:
            st.warning("No pending tasks to schedule.")
        else:
            timed = [t for t in pending if t.time is not None]
            untimed = [t for t in pending if t.time is None]
            schedule = sorted(timed, key=lambda t: (t.time, -t.priority.value)) + sorted(untimed, key=lambda t: -t.priority.value)
            conflicts = scheduler.detect_conflicts(pending)
            st.session_state.schedule = schedule
            st.session_state.conflicts = conflicts

    if "schedule" in st.session_state and st.session_state.schedule:
        conflicts = st.session_state.get("conflicts", [])
        if conflicts:
            for c in conflicts:
                st.warning(c)

        st.divider()
        st.subheader("Today's Schedule")

        # Column headers
        hdr_check, hdr_time, hdr_title, hdr_pet, hdr_cat, hdr_pri, hdr_dur = st.columns(
            [0.5, 1, 2, 1, 1, 1, 1]
        )
        with hdr_time:
            st.markdown("**Time**")
        with hdr_title:
            st.markdown("**Task**")
        with hdr_pet:
            st.markdown("**Pet**")
        with hdr_cat:
            st.markdown("**Category**")
        with hdr_pri:
            st.markdown("**Priority**")
        with hdr_dur:
            st.markdown("**Duration**")

        for t in st.session_state.schedule:
            col_check, col_time, col_title, col_pet, col_cat, col_pri, col_dur = st.columns(
                [0.5, 1, 2, 1, 1, 1, 1]
            )
            with col_check:
                checked = st.checkbox("Done", key=t.id, label_visibility="collapsed")
            with col_time:
                st.write(t.time.strftime("%H:%M") if t.time else "N/A")
            with col_title:
                st.write(t.title)
            with col_pet:
                if t.pet:
                    emoji = SPECIES_EMOJI.get(t.pet.species, "🐾")
                    st.write(f"{emoji} {t.pet.name}")
                else:
                    st.write("N/A")
            with col_cat:
                cat_name = t.category.name.capitalize()
                cat_emoji = CATEGORY_EMOJI.get(cat_name, "")
                st.write(f"{cat_emoji} {cat_name}")
            with col_pri:
                pri_name = t.priority.name.capitalize()
                st.markdown(priority_badge(pri_name), unsafe_allow_html=True)
            with col_dur:
                st.write(f"{t.duration_minutes} min")

            if checked and t.status != TaskStatus.COMPLETED:
                t.mark_complete()
                new_task = scheduler.handle_recurring(t)
                if new_task:
                    owner.add_task(new_task)
                st.rerun()
