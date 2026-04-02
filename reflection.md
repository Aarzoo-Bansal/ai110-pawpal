# PawPal+ Project Reflection

## 1. System Design

1. Pawpal should allow a user to add their pets.
2. Pawpal should allow users to add tasks, prioritize them, and input their available time.
3. As per the details entered by the user, the agent should create a schedule for the user.
4. If the pet needs medication, then the user should be able to add those and set reminders.

**a. Initial design**

- What classes did you include, and what responsibilities did you assign to each?

      1. A owner class which contains name, email, available time windows
      2. A pet class which holds pet name, species, breed, age, weight, health conditions. (An owner may have more than one pet).
      3. A task class which belongs to a Owner and optinally linked to pet
      4. Schedular 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

      The following changes were made after the initial creation:

      1. I made changes during the plan phase. I asked the LLM to generate the plan and classes. First, it suggested to have Task belong to Pet class. When I questioned it about why Pet class and not User, as user is someone who creates a task and may link to a particular pet if needed, it made the change. 
      2. It also added pet as a string in Task class which was later converted to a reference to pet object, so that the changes in pet are reflected everywhere in the app and there is no stale data.
      3. Changed time field from string to datetime in Task class.
      4. Earlier for task only completed status was used. The code just checked if the task is completed or not. Converted it to use pre-defined status (Pending, Completed, Postponed, Cancelled) through enum.
      5. Changed priority from string to enum to support "Low", "Medium", "High", "Critical", so that the user doesn't enter any incorrect value.
      6. Added support for tasks without a set time — the scheduler places them at the bottom sorted by priority instead of requiring a time for every task.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

      The scheduler considers the following constraints:
      1. **Time** — Tasks are sorted chronologically by their scheduled time. This is the primary sort key because a pet owner's day revolves around when things need to happen (morning walk, evening medication, etc.).
      2. **Priority** — Within the same time slot, tasks are sorted by priority (Critical > High > Medium > Low). This ensures that if two tasks compete for the same window, the more important one surfaces first.
      3. **Duration** — Task durations are used for conflict detection. Two tasks conflict if their time ranges (start + duration) overlap, not just if they share the same start time.
      4. **Frequency** — The scheduler checks whether a task is one-time, daily, or weekly to determine if it should appear on a given date.
      5. **Status** — Only pending tasks are included in the generated schedule. Completed, postponed, and cancelled tasks are excluded.

      Time and priority were chosen as the primary constraints because they most directly affect a pet owner's ability to execute a plan. A schedule that ignores time is unusable, and one that ignores priority risks missing critical tasks like medication.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

      1. **No automatic conflict resolution** — The scheduler detects and warns about conflicts but does not automatically reschedule or reorder tasks to resolve them. The user must manually adjust times. This is reasonable because pet care is personal — only the owner knows whether "walk" can be moved but "medication" cannot. Automatic rescheduling could make unsafe assumptions about flexible vs. fixed tasks.
      2. **Simple recurrence model** — The system only supports "once", "daily", and "weekly" frequencies. More complex patterns (e.g., every 3 days, twice a week) are not supported. This keeps the logic simple and covers the most common pet care patterns without overcomplicating the UI.
      3. **Tasks without a time are unranked in the schedule** — They appear at the bottom sorted by priority but have no specific slot. This trades precision for flexibility, allowing owners to add tasks like "give bath sometime today" without forcing a fake time.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

      1. **Design phase** — Used the LLM to brainstorm the initial class structure and generate a UML diagram. Asking it to propose classes and relationships gave a starting point, which I then refined through questioning.
      2. **Implementation** — Used AI to generate the core scheduling logic (sorting, conflict detection, recurring tasks) and the Streamlit UI. The most helpful prompts were specific ones like "detect time conflicts using duration, not just start time" rather than vague ones like "make the scheduler better."
      3. **UI improvements** — Asked for concrete suggestions to improve the UI, then selected the high-impact changes (custom CSS theming, tabbed layout, styled dataframes, color-coded badges) to implement.
      4. **Debugging** — When the schedule crashed on tasks without a time, the AI identified the root cause (sorting `None` vs `time` objects) and proposed handling it gracefully instead of just requiring the field.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

      1. The LLM initially suggested that Task should belong to the Pet class. I questioned this because a user is the one who creates tasks and a task may or may not be linked to a specific pet. After I pushed back, the AI agreed and moved task ownership to the Owner class with an optional pet reference. I evaluated this by thinking through the real-world scenario: an owner might have a task like "buy pet food" that isn't tied to any specific pet.
      2. When the AI suggested making time a required field for scheduling, I asked whether that was really the best approach. It agreed that handling optional time gracefully was better UX, and proposed placing untimed tasks at the bottom of the schedule instead.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

      The 22 tests cover the core scheduling logic:
      1. **Task status lifecycle** — Verifying that `mark_complete()`, `mark_postponed()`, and `mark_cancelled()` correctly transition task state. Important because the schedule only shows pending tasks, so status transitions must work correctly.
      2. **Owner/pet management** — Adding and removing pets and tasks. Important because these are the building blocks the rest of the system depends on.
      3. **Sorting** — Sort by time, sort by priority, and composite sorting (time first, then priority). Important because the schedule's usefulness depends entirely on correct ordering.
      4. **Date-based scheduling** — Tasks appear on the correct date, completed tasks are excluded, empty lists are handled. Important for daily schedule generation.
      5. **Recurring tasks** — Daily tasks appear on future dates, weekly tasks match the correct weekday, one-time tasks don't repeat, cloned tasks get the correct next date and a new unique ID. Important because incorrect recurrence would create duplicate or missing tasks.
      6. **Conflict detection** — Overlapping time ranges are flagged, non-overlapping tasks pass, back-to-back tasks (end time equals start time) don't false-positive. Important because incorrect conflict warnings would erode user trust.
      7. **Filtering** — Filter by pet and filter by status return the correct subset. Important for usability when the task list grows.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

      **Confidence: 4/5** — The core scheduling logic is thoroughly covered by unit tests. The main gap is UI-level integration testing (Streamlit widget interactions, session state persistence across reruns).

      Edge cases I would test next:
      1. Tasks with `time=None` in sorting and conflict detection
      2. A large number of tasks (50+) to check performance of conflict detection (currently O(n^2))
      3. Recurring tasks that span month/year boundaries
      4. Multiple tasks at the exact same time with the same priority
      5. Removing a pet that has tasks linked to it

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

      The clean separation between domain logic (`pawpal_system.py`) and UI (`app.py`). The Scheduler class has no knowledge of Streamlit, which made it easy to test independently and swap the UI approach (from a single scrolling page to a tabbed layout) without touching any scheduling logic. The enum-based design for Category, Priority, and TaskStatus also prevented many potential bugs by constraining values at the type level.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

      1. **Automatic conflict resolution** — Instead of just warning about conflicts, offer suggestions to reschedule (e.g., "Move 'walk' to 3:30 PM to avoid overlap with 'medication'").
      2. **Persistent storage** — Currently all data lives in Streamlit session state and is lost on page refresh. Adding a database (even SQLite) would make the app actually usable day-to-day.
      3. **Richer recurrence** — Support patterns like "every other day", "Mon/Wed/Fri", or custom intervals.
      4. **Edit and delete tasks from the UI** — Currently tasks can only be added. The Owner class supports `remove_task()` but it's not wired to the UI.
      5. **O(n^2) conflict detection** — For a large number of tasks, the current nested loop approach could be slow. An interval-based approach would scale better.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

      AI is a strong first-draft generator but a poor decision-maker. It will confidently suggest designs (like putting Task inside Pet) that fall apart under scrutiny. The most productive workflow was to let the AI propose a structure, then question every relationship and responsibility by asking "why this way and not that way?" The AI corrected course quickly once challenged, but it would not have caught the issue on its own. The lesson is to treat AI output as a starting point for critical review, not as a finished answer.
