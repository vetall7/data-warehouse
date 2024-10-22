from faker import Faker
import random
import datetime
from config import *
import itertools

faker = Faker(FAKER_LOCALIZATION)

student_id_iter = itertools.count(1)
study_id_iter = itertools.count(1)
teacher_id_iter = itertools.count(1)
subject_id_iter = itertools.count(1)
group_id_iter = itertools.count(1)
specialization_id_iter = itertools.count(1)
grade_id_iter = itertools.count(1)
assessment_id_iter = itertools.count(1)
teaching_id_iter = itertools.count(1)
survey_id_iter = itertools.count(1)
consultation_id_iter = itertools.count(1)

class Students:
    id_iter = itertools.count()
    
    def __init__(self):
        self.pesel = faker.unique.numerify('###########')
        self.name = faker.name()
        self.phone = faker.phone_number()
        self.address = faker.address()

class Studies:
    def __init__(self, student_pesel, group_id):
        self.id = next(study_id_iter)
        self.student_id = student_pesel
        self.group_id = group_id
        self.year = STUDIES_YEAR_RANGE.random()

class Teachers:
    def __init__(self):
        self.pesel = faker.unique.numerify('###########')
        self.name = faker.name()
        self.email = faker.email()
        self.phone = faker.phone_number()

class Subjects:
    def __init__(self):
        self.id = next(subject_id_iter)
        self.year = random.randint(2020, 2024)
        self.name = faker.word() # TODO: replace with smth more meaningful

class Groups:
    def __init__(self, specialization_id):
        self.id = next(group_id_iter)
        self.name = faker.word() # TODO: replace with smth more meaningful
        self.grade = GROUP_GRADE_RANGE.random()
        self.specialization_id = specialization_id

class Specializations:
    def __init__(self, name):
        self.id = next(specialization_id_iter)
        self.name = name

class Grades:
    def __init__(self, student_id, subject_id, title):
        self.id = next(grade_id_iter)
        self.title = title
        self.grade = GRADES_RANGE.random()
        self.student_id = student_id
        self.subject_id = subject_id

class Assessments:
    def __init__(self, survey_id, question):
        self.id = next(assessment_id_iter) 
        self.grade = ASSESSMENTS_GRADE_RANGE.random()
        self.question = question
        self.survey_id = survey_id

class Teachings:
    def __init__(self, subject_id, teacher_id, group_id):
        self.id = next(teaching_id_iter)
        self.subject_id = subject_id
        self.teacher_id = teacher_id
        self.group_id = group_id

class Surveys:
    def __init__(self, student_id, subject_id, teacher_id):
        self.id = next(survey_id_iter)
        self.date = faker.date_between(SURVEYS_DATE_RANGE.min, SURVEYS_DATE_RANGE.max)
        self.student_id = student_id 
        self.subject_id = subject_id
        self.teacher_id = teacher_id 

class Consultations:
    def __init__(self, teacher_id):
        self.id = next(consultation_id_iter)
        self.teacher_id = teacher_id
        self.date = faker.date_time_between(CONSULTATIONS_DATETIME_RANGE.min, CONSULTATIONS_DATETIME_RANGE.max)
        self.duration = datetime.timedelta(minutes=CONSULTATIONS_DURATION_RANGE.random())
