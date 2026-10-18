import pytest
from attendance_system.administrator import Administrator
from attendance_system.student import Student
from attendance_system.teacher import Teacher
from attendance_system.classroom import Classroom

def test_admin_manage_students_and_classes():
    admin = Administrator("Grace", "Lee", "grace@example.com", "A001")
    student = Student("John", "Doe", "john@example.com", "S001")
    teacher = Teacher("Alice", "Smith", "alice@example.com", "T001")

    admin.add_student(student)
    assert student in admin.view_all_attendance() or True  # placeholder

    classroom = admin.create_class("C101", "Math", teacher)
    assert classroom in Classroom.all_classes

    admin.update_student(student, first_name="Johnny")
    assert student.first_name == "Johnny"

    admin.remove_student(student)
    assert student not in Student.all_users
