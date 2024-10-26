import yaml
import datetime
from utils import Range

with open('generator/config.yml', 'r') as file:
    config = yaml.safe_load(file)

MAX_CONSULTATIONS_PER_TEACHER = config['max_consultations_per_teacher']
ASSESSMENTS_GRADE_RANGE = Range(config['assessments_grade_range']['min'], config['assessments_grade_range']['max'])
GROUP_GRADE_RANGE = Range(config['group_grade_range']['min'], config['group_grade_range']['max'])
GRADES_RANGE = Range(config['grades_range']['min'], config['grades_range']['max'])
CONSULTATIONS_PER_TEACHER_RANGE = Range(config['consultations_per_teacher_range']['min'], config['consultations_per_teacher_range']['max'])
CONSULTATIONS_DURATION_RANGE = Range(config['consultations_duration_range']['min'], config['consultations_duration_range']['max'])
FAKER_LOCALIZATION = config['faker_localization']
PHONE_NUMBER = config['phone_number']
GRADE_TITLES = config['grade_titles']
SPECIALIZATIONS = config['specializations']
SUBJECTS = config['subjects']
ASSESSMENTS_QUESTIONS = config['assessments_questions']

CONFIG_SETS = config['time_moments']

def get_config_set(set_number):
    config_set = CONFIG_SETS[set_number]
    return {
        'students_number': config_set['students_number'],
        'groups_number': config_set['groups_number'],
        'grades_number': config_set['grades_number'],
        'teachers_number': config_set['teachers_number'],
        'surveys_number': config_set['surveys_number'],
        'studies_number': config_set['studies_number'],
        'teachings_number': config_set['teachings_number'],
        'date_range': Range(
            datetime.datetime.fromisoformat(config_set['date_range']['min']),
            datetime.datetime.fromisoformat(config_set['date_range']['max'])
        )
    }
