import pytest

from models.administrator import Administrator
from models.attendance import Attendance
from models.classroom import Classroom
from models.student import Student
from models.teacher import Teacher
from models.user import User


def test_admin_manage_users_and_classes():
    admin = Administrator("Grace", "Lee", "grace@example.com")
    student = Student("John", "Doe", "john@example.com")
    teacher = Teacher("Alice", "Smith", "alice@example.com")

    admin.add_user(student)
    assert User.all_users.count(student) == 1

    classroom = admin.create_class("C101", "Math", teacher)
    assert classroom in Classroom.all_classes

    admin.update_user(student, first_name="Johnny")
    assert student.first_name == "Johnny"
    with pytest.raises(ValueError):
        admin.update_user(student, role="admin")

    admin.remove_user(student)
    assert student not in User.all_users


def test_remove_student_cleans_links_and_records(school):
    teacher, student, classroom = school
    admin = Administrator("Grace", "Lee", "grace@example.com")
    Attendance(student, classroom, "2026-10-18", "Present")
    admin.remove_user(student)
    assert student not in classroom.students
    assert admin.view_all_attendance() == []


def test_admin_cannot_remove_admin_or_busy_teacher(school):
    teacher, _, _ = school
    admin = Administrator("Grace", "Lee", "grace@example.com")
    with pytest.raises(ValueError):
        admin.remove_user(admin)
    with pytest.raises(ValueError):
        admin.remove_user(teacher)


def test_admin_report(school):
    _, student, classroom = school
    admin = Administrator("Grace", "Lee", "grace@example.com")
    Attendance(student, classroom, "2026-10-18", "Absent")
    assert admin.generate_report()[0]["Student"] == "John Doe"
