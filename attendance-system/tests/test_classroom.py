import pytest
from attendance_system.classroom import Classroom
from attendance_system.teacher import Teacher
from attendance_system.student import Student

def test_classroom_add_and_remove_student():
    teacher = Teacher("Alice", "Smith", "alice@example.com", "T001")
    classroom = Classroom("C101", "Math", teacher)
    student = Student("John", "Doe", "john@example.com", "S001")

    classroom.add_student(student)
    assert student in classroom.students

    classroom.remove_student(student)
    assert student not in classroom.students
