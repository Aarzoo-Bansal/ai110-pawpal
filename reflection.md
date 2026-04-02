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
      5. Changee priority from string to enum to support "Low", "Medium", "High", "Critical", so that the user doesn't enter any incorrect value.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
