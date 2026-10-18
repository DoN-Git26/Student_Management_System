import pytest
from attendance_system.teacher import Teacher
from attendance_system.student import Student
from attendance_system.classroom import Classroom
from attendance_system.attendance import Attendance

def test_teacher_view_students_and_attendance():
    teacher = Teacher("Alice", "Smith", "alice@example.com", "T001")
    classroom = Classroom("C101", "Math", teacher)
    student = Student("John", "Doe", "john@example.com", "S001")
    classroom.add_student(student)

    Attendance(student, classroom, "2026-10-18", "Present")

    assert "John Doe" in teacher.view_students(classroom)
    daily = teacher.view_daily_attendance(classroom, "2026-10-18")
    assert daily[0].status == "Present"
