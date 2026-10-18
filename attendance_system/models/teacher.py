"""Teacher subclass."""

from models.attendance import Attendance
from models.user import User


class Teacher(User):
    """A teacher who manages the attendance of their own classes."""

    ROLE = "teacher"
    PREFIX = "T"

    def __init__(self, first_name, last_name, email, teacher_id=None, password_hash=""):
        self.assigned_classes = []
        super().__init__(first_name, last_name, email, teacher_id, password_hash)

    @property
    def teacher_id(self):
        return self.user_id

    def view_students(self, classroom):
        """Return the names of students in a class."""
        return classroom.get_student_list()

    def view_daily_attendance(self, classroom, date):
        """Return attendance records for a class on a date."""
        return [
            r for r in Attendance.all_records
            if r.classroom is classroom and r.date == date
        ]

    def view_student_history(self, student):
        """Return a student's attendance records as dicts."""
        return Attendance.get_student_records(student)

    def mark_attendance(self, student, classroom, date, status):
        """Mark a student's attendance in a class this teacher teaches."""
        if classroom.teacher is not self:
            raise ValueError("You can only mark attendance for your own classes.")
        return Attendance.mark(student, classroom, date, status)

    def generate_attendance_report(self, classroom):
        """Return attendance details for every record in a class."""
        return [
            r.get_attendance_details()
            for r in Attendance.all_records if r.classroom is classroom
        ]
