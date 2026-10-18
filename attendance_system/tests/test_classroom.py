import pytest

from models.classroom import Classroom
from models.student import Student
from models.teacher import Teacher


def test_classroom_add_and_remove_student(school):
    teacher, student, classroom = school
    assert student in classroom.students
    assert classroom in teacher.assigned_classes
    classroom.add_student(student)
    assert classroom.students.count(student) == 1
    classroom.remove_student(student)
    assert student not in classroom.students
    assert classroom not in student.enrolled_classes


def test_classroom_requires_teacher_and_unique_id(school):
    teacher, student, _ = school
    with pytest.raises(ValueError):
        Classroom("C102", "Art", student)
    with pytest.raises(ValueError):
        Classroom("C101", "Dup", teacher)


def test_only_students_can_enrol(school):
    teacher, _, classroom = school
    with pytest.raises(ValueError):
        classroom.add_student(teacher)


def test_find_and_student_list(school):
    _, _, classroom = school
    assert Classroom.find("C101") is classroom
    assert Classroom.find("nope") is None
    assert classroom.get_student_list() == ["John Doe"]
