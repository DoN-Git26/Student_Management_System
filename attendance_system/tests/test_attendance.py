import pytest

from models.attendance import Attendance


def test_attendance_mark_and_find(school):
    _, student, classroom = school
    record = Attendance(student, classroom, "2026-10-18", "Absent")
    record.mark_present()
    assert record.status == "Present"
    assert Attendance.find_record(student, classroom, "2026-10-18") is record
    assert Attendance.get_student_records(student)[0]["Status"] == "Present"


def test_mark_updates_existing_record(school):
    _, student, classroom = school
    Attendance.mark(student, classroom, "2026-10-18", "Absent")
    Attendance.mark(student, classroom, "2026-10-18", "Late")
    assert len(Attendance.all_records) == 1
    assert Attendance.all_records[0].status == "Late"


def test_invalid_date_status_and_duplicate(school):
    _, student, classroom = school
    with pytest.raises(ValueError):
        Attendance(student, classroom, "18/10/2026", "Present")
    with pytest.raises(ValueError):
        Attendance(student, classroom, "2026-10-18", "Sleeping")
    Attendance(student, classroom, "2026-10-18", "Present")
    with pytest.raises(ValueError):
        Attendance(student, classroom, "2026-10-18", "Absent")
