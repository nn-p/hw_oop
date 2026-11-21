class Student:
    """Класс студента."""
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}  # {название_курса: [оценки за ДЗ]}

    def rate_hw(self, reviewer, course, grade):
        """Студент не может оценивать — это делает только Reviewer."""
        return 'Ошибка: студент не может оценивать!'

    def rate_lecture(self, lecturer, course, grade):
        """
        Студент выставляет оценку лектору за лекцию.
        Условия:
        - lecturer должен быть экземпляром класса Lecturer
        - курс должен быть в courses_in_progress у студента
        - курс должен быть в courses_attached у лектора
        """
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: оценивать можно только лекторов!'
        if course not in self.courses_in_progress:
            return 'Ошибка: студент не изучает этот курс!'
        if course not in lecturer.courses_attached:
            return 'Ошибка: лектор не ведёт этот курс!'

        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]

    def _average_grade(self):
        """Вспомогательный метод для подсчёта средней оценки за ДЗ."""
        all_grades = [g for grades_list in self.grades.values() for g in grades_list]
        if not all_grades:
            return 0
        return round(sum(all_grades) / len(all_grades), 2)

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self._average_grade()}\n"
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
            f"Завершенные курсы: {', '.join(self.finished_courses)}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Mentor:
    """Родительский класс для всех наставников."""
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Reviewer(Mentor):
    """Эксперт, проверяющий домашние задания."""
    def rate_hw(self, student, course, grade):
        """
        Reviewer выставляет оценку студенту за домашнее задание.
        Условия:
        - student должен быть экземпляром Student
        - курс должен быть в courses_attached у Reviewer
        - курс должен быть в courses_in_progress у студента
        """
        if isinstance(student, Student) and \
                course in self.courses_attached and \
                course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка: студент или курс не соответствуют условиям!'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    """Лектор, ведущий курсы."""
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # {название_курса: [оценки за лекции]}

    def _average_grade(self):
        """Вспомогательный метод для подсчёта средней оценки за лекции."""
        all_grades = [g for grades_list in self.grades.values() for g in grades_list]
        if not all_grades:
            return 0
        return round(sum(all_grades) / len(all_grades), 2)

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {self._average_grade()}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() == other._average_grade()


# ==================== ПРОВЕРКА ====================
if __name__ == '__main__':
    # --- Задание №1: проверка наследования ---
    lecturer = Lecturer('Иван', 'Иванов')
    reviewer = Reviewer('Пётр', 'Петров')
    print(isinstance(lecturer, Mentor))   # True
    print(isinstance(reviewer, Mentor))   # True
    print(lecturer.courses_attached)      # []
    print(reviewer.courses_attached)      # []

    # --- Задание №2: взаимодействие классов ---
    student = Student('Ольга', 'Алёхина', 'Ж')

    student.courses_in_progress += ['Python', 'Java']
    lecturer.courses_attached += ['Python', 'C++']
    reviewer.courses_attached += ['Python', 'C++']

    print(student.rate_lecture(lecturer, 'Python', 7))   # None
    print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
    print(student.rate_lecture(lecturer, 'C++', 8))      # Ошибка
    print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка

    print(lecturer.grades)  # {'Python': [7]}

    # Проверяем, что Reviewer тоже может оценивать студентов
    reviewer.rate_hw(student, 'Python', 9)
    reviewer.rate_hw(student, 'Python', 8)
    print(student.grades)   # {'Python': [9, 8]}

    # --- Задание №3: __str__ и сравнение ---
    print('\n--- Вывод через __str__ ---')
    print(reviewer)
    print()
    print(lecturer)
    print()
    print(student)

    # Сравнение лекторов
    lecturer2 = Lecturer('Анна', 'Смирнова')
    lecturer2.courses_attached += ['Python']
    lecturer2.grades = {'Python': [10, 10, 10]}

    print('\n--- Сравнение лекторов ---')
    print(f'Лектор 1 средняя: {lecturer._average_grade()}')
    print(f'Лектор 2 средняя: {lecturer2._average_grade()}')
    print(f'lecturer < lecturer2: {lecturer < lecturer2}')   # True
    print(f'lecturer == lecturer2: {lecturer == lecturer2}') # False

    # Сравнение студентов
    student2 = Student('Иван', 'Петров', 'М')
    student2.courses_in_progress += ['Python']
    student2.grades = {'Python': [10, 10]}

    print('\n--- Сравнение студентов ---')
    print(f'Студент 1 средняя: {student._average_grade()}')
    print(f'Студент 2 средняя: {student2._average_grade()}')
    print(f'student < student2: {student < student2}')   # True
    print(f'student == student2: {student == student2}') # False



#4 задание

class Student:
    """Класс студента."""

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}  # {название_курса: [оценки за ДЗ]}

    def rate_lecture(self, lecturer, course, grade):
        """Студент выставляет оценку лектору за лекцию."""
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: оценивать можно только лекторов!'
        if course not in self.courses_in_progress:
            return 'Ошибка: студент не изучает этот курс!'
        if course not in lecturer.courses_attached:
            return 'Ошибка: лектор не ведёт этот курс!'

        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]

    def _average_grade(self):
        """Средняя оценка за ДЗ по всем курсам."""
        all_grades = [g for grades_list in self.grades.values() for g in grades_list]
        if not all_grades:
            return 0
        return round(sum(all_grades) / len(all_grades), 2)

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self._average_grade()}\n"
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
            f"Завершенные курсы: {', '.join(self.finished_courses)}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Mentor:
    """Родительский класс для всех наставников."""

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Reviewer(Mentor):
    """Эксперт, проверяющий домашние задания."""

    def rate_hw(self, student, course, grade):
        """Reviewer выставляет оценку студенту за домашнее задание."""
        if isinstance(student, Student) and \
                course in self.courses_attached and \
                course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка: студент или курс не соответствуют условиям!'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    """Лектор, ведущий курсы."""

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # {название_курса: [оценки за лекции]}

    def _average_grade(self):
        """Средняя оценка за лекции по всем курсам."""
        all_grades = [g for grades_list in self.grades.values() for g in grades_list]
        if not all_grades:
            return 0
        return round(sum(all_grades) / len(all_grades), 2)

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {self._average_grade()}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() == other._average_grade()


# ===================== НОВЫЕ ФУНКЦИИ =====================

def get_average_hw_grade(students_list, course_name):
    """
    Подсчитывает среднюю оценку за домашние задания
    по всем студентам в рамках конкретного курса.

    :param students_list: список экземпляров класса Student
    :param course_name: название курса (строка)
    :return: средняя оценка (float) или 0, если оценок нет
    """
    all_grades = []
    for student in students_list:
        if course_name in student.grades:
            all_grades.extend(student.grades[course_name])

    if not all_grades:
        return 0
    return round(sum(all_grades) / len(all_grades), 2)


def get_average_lecture_grade(lecturers_list, course_name):
    """
    Подсчитывает среднюю оценку за лекции всех лекторов
    в рамках конкретного курса.

    :param lecturers_list: список экземпляров класса Lecturer
    :param course_name: название курса (строка)
    :return: средняя оценка (float) или 0, если оценок нет
    """
    all_grades = []
    for lecturer in lecturers_list:
        if course_name in lecturer.grades:
            all_grades.extend(lecturer.grades[course_name])

    if not all_grades:
        return 0
    return round(sum(all_grades) / len(all_grades), 2)


# ===================== ПОЛЕВЫЕ ИСПЫТАНИЯ =====================

if __name__ == '__main__':
    # --- Создаём по 2 экземпляра каждого класса ---
    # Студенты
    student1 = Student('Ольга', 'Алёхина', 'Ж')
    student2 = Student('Иван', 'Петров', 'М')

    # Лекторы
    lecturer1 = Lecturer('Иван', 'Иванов')
    lecturer2 = Lecturer('Анна', 'Смирнова')

    # Эксперты
    reviewer1 = Reviewer('Пётр', 'Петров')
    reviewer2 = Reviewer('Мария', 'Сидорова')

    # --- Настраиваем курсы ---
    student1.courses_in_progress += ['Python', 'Git']
    student1.finished_courses += ['Введение в программирование']

    student2.courses_in_progress += ['Python', 'Java']
    student2.finished_courses += ['Основы HTML']

    lecturer1.courses_attached += ['Python', 'Git']
    lecturer2.courses_attached += ['Python', 'Java']

    reviewer1.courses_attached += ['Python', 'Git']
    reviewer2.courses_attached += ['Python', 'Java']

    # --- Выставляем оценки ---
    # Reviewer'ы оценивают студентов за ДЗ
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student1, 'Python', 8)
    reviewer1.rate_hw(student1, 'Git', 10)

    reviewer2.rate_hw(student2, 'Python', 7)
    reviewer2.rate_hw(student2, 'Java', 9)
    reviewer2.rate_hw(student2, 'Java', 10)

    # Студенты оценивают лекторов
    student1.rate_lecture(lecturer1, 'Python', 10)
    student1.rate_lecture(lecturer1, 'Python', 9)
    student1.rate_lecture(lecturer1, 'Git', 8)

    student2.rate_lecture(lecturer2, 'Python', 7)
    student2.rate_lecture(lecturer2, 'Java', 10)

    # --- Проверка проверки ошибок ---
    print("=== Проверка обработки ошибок ===")
    print(student1.rate_lecture(lecturer1, 'Java', 8))  # Ошибка: студент не изучает Java
    print(student1.rate_lecture(reviewer1, 'Python', 6))  # Ошибка: оценивать можно только лекторов
    print(reviewer1.rate_hw(student2, 'Python', 5))  # Ошибка: студент не изучает Python у reviewer1

    # --- Вывод через __str__ ---
    print("\n=== Вывод объектов через __str__ ===")
    print(reviewer1)
    print("-" * 30)
    print(lecturer1)
    print("-" * 30)
    print(student1)

    # --- Сравнение объектов ---
    print("\n=== Сравнение объектов ===")
    print(f"student1 < student2: {student1 < student2}")
    print(f"student1 == student2: {student1 == student2}")
    print(f"lecturer1 < lecturer2: {lecturer1 < lecturer2}")
    print(f"lecturer1 == lecturer2: {lecturer1 == lecturer2}")

    # --- Работа новых функций ---
    print("\n=== Работа функций подсчёта средних оценок ===")

    students_list = [student1, student2]
    lecturers_list = [lecturer1, lecturer2]

    avg_hw_python = get_average_hw_grade(students_list, 'Python')
    print(f"Средняя оценка за ДЗ по курсу 'Python': {avg_hw_python}")

    avg_hw_git = get_average_hw_grade(students_list, 'Git')
    print(f"Средняя оценка за ДЗ по курсу 'Git': {avg_hw_git}")

    avg_hw_java = get_average_hw_grade(students_list, 'Java')
    print(f"Средняя оценка за ДЗ по курсу 'Java': {avg_hw_java}")

    avg_lecture_python = get_average_lecture_grade(lecturers_list, 'Python')
    print(f"Средняя оценка за лекции по курсу 'Python': {avg_lecture_python}")

    avg_lecture_git = get_average_lecture_grade(lecturers_list, 'Git')
    print(f"Средняя оценка за лекции по курсу 'Git': {avg_lecture_git}")

    avg_lecture_java = get_average_lecture_grade(lecturers_list, 'Java')
    print(f"Средняя оценка за лекции по курсу 'Java': {avg_lecture_java}")