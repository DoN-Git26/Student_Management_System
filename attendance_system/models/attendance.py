"""Attendance class."""

from datetime import datetime

STATUSES = ("Present", "Absent", "Late")


class Attendance:
    """One student's attendance status in one class on one date."""

    all_records = []

    def __init__(self, student, classroom, date, status):
        """Create a record; one record per student, class and date."""
        self.date = date
        self.status = status
        if Attendance.find_record(student, classroom, self.date):
            raise ValueError("An attendance record already exists for that day.")
        self.student = student
        self.classroom = classroom
        Attendance.all_records.append(self)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        """Accept only YYYY-MM-DD dates."""
        try:
            datetime.strptime(str(value), "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date '{value}'. Use YYYY-MM-DD.") from None
        self._date = str(value)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        """Accept Present, Absent or Late (case-insensitive)."""
        normalised = str(value).strip().capitalize()
        if normalised not in STATUSES:
            raise ValueError(f"Invalid status '{value}'. Use {', '.join(STATUSES)}.")
        self._status = normalised

    def mark_present(self):
        """Set status to Present."""
        self.status = "Present"

    def mark_absent(self):
        """Set status to Absent."""
        self.status = "Absent"

    def update_status(self, status):
        """Set a new validated status."""
        self.status = status

    def get_attendance_details(self):
        """Return the record as a dict for display."""
        return {
            "Student": self.student.get_full_name(),
            "Class": self.classroom.class_name,
            "Date": self.date,
            "Status": self.status,
        }

    def to_dict(self):
        """Serialise the record for JSON storage."""
        return {
            "student": self.student.email,
            "class_id": self.classroom.class_id,
            "date": self.date,
            "status": self.status,
        }

    @classmethod
    def mark(cls, student, classroom, date, status):
        """Create or update a record; the student must be enrolled."""
        if student not in classroom.students:
            raise ValueError(
                f"{student.get_full_name()} is not enrolled in {classroom.class_id}."
            )
        record = cls.find_record(student, classroom, date)
        if record is None:
            return cls(student, classroom, date, status)
        record.update_status(status)
        return record

    @classmethod
    def find_record(cls, student, classroom, date):
        """Return the matching record, or None."""
        return next(
            (r for r in cls.all_records
             if r.student is student and r.classroom is classroom and r.date == str(date)),
            None,
        )

    @classmethod
    def get_student_records(cls, student):
        """Return a student's records as dicts."""
        return [r.get_attendance_details() for r in cls.all_records if r.student is student]

    @classmethod
    def remove_for_student(cls, student):
        """Delete all records belonging to a student."""
        cls.all_records[:] = [r for r in cls.all_records if r.student is not student]
