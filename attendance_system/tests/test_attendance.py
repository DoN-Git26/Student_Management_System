from attendance_system.attendance import Attendance
from attendance_system.student import Student
from attendance_system.teacher import Teacher
from attendance_system.classroom import Classroom

def test_attendance_mark_and_find():
    teacher = Teacher("Alice", "Smith", "alice@example.com", "T001")
    classroom = Classroom("C101", "Math", teacher)
    student = Student("John", "Doe", "john@example.com", "S001")

    record = Attendance(student, classroom, "2026-10-18", "Absent")
    record.mark_present()
    assert record.status == "Present"

    found = Attendance.find_record(student, classroom, "2026-10-18")
    assert found == record

    history = Attendance.get_student_records(student)
    assert history[0]["Status"] == "Present"
