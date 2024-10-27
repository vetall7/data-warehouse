from faker import Faker
import random
import datetime
from config import *
import itertools
from random_pesel import RandomPESEL

pesel = RandomPESEL()
faker = Faker(FAKER_LOCALIZATION)

id_iters = {
    'student': itertools.count(1),
    'study': itertools.count(1),
    'teacher': itertools.count(1),
    'subject': itertools.count(1),
    'group': itertools.count(1),
    'specialization': itertools.count(1),
    'grade': itertools.count(1),
    'assessment': itertools.count(1),
    'teaching': itertools.count(1),
    'survey': itertools.count(1),
    'consultation': itertools.count(1)
}

class Students:
    def __init__(self):
        self.pesel = pesel.generate(min_age=13, max_age=20)
        self.name = faker.name()
        self.phone = faker.unique.numerify(PHONE_NUMBER)
        self.address = faker.address()

class Studies:
    def __init__(self, student_pesel, group_id, config):
        self.id = next(id_iters['study'])
        self.student_id = student_pesel
        self.group_id = group_id
        self.year = random.randint(config['date_range'].min.year, config['date_range'].max.year)

class Teachers:
    def __init__(self):
        self.pesel = pesel.generate(min_age=20, max_age=70)
        self.name = faker.name()
        self.email = faker.email()
        self.phone = faker.unique.numerify(PHONE_NUMBER)

class Subjects:
    def __init__(self, name, year):
        self.id = next(id_iters['subject'])
        self.year = year
        self.name = name

class Groups:
    def __init__(self, specialization_id):
        self.id = next(id_iters['group'])
        self.name = faker.unique.bothify('##-?', letters="ABC")
        self.grade = GROUP_GRADE_RANGE.random()
        self.specialization_id = specialization_id

class Specializations:
    def __init__(self, name):
        self.id = next(id_iters['specialization'])
        self.name = name

class Grades:
    def __init__(self, student_id, subject_id, title):
        self.id = next(id_iters['grade'])
        self.title = title
        self.grade = GRADES_RANGE.random()
        self.student_id = student_id
        self.subject_id = subject_id

class Assessments:
    def __init__(self, survey_id, question):
        self.id = next(id_iters['assessment'])
        self.grade = ASSESSMENTS_GRADE_RANGE.random()
        self.question = question
        self.survey_id = survey_id

class Teachings:
    def __init__(self, subject_id, teacher_id, group_id):
        self.id = next(id_iters['teaching'])
        self.subject_id = subject_id
        self.teacher_id = teacher_id
        self.group_id = group_id

class Surveys:
    def __init__(self, student_id, subject_id, teacher_id, config):
        self.id = next(id_iters['survey'])
        self.date = faker.date_between(config['date_range'].min, config['date_range'].max)
        self.student_id = student_id
        self.subject_id = subject_id
        self.teacher_id = teacher_id

class Consultations:
    def __init__(self, teacher_id, config):
        self.id = next(id_iters['consultation'])
        self.teacher_id = teacher_id
        self.date = faker.date_time_between(config['date_range'].min, config['date_range'].max)
        self.duration = datetime.time(minutes=CONSULTATIONS_DURATION_RANGE.random())
