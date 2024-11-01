from faker import Faker
import yaml
import datetime
from utils import Range

with open('../config.yml', 'r') as file:
    config = yaml.safe_load(file)

MAX_CONSULTATIONS_PER_TEACHER = config['max_consultations_per_teacher']
ASSESSMENTS_GRADE_RANGE = Range(config['assessments_grade_range']['min'], config['assessments_grade_range']['max'])
GROUP_GRADE_RANGE = Range(config['group_grade_range']['min'], config['group_grade_range']['max'])
GRADES_RANGE = Range(config['grades_range']['min'], config['grades_range']['max'])
CONSULTATIONS_PER_TEACHER_RANGE = Range(config['consultations_per_teacher_range']['min'], config['consultations_per_teacher_range']['max'])
CONSULTATIONS_DURATION_RANGE = Range(config['consultations_duration_range']['min'], config['consultations_duration_range']['max'])
PHONE_NUMBER = config['phone_number']
GRADE_TITLES = config['grade_titles']
SUBJECTS = config['subjects']
ASSESSMENTS_QUESTIONS = config['assessments_questions']

GENERATE_CONFIGS = config['time_generate']
UPDATE_CONFIGS = config['time_update']

faker = Faker(config['faker_localization'])

def get_generate_config(set_number):
        config_set = GENERATE_CONFIGS[set_number].copy()
        config_set['date_range'] = Range(
            datetime.datetime.fromisoformat(config_set['date_range']['min']),
            datetime.datetime.fromisoformat(config_set['date_range']['max'])
        )
        return config_set

def get_update_config(set_number):
    try:
        config_set = UPDATE_CONFIGS[set_number].copy()
        config_set['date_range'] = Range(
            datetime.datetime.fromisoformat(GENERATE_CONFIGS[set_number]['date_range']['min']),
            datetime.datetime.fromisoformat(GENERATE_CONFIGS[set_number]['date_range']['max'])
        )
        return config_set
    except KeyError:
        return None
