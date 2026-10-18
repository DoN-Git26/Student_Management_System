class Attendance:
    all_records = []

    def __init__(self, student, classroom, date, status):
        self.student = student
        self.classroom = classroom
        self.date = date
        self.status = status
        Attendance.all_records.append(self)

    def mark_present(self):
        self.status = "Present"

    def mark_absent(self):
        self.status = "Absent"

    def update_status(self, status):
        self.status = status

    def get_attendance_details(self):
        return {
            "Student": self.student.get_full_name(),
            "Class": self.classroom.class_name,
            "Date": self.date,
            "Status": self.status
        }

    @classmethod
    def find_record(cls, student, classroom, date):
        return next((rec for rec in cls.all_records if rec.student == student and rec.classroom == classroom and rec.date == date), None)

    @classmethod
    def get_student_records(cls, student):
        return [rec.get_attendance_details() for rec in cls.all_records if rec.student == student]
