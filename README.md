# TaskFlow — Django 6 + Tailwind CDN Todo App

A creative, detail-rich todo list web application built with **Django 6** and **Tailwind CSS via CDN**. No APIs, no complications — just clean Django with beautiful styling.

---

## Features

- **Smart Dashboard** — Progress bar, 4 animated stat cards (Total, Active, Done, Urgent)
- **Priority System** — Low / Medium / High with color-coded badges and left-side strips
- **7 Categories** — Personal 🏠, Work 💼, Shopping 🛒, Health ❤️, Education 📚, Finance 💰, Other 📌
- **Search & Filters** — Search by title, filter by status / priority / category
- **Toggle Complete** — Click the circle to mark done with animated checkmark
- **Clear Completed** — Bulk delete all finished tasks in one click
- **Due Dates** — Date picker with overdue indicators
- **Animated UI** — Fade-in animations, hover lifts, pulsing urgent badges, smooth progress bar
- **Flash Messages** — Encouraging feedback on every action
- **Empty State** — Beautiful illustration when no tasks exist

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Adrian-rgb67/todo_list.git
cd todo_list
```

### 2. Create a virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### 3. Run the development server
```bash
python manage.py runserver
```

### 4. Open in browser
```
http://127.0.0.1:8000/
```

> **Note:** The SQLite database (`db.sqlite3`) is included with 6 sample tasks and an admin account. No migration needed for the sample data!

---

## Admin Access

```
URL:      http://127.0.0.1:8000/admin/
Username: admin
Password: admin123
```

---

## URL Routes

| Route | Action |
|---|---|
| `/` | Dashboard — list all tasks with stats & filters |
| `/create/` | Add a new task |
| `/update/<id>/` | Edit a task |
| `/delete/<id>/` | Delete a task (with confirmation) |
| `/toggle/<id>/` | Toggle task completed status |
| `/clear-completed/` | Bulk delete all completed tasks |

---

## Project Structure

```
todo_list/
├── manage.py
├── requirements.txt
├── db.sqlite3                  # Included — pre-loaded with sample data
├── todo_project/
│   ├── settings.py             # Django settings (Tailwind via CDN, no build step)
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── todo/
│   ├── models.py               # Task model with priority, category, due date
│   ├── views.py                # ListView, CreateView, UpdateView, DeleteView, toggle, clear
│   ├── forms.py                # TaskForm & TaskEditForm with Tailwind widgets
│   ├── urls.py                 # App URL routes
│   ├── admin.py                # Admin site registration
│   └── migrations/
│       └── 0001_initial.py
└── templates/
    ├── base.html               # Tailwind CDN, navbar, flash messages, footer
    └── todo/
        ├── task_list.html      # Dashboard with stats, filters, task cards
        ├── task_form.html      # Create task form
        ├── task_edit.html      # Edit task form with completed toggle
        └── task_confirm_delete.html  # Delete confirmation
```

---

## The Minimal Stack

| Package | Purpose |
|---|---|
| **Django 6** | The web framework — ORM, URL routing, templates, security |
| **Tailwind CSS (CDN)** | Utility-first CSS via `<script>` tag — zero build steps |
| **django-widget-tweaks** | Add Tailwind classes to Django form fields easily |

---

## Resetting the Database

If you want a fresh start:

```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

Built with ❤️ using Django 6 + Tailwind CSS
