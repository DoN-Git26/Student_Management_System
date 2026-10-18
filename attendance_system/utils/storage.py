"""JSON persistence for users, classrooms and attendance records."""

import json
import os
from pathlib import Path

from models.attendance import Attendance
from models.classroom import Classroom
from models.user import User

DB_FILE = Path(__file__).resolve().parent.parent / "data" / "records.json"


class StorageError(Exception):
    """Raised when data cannot be saved."""


def reset_registries():
    """Empty every in-memory registry."""
    User.all_users.clear()
    Classroom.all_classes.clear()
    Attendance.all_records.clear()


def _snapshot():
    """Return all registries as a JSON-ready dict."""
    return {
        "users": [u.to_dict() for u in User.all_users],
        "classrooms": [c.to_dict() for c in Classroom.all_classes],
        "attendance": [r.to_dict() for r in Attendance.all_records],
    }


def save(path=None):
    """Write all data to disk atomically."""
    path = Path(path or DB_FILE)
    tmp = path.with_suffix(".tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(_snapshot(), indent=2), encoding="utf-8")
        os.replace(tmp, path)
    except OSError as exc:
        raise StorageError(f"Could not save data: {exc}") from exc


def _restore(data):
    """Rebuild registries from a loaded dict (raises on bad data)."""
    for item in data.get("users", []):
        User.from_dict(item)
    for item in data.get("classrooms", []):
        teacher = User.find_user(item["teacher"])
        classroom = Classroom(item["class_id"], item["class_name"], teacher)
        for email in item.get("students", []):
            classroom.add_student(User.find_user(email))
    for item in data.get("attendance", []):
        Attendance(
            User.find_user(item["student"]),
            Classroom.find(item["class_id"]),
            item["date"],
            item["status"],
        )


def load(path=None):
    """Load data from disk; a missing file starts empty, a corrupt one is set aside."""
    path = Path(path or DB_FILE)
    reset_registries()
    if not path.exists():
        return
    try:
        _restore(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        reset_registries()
        backup = path.with_suffix(".corrupt")
        try:
            os.replace(path, backup)
        except OSError:
            pass
        print(f"Warning: could not read {path.name} ({exc}); starting empty. "
              f"The old file was kept as {backup.name}.")
