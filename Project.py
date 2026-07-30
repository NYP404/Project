import numpy as np


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    __repr__ = __str__


class Student(Person):
    def __init__(self, first_name, last_name, ID, courses_and_grades=None):
        super().__init__(first_name, last_name)
        self.__ID = ID
        self.courses_and_grades = {} if courses_and_grades is None else dict(courses_and_grades)

    @property
    def ID(self):
        return self.__ID

    def add_course(self, course, grade):
        self.courses_and_grades[course] = grade

    def remove_course(self, course):
        if course not in self.courses_and_grades:
            raise ValueError(f"{course.name} is not in {self.full_name}'s courses")
        del self.courses_and_grades[course]

    def calculate_gpa(self):
        if not self.courses_and_grades:
            return 0.0

        total_units = sum(course.unit for course in self.courses_and_grades.keys())
        if total_units == 0:
            return 0.0

        weighted_sum = sum(
            grade * course.unit
            for course, grade in self.courses_and_grades.items()
        )
        return weighted_sum / total_units

    def __eq__(self, other):
        return self.ID == other.ID

    def __str__(self):
        return f"{self.full_name} | ID: {self.ID} | GPA: {self.calculate_gpa():.2f}"

    __repr__ = __str__


class Course:
    def __init__(self, name, ID, unit):
        self.name = name
        self.__ID = ID
        self.unit = unit

    @property
    def ID(self):
        return self.__ID

    def __str__(self):
        return f"{self.name} ({self.unit}) | ID: {self.ID}"

    __repr__ = __str__


class Management:
    population = 0

    def __init__(self, students=None, courses=None):
        self.students = list(students) if students is not None else []
        self.courses = list(courses) if courses is not None else []
        Management.population = len(self.students)

    def _find_student(self, student):
        student_id = student.ID if isinstance(student, Student) else student
        for s in self.students:
            if s.ID == student_id:
                return s
        return None

    def _find_course(self, course):
        course_id = course.ID if isinstance(course, Course) else course
        for c in self.courses:
            if c.ID == course_id:
                return c
        return None

    def add_student(self, new_student):
        if self._find_student(new_student) is not None:
            raise ValueError("this student already exists!")
        self.students.append(new_student)
        Management.population += 1

    def remove_student(self, student):
        student_obj = self._find_student(student)
        if student_obj is None:
            raise ValueError("this student doesn't exist!")

        self.students.remove(student_obj)
        Management.population -= 1

    def add_course(self, new_course):
        if self._find_course(new_course) is not None:
            raise ValueError("this course already exists!")
        self.courses.append(new_course)

    def remove_course(self, course):
        course_obj = self._find_course(course)
        if course_obj is None:
            raise ValueError("this course doesn't exist!")

        self.courses.remove(course_obj)
        for student in self.students:
            student.courses_and_grades.pop(course_obj, None)

    def add_course_to_student(self, student, course, course_grade):
        student_obj = self._find_student(student)
        if student_obj is None:
            self.add_student(student)
            student_obj = student

        course_obj = self._find_course(course)
        if course_obj is None:
            self.add_course(course)
            course_obj = course

        student_obj.add_course(course_obj, course_grade)

    def remove_student_course(self, student, student_course):
        student_obj = self._find_student(student)
        if student_obj is None:
            raise ValueError("this student doesn't exist!")

        course_obj = self._find_course(student_course)
        if course_obj is None or course_obj not in student_obj.courses_and_grades:
            raise ValueError(f"{student_course.name} is not in {student_obj.full_name}'s courses")

        student_obj.remove_course(course_obj)

    def assign_grade(self, student, course, grade):
        student_obj = self._find_student(student)
        if student_obj is None:
            raise ValueError("this student doesn't exist!")

        course_obj = self._find_course(course)
        if course_obj is None:
            raise ValueError("this course doesn't exist!")

        student_obj.courses_and_grades[course_obj] = grade

    def get_transcript(self, student):
        student_obj = self._find_student(student)
        if student_obj is None:
            raise ValueError("this student doesn't exist!")

        lines = [
            f"Transcript for {student_obj.full_name}",
            f"ID: {student_obj.ID}",
            "-" * 35,
        ]

        if not student_obj.courses_and_grades:
            lines.append("No courses registered.")
        else:
            for course, grade in student_obj.courses_and_grades.items():
                lines.append(f"{course.name} ({course.unit}) -> {grade}")

        lines.append("-" * 35)
        lines.append(f"GPA: {student_obj.calculate_gpa():.2f}")
        return "\n".join(lines)

    @staticmethod
    def merge(left, right, key):
        result = []
        i, j = 0, 0

        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort(self, l, key=lambda x: x):
        if len(l) < 2:
            return l[:]

        middle = len(l) // 2
        left = self.merge_sort(l[:middle], key)
        right = self.merge_sort(l[middle:], key)
        return Management.merge(left, right, key)

    def sorted_by_GPAs(self):
        return self.merge_sort(
            self.students,
            key=lambda student: student.calculate_gpa()
        )

    def sorted_by_names(self):
        return self.merge_sort(
            self.students,
            key=lambda student: student.full_name.lower()
        )

    def sorted_courses(self):
        return self.merge_sort(
            self.courses,
            key=lambda course: course.unit
        )

    def sorted_courses_by_name(self):
        return self.merge_sort(
            self.courses,
            key=lambda course: course.name.lower()
        )

    def all_grades(self):
        return [
            grade
            for student in self.students
            for grade in student.courses_and_grades.values()
        ]

    def mean_grade(self):
        grades = np.array(self.all_grades(), dtype=float)
        return float(np.mean(grades)) if grades.size else 0.0

    def max_grade(self):
        grades = np.array(self.all_grades(), dtype=float)
        return float(np.max(grades)) if grades.size else 0.0

    def min_grade(self):
        grades = np.array(self.all_grades(), dtype=float)
        return float(np.min(grades)) if grades.size else 0.0

    def std_grade(self):
        grades = np.array(self.all_grades(), dtype=float)
        return float(np.std(grades)) if grades.size else 0.0

    def passed_failed_students(self, pass_mark=10):
        passed = 0
        failed = 0

        for student in self.students:
            if student.calculate_gpa() >= pass_mark:
                passed += 1
            else:
                failed += 1

        return passed, failed

    def analysis_report(self, pass_mark=10):
        passed, failed = self.passed_failed_students(pass_mark=pass_mark)
        return {
            "mean_grade": self.mean_grade(),
            "max_grade": self.max_grade(),
            "min_grade": self.min_grade(),
            "std_grade": self.std_grade(),
            "passed_students": passed,
            "failed_students": failed,
        }