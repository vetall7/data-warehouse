import datetime

from utils import Range

GRADE_TITLES = ["wejściówka", "kartkówka", "test", "aktywność", "quiz", "kolokwium", "egzamin", "zadanie domowe"]
SPECIALIZATIONS = ["informatyka", "matematyka", "fizyka", "chemia", "nauki społeczne", "prawo"]
PHONE_NUMBER = "+48#########"
ASSESSMENTS_QUESTIONS = [
    "Czy zajęcia były prowadzone w sposób zrozumiały?",
    "Czy zajęcia były prowadzone w sposób interesujący?"
]

STUDENTS_NUMBER = 100
GROUPS_NUMBER = 10
GRADES_NUMBER = 100
SUBJECTS_NUMBER = 10
TEACHERS_NUMBER = 10
SURVEYS_NUMBER = 100
MAX_CONSULTATIONS_PER_TEACHER = 20

STUDIES_NUMBER = 100
TEACHINGS_NUMBER = 100

SURVEYS_DATE_RANGE = Range(datetime.datetime(2020, 1, 1), datetime.datetime.now())
ASSESSMENTS_GRADE_RANGE = Range(1, 5)
GROUP_GRADE_RANGE = Range(8, 12)
GRADES_RANGE = Range(1, 10)
STUDIES_YEAR_RANGE = Range(2020, 2024)
SUBJECTS_YEAR_RANGE = Range(2020, 2024)
CONSULTATIONS_PER_TEACHER_RANGE = Range(0, 25)
CONSULTATIONS_DURATION_RANGE = Range(30, 180)
CONSULTATIONS_DATETIME_RANGE = Range(datetime.datetime(2020, 1, 1, 0, 0, 0), datetime.datetime.now())

FAKER_LOCALIZATION = 'pl_PL'