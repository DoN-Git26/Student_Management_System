import pytest
from attendance_system.student import Student
from attendance_system.classroom import Classroom
from attendance_system.teacher import Teacher

def test_student_register_for_class():
    teacher = Teacher("Alice", "Smith", "alice@example.com", "T001")
    classroom = Classroom("C101", "Math", teacher)
    student = Student("John", "Doe", "john@example.com", "S001")

    student.register_for_class(classroom)
    assert student in classroom.students
    assert classroom in student.enrolled_classes
