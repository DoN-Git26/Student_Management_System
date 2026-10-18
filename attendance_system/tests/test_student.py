import pytest

from models.student import Student


def test_student_register_for_class(school):
    _, student, classroom = school
    other = Student("Jane", "Roe", "jane@example.com")
    other.register_for_class(classroom)
    assert other in classroom.students
    assert classroom in other.enrolled_classes
    assert other.student_id == "S002"


def test_student_marks_and_views_attendance(school):
    _, student, classroom = school
    student.mark_attendance(classroom, "2026-10-18", "present")
    assert student.view_attendance_history()[0]["Status"] == "Present"


def test_student_cannot_mark_unenrolled_class(school):
    _, _, classroom = school
    outsider = Student("Out", "Sider", "out@example.com")
    with pytest.raises(ValueError):
        outsider.mark_attendance(classroom, "2026-10-18", "Present")
