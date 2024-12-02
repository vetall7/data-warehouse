import random

from config import *
from tables import Students, Teachers, Groups

class Updater:
    def __init__(self, config):
        self._config = config

    def update(self, data):
        groups_to_update = random.sample(data['groups'], self._config['groups_number'])
        teachers_to_update = random.sample(data['teachers'], self._config['teachers_number'])
        
        updated_groups = self._update_groups(groups_to_update)
        updated_teachers = self._update_teachers(teachers_to_update)
        
        data['groups'] = [group for group in data['groups'] if group not in groups_to_update] + updated_groups
        data['teachers'] = [teacher for teacher in data['teachers'] if teacher not in teachers_to_update] + updated_teachers
        return data
    

    def _update_students(self, students):
        updated_students = [Students.from_student(student) for student in students]
        for student in updated_students:
            student.address = faker.address().replace('\n', ' ')
        return updated_students
    
    def _update_groups(self, groups):
        # updated_groups = [Groups.from_group(group) for group in groups if group.grade < GROUP_GRADE_RANGE.max]
        updated_groups = [group for group in groups if group.grade < GROUP_GRADE_RANGE.max]
        for group in updated_groups:
            group.grade += 1
        return updated_groups

    def _update_teachers(self, teachers):
        # updated_teachers = [Teachers.from_teacher(teacher) for teacher in teachers]
        updated_teachers = teachers
        for teacher in updated_teachers:
            teacher.phone = faker.unique.numerify(PHONE_NUMBER)
        return updated_teachers
