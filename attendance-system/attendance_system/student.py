from attendance_system.user import User

class Student(User):
    def __init__(self, first_name, last_name, email, student_id):
        super().__init__(first_name, last_name, email, "student")
        self.student_id = student_id
        self.enrolled_classes = []

    def register_for_class(self, classroom):
        self.enrolled_classes.append(classroom)
        classroom.add_student(self)

    def mark_attendance(self, classroom, date, status):
        from attendance_system.attendance import Attendance
        Attendance(self, classroom, date, status)

    def view_attendance_history(self):
        from attendance_system.attendance import Attendance
        return Attendance.get_student_records(self)
