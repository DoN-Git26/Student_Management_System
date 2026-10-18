import json

from models.attendance import Attendance
from models.classroom import Classroom
from models.user import User
from utils import storage


def test_save_and_load_roundtrip(school, tmp_path):
    _, student, classroom = school
    Attendance(student, classroom, "2026-10-18", "Present")
    path = tmp_path / "db.json"
    storage.save(path)

    storage.load(path)
    assert [u.email for u in User.all_users] == ["alice@example.com", "john@example.com"]
    loaded = Classroom.find("C101")
    assert loaded.teacher.email == "alice@example.com"
    assert loaded.students[0].enrolled_classes == [loaded]
    assert Attendance.all_records[0].status == "Present"


def test_missing_file_starts_empty(tmp_path):
    storage.load(tmp_path / "missing.json")
    assert User.all_users == []


def test_malformed_file_is_set_aside(tmp_path):
    path = tmp_path / "db.json"
    path.write_text("{not json", encoding="utf-8")
    storage.load(path)
    assert User.all_users == []
    assert (tmp_path / "db.corrupt").exists()


def test_bad_references_are_treated_as_malformed(tmp_path):
    path = tmp_path / "db.json"
    path.write_text(json.dumps({"classrooms": [
        {"class_id": "C1", "class_name": "X", "teacher": "ghost@example.com"}]}))
    storage.load(path)
    assert Classroom.all_classes == []
