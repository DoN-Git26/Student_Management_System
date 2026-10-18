# Attendance Management System

An object-oriented Python project for managing students, teachers, classrooms and attendance records. Users have roles (student, teacher, administrator) and each role can perform its own set of actions.

## Status

| Component | State |
|-----------|-------|
| Domain models (`User`, `Student`, `Teacher`, `Administrator`, `Classroom`, `Attendance`) | Implemented, in memory |
| Unit tests (`tests/`) | One test per model |
| JSON persistence (`storage.py`, `data/records.json`) | Placeholder, not implemented yet |
| CLI (`main.py`) | Placeholder, not implemented yet |

Data currently lives only in memory and is lost when the program exits.

## Project structure

```
attendance_system/
├── main.py                    # CLI entry point (placeholder)
├── attendance_system/         # Core package
│   ├── __init__.py
│   ├── user.py                # User superclass
│   ├── student.py             # Student subclass
│   ├── teacher.py             # Teacher subclass
│   ├── administrator.py       # Administrator subclass
│   ├── classroom.py           # Classroom class
│   ├── attendance.py          # Attendance class
│   └── storage.py             # JSON persistence (placeholder)
├── data/
│   └── records.json           # Persistent storage (placeholder)
├── tests/
│   ├── test_user.py
│   ├── test_student.py
│   ├── test_teacher.py
│   ├── test_admin.py
│   ├── test_classroom.py
│   └── test_attendance.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer (developed on 3.12)
- `pytest` for running the tests

```bash
pip install -r requirements.txt
```

`requirements.txt` also lists `argparse`, which is part of the Python standard library and does not need installing.

## Design

Each model keeps a class-level registry of every instance created:

| Registry | Holds |
|----------|-------|
| `User.all_users` | Every user (students, teachers, administrators) |
| `Classroom.all_classes` | Every classroom |
| `Attendance.all_records` | Every attendance record |

```
User
├── Student
├── Teacher
└── Administrator

Classroom ── has one Teacher, many Students
Attendance ── links one Student, one Classroom, a date and a status
```

### `User` (`user.py`)

Base class. Attributes: `first_name`, `last_name`, `email`, `role`.

| Method | Description |
|--------|-------------|
| `get_full_name()` | Returns `"First Last"` |
| `view_profile()` | Returns a dict with `Name`, `Email`, `Role` |
| `User.register_user(first, last, email, role)` | Creates a user (class method) |
| `User.find_user(email)` | Finds a registered user by email, or `None` |

### `Student` (`student.py`)

Extends `User` with role `"student"`, a `student_id` and `enrolled_classes`.

| Method | Description |
|--------|-------------|
| `register_for_class(classroom)` | Enrols in a classroom and adds the student to its roster |
| `mark_attendance(classroom, date, status)` | Creates an attendance record |
| `view_attendance_history()` | Returns the student's attendance records as dicts |

### `Teacher` (`teacher.py`)

Extends `User` with role `"teacher"`, a `teacher_id` and `assigned_classes`.

| Method | Description |
|--------|-------------|
| `view_students(classroom)` | Names of students in a classroom |
| `view_daily_attendance(classroom, date)` | Attendance records for a class on a date |
| `view_student_history(student)` | A student's attendance records |
| `generate_attendance_report(classroom)` | Attendance details for every record in a class |

### `Administrator` (`administrator.py`)

Extends `User` with role `"admin"` and an `admin_id`.

| Method | Description |
|--------|-------------|
| `add_student(student)` | Adds a student to the user registry |
| `update_student(student, **fields)` | Updates student attributes, e.g. `first_name="Johnny"` |
| `remove_student(student)` | Removes a student from the user registry |
| `create_class(class_id, class_name, teacher)` | Creates a classroom |
| `view_all_attendance()` | Returns every attendance record |
| `generate_report()` | Attendance details for all records |

### `Classroom` (`classroom.py`)

Attributes: `class_id`, `class_name`, `teacher`, `students`.

| Method | Description |
|--------|-------------|
| `add_student(student)` / `remove_student(student)` | Manage the roster |
| `get_student_list()` | Full names of enrolled students |

### `Attendance` (`attendance.py`)

Attributes: `student`, `classroom`, `date`, `status`.

| Method | Description |
|--------|-------------|
| `mark_present()` / `mark_absent()` | Set status to `"Present"` / `"Absent"` |
| `update_status(status)` | Set any status |
| `get_attendance_details()` | Dict with `Student`, `Class`, `Date`, `Status` |
| `Attendance.find_record(student, classroom, date)` | Finds a specific record or `None` |
| `Attendance.get_student_records(student)` | All records for a student, as dicts |

## Usage example

Run from the project root so the `attendance_system` package is importable:

```python
from attendance_system.administrator import Administrator
from attendance_system.teacher import Teacher
from attendance_system.student import Student

admin = Administrator("Grace", "Lee", "grace@example.com", "A001")
teacher = Teacher("Alice", "Smith", "alice@example.com", "T001")
student = Student("John", "Doe", "john@example.com", "S001")

math = admin.create_class("C101", "Math", teacher)
student.register_for_class(math)
student.mark_attendance(math, "2026-10-18", "Present")

print(teacher.view_students(math))                                  # ['John Doe']
print(teacher.view_daily_attendance(math, "2026-10-18")[0].status)  # Present
print(student.view_attendance_history())
print(admin.generate_report())
```

## Running the tests

```bash
python3 -m pytest
```

## Known limitations

- `main.py`, `storage.py` and `data/records.json` are empty; there is no CLI and no persistence yet.
- `User.register_user` always returns a plain `User`, even for the `"student"`, `"teacher"` or `"admin"` roles.
- Registries are class-level lists shared across the whole process, so tests that create users or classes see each other's data. `tests/test_user.py` currently fails when run after other tests because `find_user` returns an earlier user with the same email.
- `Administrator.add_student` does not check for duplicates, so adding a student who is already registered creates a second entry.
- There is no authentication or role enforcement; any object can call any method.
- Attendance status and dates are not validated, and duplicate records for the same student, class and date are allowed.

## Planned work

- JSON save/load in `storage.py` backed by `data/records.json`
- An interactive CLI in `main.py`
- Role-based access control and input validation
