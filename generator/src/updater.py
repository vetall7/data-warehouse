import random

import faker

from config import *

from config import faker

class Updater:
    def __init__(self, config):
        self._config = config

    def update(self, data):
        assessments_to_update = random.sample(data['assessments'], self._config['assessments_number'])
        consultations_to_update = random.sample(data['consultations'], self._config['consultations_number'])
        students_to_update = random.sample(data['students'], self._config['students_number'])
        groups_to_update = random.sample(data['groups'], self._config['groups_number'])
        grades_to_update = random.sample(data['grades'], self._config['grades_number'])
        teachers_to_update = random.sample(data['teachers'], self._config['teachers_number'])
        surveys_to_update = random.sample(data['surveys'], self._config['surveys_number'])
        studies_to_update = random.sample(data['studies'], self._config['studies_number'])
        teachings_to_update = random.sample(data['teachings'], self._config['teachings_number'])

        return {
            'assessments': self._update_assessments(assessments_to_update),
            'consultations': self._update_consultations(consultations_to_update),
            'students': self._update_students(students_to_update),
            'groups': self._update_groups(groups_to_update),
            'grades': self._update_grades(grades_to_update),
            'teachers': self._update_teachers(teachers_to_update),
            'surveys': self._update_surveys(surveys_to_update),
            'studies': self._update_studies(studies_to_update),
            'teachings': self._update_teachings(teachings_to_update, data)
        }
    
    def _update_assessments(self, assessments):
        for assessment in assessments:
            assessment.grade = ASSESSMENTS_GRADE_RANGE.random()
        return assessments

    def _update_consultations(self, consultations):
        for consultation in consultations:
            time = CONSULTATIONS_DURATION_RANGE.random()
            hours = time // 60
            minutes = time % 60
            consultation.duration = datetime.time(hour=hours, minute=minutes)
        return consultations

    def _update_students(self, students):
        for student in students:
            student.phone = faker.unique.numerify(PHONE_NUMBER)
        return students
    
    def _update_groups(self, groups):
        for group in groups:
            group.grade = GROUP_GRADE_RANGE.random()
        return groups
        
    def _update_grades(self, grades):
        for grade in grades:
            grade.grade = GRADES_RANGE.random()
        return grades
    
    def _update_teachers(self, teachers):
        for teacher in teachers:
            teacher.phone = faker.unique.numerify(PHONE_NUMBER)
        return

    def _update_surveys(self, surveys):
        for survey in surveys:
            survey.date = faker.date_between(self._config['date_range'].min, self._config['date_range'].max)
        return surveys
    
    def _update_studies(self, studies):
        for study in studies:
            study.year = random.randint(self._config['date_range'].min.year, self._config['date_range'].max.year)
        return studies

    def _update_teachings(self, teachings, data):
        for teaching in teachings:
            teaching.teacher_id = random.choice(data['teachers']).pesel
        return teachings
