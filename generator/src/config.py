import yaml
import datetime
from utils import Range

with open('../config.yml', 'r') as file:
    config = yaml.safe_load(file)

GRADE_TITLES = config['grade_titles']
SPECIALIZATIONS = config['specializations']
PHONE_NUMBER = config['phone_number']
SUBJECTS = config['subjects']
ASSESSMENTS_QUESTIONS = config['assessments_questions']

STUDENTS_NUMBER = config['students_number']
GROUPS_NUMBER = config['groups_number']
GRADES_NUMBER = config['grades_number']
SUBJECTS_NUMBER = config['subjects_number']
TEACHERS_NUMBER = config['teachers_number']
SURVEYS_NUMBER = config['surveys_number']
MAX_CONSULTATIONS_PER_TEACHER = config['max_consultations_per_teacher']

STUDIES_NUMBER = config['studies_number']
TEACHINGS_NUMBER = config['teachings_number']

SURVEYS_DATE_RANGE = Range(
    datetime.datetime.fromisoformat(config['surveys_date_range']['min']),
    datetime.datetime.fromisoformat(config['surveys_date_range']['max'])
)
ASSESSMENTS_GRADE_RANGE = Range(config['assessments_grade_range']['min'], config['assessments_grade_range']['max'])
GROUP_GRADE_RANGE = Range(config['group_grade_range']['min'], config['group_grade_range']['max'])
GRADES_RANGE = Range(config['grades_range']['min'], config['grades_range']['max'])
STUDIES_YEAR_RANGE = Range(config['studies_year_range']['min'], config['studies_year_range']['max'])
SUBJECTS_YEAR_RANGE = Range(config['subjects_year_range']['min'], config['subjects_year_range']['max'])
CONSULTATIONS_PER_TEACHER_RANGE = Range(config['consultations_per_teacher_range']['min'], config['consultations_per_teacher_range']['max'])
CONSULTATIONS_DURATION_RANGE = Range(config['consultations_duration_range']['min'], config['consultations_duration_range']['max'])
CONSULTATIONS_DATETIME_RANGE = Range(
    datetime.datetime.fromisoformat(config['consultations_datetime_range']['min']),
    datetime.datetime.fromisoformat(config['consultations_datetime_range']['max'])
)

FAKER_LOCALIZATION = config['faker_localization']
