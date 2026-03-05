# Summary: Getting Started with GitHub Copilot

This document summarizes the end-to-end hands-on lab experience from the **"Getting Started with GitHub Copilot"** GitHub Skills exercise. The lab is built around a real-world web application called the **Mergington High School Activities Portal**, a website that lets students sign up for extracurricular activities. Throughout the lab, GitHub Copilot is used as an AI pair-programmer to help explore, fix, extend, test, and review the codebase.

---

## 🗺️ Overview of the Lab

| Step | Title | Key Copilot Feature Used |
|------|-------|--------------------------|
| 1 | Hello Copilot | Ask Mode (Chat), Terminal Inline Chat |
| 2 | Getting Work Done | Inline Suggestions, Inline Chat, Commit Message Generation |
| 3 | Engage Hyperdrive | Agent Mode |
| 4 | Plan Your Implementation | Plan Agent |
| 5 | Pull Request with Copilot | PR Summary, Copilot Code Review |

---

## 🔧 The Project: Mergington High School Activities Portal

Before diving into the steps, it helps to understand what we are working with.

### What the App Does

The app is a simple web application with two main parts:

- **Backend (Python/FastAPI):** A REST API defined in `src/app.py` that stores a list of extracurricular activities in memory. It exposes endpoints to:
  - `GET /activities` — list all activities and their current participants
  - `POST /activities/{name}/signup` — sign a student up for an activity
  - `DELETE /activities/{name}/participants` — remove a student from an activity

- **Frontend (HTML/CSS/JavaScript):** Static files in `src/static/` that display the activities in a browser and provide a sign-up form.

### Project Structure

```
/
├── src/
│   ├── app.py            # FastAPI backend
│   └── static/
│       ├── index.html    # Main web page
│       ├── app.js        # Frontend JavaScript logic
│       └── styles.css    # Styling
├── tests/
│   ├── conftest.py       # Shared test fixtures
│   ├── test_activities.py
│   ├── test_signup.py
│   └── test_unregister.py
├── requirements.txt      # Python dependencies
└── pytest.ini            # Test configuration
```

### Technologies Used

| Technology | Role |
|------------|------|
| **Python** | Primary programming language for the backend |
| **FastAPI** | Web framework for building the REST API |
| **Uvicorn** | ASGI web server that runs the FastAPI app |
| **HTML/CSS/JS** | Frontend of the web application |
| **pytest** | Framework for writing and running automated tests |
| **GitHub Codespaces** | Cloud-hosted development environment used during the lab |
| **GitHub Copilot** | AI coding assistant integrated into VS Code |

---

## Step 1: Hello Copilot 👋

### Goal
Get familiar with GitHub Copilot and the project, then create a working branch.

### What is GitHub Copilot?

GitHub Copilot is an AI coding assistant built into your editor. You can think of it as a knowledgeable colleague sitting next to you who:
- Suggests code as you type (inline suggestions)
- Answers questions about your code (chat)
- Can autonomously write, edit, and test code (agent mode)

The main ways to interact with Copilot in VS Code are:

| Mode | What It Does | Best For |
|------|-------------|----------|
| **⚡ Inline Suggestions** | Suggests code as you type | Completing the current line or block |
| **💭 Inline Chat** | Chat scoped to the file or selection you have open | Targeted changes or explanations |
| **💬 Ask Mode** | Chat for questions about the codebase or tech topics | Understanding code, brainstorming |
| **🤖 Agent Mode** | Autonomous multi-step coding: reads files, runs commands, iterates | Full feature development |
| **🧭 Plan Agent** | Drafts a plan and asks questions before writing any code | Structured implementation |

### Activities Performed

1. **Opened a GitHub Codespace** — a fully configured cloud development environment that comes with VS Code, the GitHub Copilot extension, and the Python extension pre-installed. No local setup required!

2. **Used Ask Mode with `@workspace`** — A special *chat participant* that scans the project repository to provide relevant context. The prompt used was:
   ```
   @workspace Please briefly explain the structure of this project.
   What should I do to run it?
   ```
   Copilot responded with a plain-English explanation of the project files and how to run the server.

3. **Ran the application** using VS Code's Run and Debug panel, then opened the live website on port `8000` in a browser to see it working.

4. **Used Terminal Inline Chat** (`Ctrl+I` / `Cmd+I`) to ask Copilot how to create and publish a new Git branch:
   ```
   Hey copilot, how can I create and publish a new Git branch called "accelerate-with-copilot"?
   ```
   Copilot generated the correct `git` command, which was then run with one click.

### Key Takeaway
Copilot is a great onboarding tool. Instead of reading long documentation, you can simply ask it to explain a project, and it provides a tailored answer based on the actual code.

---

## Step 2: Getting Work Done with Copilot 🐛

### Goal
Use Copilot to find and fix a real bug, add sample data, and create a commit message.

### The Bug: Duplicate Activity Registration

Students could sign up for the same activity more than once! This is a data integrity bug in the `signup_for_activity` function in `src/app.py`.

**How Copilot helped find it:**

Using Ask Mode, we asked:
```
@workspace Students are able to register twice for an activity.
Where could this bug be coming from?
```
Copilot analyzed the codebase and identified that the `signup_for_activity` function in `src/app.py` was missing a check to see if the student was already registered.

**How Copilot helped fix it:**

Instead of writing the fix manually, we simply typed a descriptive comment in the right place:
```python
# Validate student is not already signed up
```
After pressing Enter, Copilot displayed a **shadow text suggestion** — a greyed-out block of code. Pressing `Tab` accepted the suggestion and inserted the logic automatically!

The resulting fix:
```python
# Validate student is not already signed up
if email in activity["participants"]:
    raise HTTPException(status_code=400, detail="Student is already signed up")
```

### Adding Sample Data with Inline Chat

A realistic dataset makes development and testing easier. Instead of manually writing Python dictionaries, we:

1. Selected the entire `activities` dictionary in `src/app.py`.
2. Opened **Inline Chat** (`Ctrl+I` / `Cmd+I`).
3. Entered the prompt:
   ```
   Add 2 more sports related activities, 2 more artistic activities, and 2 more intellectual activities.
   ```
4. Copilot generated six new activity entries with descriptions, schedules, and participant limits.
5. We reviewed the highlighted diff showing additions/removals, and clicked **Keep** to accept.

### Generating a Commit Message

After making changes, instead of writing a commit message manually:

1. Staged the changed file (`src/app.py`) in the Source Control panel.
2. Clicked the **Generate Commit Message** sparkle ✨ button next to the message box.
3. Copilot read the staged diff and proposed a descriptive commit message automatically.
4. Committed and pushed changes to the `accelerate-with-copilot` branch.

### Key Takeaway
Copilot's inline suggestions are powerful for small, targeted fixes. Providing a clear comment describing *what* you want to do is often enough to get a correct code suggestion. Inline Chat is ideal for scoped tasks on a specific file or code block.

---

## Step 3: Engage Hyperdrive — Copilot Agent Mode 🚀

### Goal
Use Agent Mode to build new features across multiple files.

### What is Agent Mode?

Agent Mode is the most autonomous way to use Copilot. It can:
- Understand a high-level request and break it into smaller tasks
- Read and edit multiple files
- Run terminal commands (with your approval)
- React to errors and fix them automatically
- Iterate until the task is done

### Activity 1: Display Participants on Activity Cards

The website listed activities but did not show who was signed up. We asked Copilot to add a participants section:

```
Hey Copilot, can you please edit the activity cards to add a participants section.
It will show what participants that are already signed up for that activity as a bulleted list.
Remember to make it pretty!
```

We provided the three frontend files as context by dragging them into the chat panel:
- `src/static/app.js`
- `src/static/index.html`
- `src/static/styles.css`

Copilot edited all the necessary files to render a participants list under each activity card.

### Activity 2: Add Unregister (Delete) Buttons

We then asked Copilot to add delete functionality:

```
#codebase Please add a delete icon next to each participant and hide the bullet points.
When clicked, it will unregister that participant from the activity.
```

The `#codebase` chat variable told Copilot to search the whole project for relevant files. Copilot:
- Added a delete button (with an icon) next to each participant's name in the frontend
- Added a new `DELETE /activities/{name}/participants` API endpoint in `src/app.py`
- Wired the frontend button to call the new API endpoint

### Activity 3: Fix a UI Refresh Bug

After testing the registration flow, we noticed that signing up did not immediately update the page:

```
I've noticed there seems to be a bug.
When a participant is registered, the page must be refreshed to see the change on the activity.
```

Copilot identified the root cause (the page was not refetching data after a successful signup) and updated the frontend JavaScript to call `fetchActivities()` after each signup or unregister action.

### Reviewing and Accepting Changes

After each Agent Mode session:
- Changed files were highlighted with a diff view
- We verified the results in the live browser preview
- We clicked **Keep** to accept or gave follow-up feedback to refine the results
- All changes were committed and pushed to the `accelerate-with-copilot` branch

### Key Takeaway
Agent Mode is ideal for feature-level tasks that span multiple files. Providing sufficient context (via file references or `#codebase`) helps Copilot make more accurate changes with fewer follow-up corrections.

---

## Step 4: Plan Your Implementation with Plan Agent 🧭

### Goal
Use the Plan Agent to design and then implement automated backend tests.

### What is Plan Agent?

Plan Agent is designed for situations where you want to *think before you code*. Unlike Agent Mode, it:
- Only reads your codebase — it does **not** make edits
- Asks clarifying questions to better understand your requirements
- Produces a structured implementation plan for you to review
- Hands off to **Agent Mode** when you click **Start Implementation**

### Why Write Tests?

At this point in the lab, the backend had no automated tests. Tests are important because:
- They verify that the code does what it is supposed to do
- They catch regressions (unintentional breakages) when you make future changes
- They serve as living documentation of expected behavior

### The Testing Approach: AAA Pattern

The tests follow the **Arrange-Act-Assert (AAA)** pattern:

| Phase | What It Does |
|-------|-------------|
| **Arrange** | Set up any data or state needed for the test |
| **Act** | Call the function or API endpoint being tested |
| **Assert** | Check that the result matches what was expected |

### Activities Performed

1. Switched Copilot Chat to **Plan Agent** mode.
2. Submitted the initial prompt:
   ```
   I want to add backend FastAPI tests in a separate tests directory.
   ```
3. Refined the plan with follow-up prompts, such as:
   ```
   Let's use the AAA (Arrange-Act-Assert) testing pattern to structure our tests
   ```
   ```
   Make sure we use pytest and add it to requirements.txt file
   ```
4. Reviewed the final plan, then clicked **Start Implementation** to hand off to Agent Mode.
5. Watched Copilot create the `tests/` directory and write test files.
6. Verified all tests passed by running `pytest`.
7. Committed and pushed the new tests.

### What Was Tested

The resulting test suite covers these scenarios:

| Test File | What It Tests |
|-----------|--------------|
| `test_activities.py` | Listing activities returns data; caching headers are correct |
| `test_signup.py` | Successful signup; unknown activity (404); duplicate email (409); full activity (400) |
| `test_unregister.py` | Successful unregister; unknown activity (404); missing participant (404); case-insensitive matching |

### Key Takeaway
Plan Agent encourages a "measure twice, cut once" approach to development. It is especially useful for non-trivial tasks where getting the design right upfront leads to cleaner, more maintainable code.

---

## Step 5: Using GitHub Copilot Within a Pull Request 🔀

### Goal
Use Copilot's pull request features to summarize and review the changes before merging.

### Copilot PR Summary

Writing a good pull request description is important — it helps teammates (and your future self) understand *what* changed and *why*. Copilot can automate this:

1. Created a pull request on GitHub:
   - **Base branch:** `main`
   - **Compare branch:** `accelerate-with-copilot`
   - **Title:** `Improve student activity registration system`

2. In the PR description toolbar, clicked the **Copilot icon → Summary**.
3. Copilot scanned all the commits and file diffs and generated a structured summary describing the bug fix, new features, and tests added.

### Copilot Code Review

Before merging, asking Copilot to review the code provides an extra safety net:

1. In the **Reviewers** section of the PR sidebar, clicked **Request** next to the Copilot icon.
2. Copilot added inline review comments pointing out potential issues, code style suggestions, and things to verify.

> **Note:** Copilot pull request summary and code review features require a paid GitHub Copilot plan.

### Merging

After reviewing (and optionally addressing) Copilot's feedback, we clicked **Merge pull request** to complete the exercise.

### Key Takeaway
Copilot's PR features reduce friction in the code review process. Even if it doesn't catch everything, having an automated first pass helps surface simple issues quickly and keeps human reviewers focused on higher-level concerns.

---

## 🧠 Concepts Recap

Here is a quick reference of the key concepts and tools covered in this lab:

| Concept | Description |
|---------|-------------|
| **GitHub Copilot** | An AI coding assistant integrated into your code editor |
| **Inline Suggestions** | Code completions that appear as you type; accept with `Tab` |
| **Inline Chat** | Scoped AI chat triggered with `Ctrl+I` / `Cmd+I`; targets the current file or selection |
| **Ask Mode** | Conversational chat for questions; great with `@workspace` for project-level context |
| **Agent Mode** | Autonomous mode: Copilot reads files, runs commands, and iterates to complete tasks |
| **Plan Agent** | Designs a solution plan before making any code changes |
| **`@workspace`** | A chat participant that scans the whole repository for context |
| **`#codebase`** | A chat variable that tells Agent Mode to search the codebase for relevant files |
| **GitHub Codespaces** | A cloud-hosted development environment that requires no local setup |
| **FastAPI** | A modern Python web framework for building APIs |
| **pytest** | A Python testing framework for writing and running automated tests |
| **AAA Pattern** | Arrange-Act-Assert: a structured way to write clear, focused tests |
| **PR Summary** | A Copilot feature that auto-generates pull request descriptions from code diffs |
| **Copilot Code Review** | A Copilot feature that reviews a pull request and adds inline feedback |

---

## ✅ What We Built

By the end of the lab, the Mergington High School Activities Portal had been improved in the following ways:

- 🐛 **Bug fixed:** Students can no longer register for the same activity twice
- 📋 **More data:** Additional sample activities were added across sports, arts, and academics
- 👥 **Participants visible:** Activity cards now display who is signed up
- ❌ **Unregister feature:** A delete button allows removing a participant from an activity
- 🔄 **Live updates:** The page refreshes the activity list automatically after sign-up or unregister
- 🧪 **Tests added:** A full pytest suite covers the core signup, unregister, and activity listing functionality

---

*This exercise was completed using the [Getting Started with GitHub Copilot](https://github.com/skills/getting-started-with-github-copilot) GitHub Skills lab.*
