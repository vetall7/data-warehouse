import random
import concurrent.futures
from tables import *
from config import *
from utils import Attendance

class Generator:
    def __init__(self, config):
        self._config = config

    def generate(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Independent tasks
            specializations_future = executor.submit(self._generate_specializations)
            students_future = executor.submit(self._generate_students)
            teachers_future = executor.submit(self._generate_teachers)
            subjects_future = executor.submit(self._generate_subjects)
            
            specializations = specializations_future.result()
            students = students_future.result()
            teachers = teachers_future.result()
            subjects = subjects_future.result()
            
            # Dependent tasks
            groups_future = executor.submit(self._generate_groups, specializations)
            studies_future = executor.submit(self._generate_studies, students, groups_future.result())
            grades_future = executor.submit(self._generate_grades, students, subjects)
            consultations_future = executor.submit(self._generate_consultations, teachers)
            surveys_future = executor.submit(self._generate_surveys, students, subjects, teachers)
            teachings_future = executor.submit(self._generate_teachings, subjects, teachers, groups_future.result())
            assessments_future = executor.submit(self._generate_assessments, surveys_future.result())
            
            groups = groups_future.result()
            studies = studies_future.result()
            grades = grades_future.result()
            consultations = consultations_future.result()
            surveys = surveys_future.result()
            teachings = teachings_future.result()
            assessments = assessments_future.result()

        return {
            'specializations': specializations,
            'students': students,
            'teachers': teachers,
            'groups': groups,
            'subjects': subjects,
            'studies': studies,
            'grades': grades,
            'surveys': surveys,
            'assessments': assessments,
            'teachings': teachings,
            'consultations': consultations
        }

    def _generate_entities(self, entity_class, count, *args):
        return [
            entity_class(*args[0]()) if args and isinstance(args[0](), tuple) 
            else entity_class(args[0]()) if args 
            else entity_class() 
            for _ in range(count)
        ]

    def _generate_specializations(self):
        return [Specializations(name) for name in SPECIALIZATIONS]

    def _generate_students(self):
        return self._generate_entities(Students, self._config['students_number'])

    def _generate_teachers(self):
        return self._generate_entities(Teachers, self._config['teachers_number'])

    def _generate_groups(self, specializations):
        return self._generate_entities(Groups, self._config['groups_number'], lambda: random.choice(specializations).id)

    def _generate_subjects(self):
        return [Subjects(name, year) for name in SUBJECTS for year in range(self._config['date_range'].min.year, self._config['date_range'].max.year + 1)]

    def _generate_studies(self, students, groups):
        return self._generate_entities(Studies, self._config['studies_number'], lambda: (random.choice(students).pesel, random.choice(groups).id, self._config))

    def _generate_grades(self, students, subjects):
        return self._generate_entities(Grades, self._config['grades_number'], lambda: (random.choice(students).pesel, random.choice(subjects).id, random.choice(GRADE_TITLES)))

    def _generate_surveys(self, students, subjects, teachers):
        return self._generate_entities(Surveys, self._config['surveys_number'], lambda: (random.choice(students).pesel, random.choice(subjects).id, random.choice(teachers).pesel, self._config))

    def _generate_teachings(self, subjects, teachers, groups):
        return self._generate_entities(Teachings, self._config['teachings_number'], lambda: (random.choice(subjects).id, random.choice(teachers).pesel, random.choice(groups).id))

    def _generate_assessments(self, surveys):
        return [Assessments(survey.id, question) for question in ASSESSMENTS_QUESTIONS for survey in surveys]

    def _generate_consultations(self, teachers):
        consultations = []
        for teacher in teachers:
            consultations.extend(self._generate_entities(Consultations, CONSULTATIONS_PER_TEACHER_RANGE.random(), lambda: (teacher.pesel, self._config)))
        return consultations


    def generate_attendance(self, data):
        attendance_files = self._config['attendance_files']
        groups_number, subjects_number = attendance_files['groups_number'], attendance_files['subjects_number']
        random_groups = random.sample(data['groups'], groups_number)

        attendance = dict()

        for group in random_groups:
            random_subjects = random.sample(data['subjects'], subjects_number)
            for subject in random_subjects:
                group_students = self._get_group_students(data, group, subject.year)
                attendance[(group.id, subject.id)] = self._generate_attendance(subject, group_students)

        return attendance


    def _generate_attendance(self, subject, students):
        attendances = dict()
        date = datetime.date(year=subject.year, month=10, day=1) # start of the academic year
        for _ in range(self._config['attendance_files']['dates_number']):
            attendance_list = []
            for student in students:
                present = random.choice([True, False])
                excused = random.choice([True, False]) if not present else False
                attendance_list.append(Attendance(student.pesel, present, excused))

            attendances[date] = attendance_list
            date += datetime.timedelta(weeks=1)

        return attendances
        
    def _get_group_students(self, data, group, year):
        student_ids = [study.student_id for study in data['studies'] if study.group_id == group.id and study.year == year]
        return [student for student in data['students'] if student.pesel in student_ids]
