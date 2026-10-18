import pytest

from models.attendance import Attendance
from models.teacher import Teacher


def test_teacher_view_students_and_attendance(school):
    teacher, student, classroom = school
    Attendance(student, classroom, "2026-10-18", "Present")
    assert "John Doe" in teacher.view_students(classroom)
    daily = teacher.view_daily_attendance(classroom, "2026-10-18")
    assert daily[0].status == "Present"
    assert teacher.view_student_history(student)[0]["Class"] == "Math"


def test_teacher_marks_own_class_only(school):
    teacher, student, classroom = school
    teacher.mark_attendance(student, classroom, "2026-10-18", "Late")
    assert teacher.generate_attendance_report(classroom)[0]["Status"] == "Late"
    other = Teacher("Bob", "Brown", "bob@example.com")
    with pytest.raises(ValueError):
        other.mark_attendance(student, classroom, "2026-10-19", "Present")
