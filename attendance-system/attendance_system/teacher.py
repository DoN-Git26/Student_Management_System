from attendance_system.user import User

class Teacher(User):
    def __init__(self, first_name, last_name, email, teacher_id):
        super().__init__(first_name, last_name, email, "teacher")
        self.teacher_id = teacher_id
        self.assigned_classes = []

    def view_students(self, classroom):
        return classroom.get_student_list()

    def view_daily_attendance(self, classroom, date):
        from attendance_system.attendance import Attendance
        return [rec for rec in Attendance.all_records if rec.classroom == classroom and rec.date == date]

    def view_student_history(self, student):
        from attendance_system.attendance import Attendance
        return Attendance.get_student_records(student)

    def generate_attendance_report(self, classroom):
        from attendance_system.attendance import Attendance
        return [rec.get_attendance_details() for rec in Attendance.all_records if rec.classroom == classroom]
