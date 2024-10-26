import random
import time
from utils import save_to_csv
from tables import *
from config import *


def generate_entities(entity_class, count, *args):
    return [
        entity_class(*args[0]()) if args and isinstance(args[0](), tuple) 
        else entity_class(args[0]()) if args 
        else entity_class() 
        for _ in range(count)
    ]


def generate_data(config):
    specializations = [Specializations(name) for name in SPECIALIZATIONS]

    students = generate_entities(Students, config['students_number'])
    teachers = generate_entities(Teachers, config['teachers_number'])
    groups = generate_entities(Groups, config['groups_number'], lambda: random.choice(specializations).id)
    subjects = [Subjects(name, year) for name in SUBJECTS for year in range(config['date_range'].min.year, config['date_range'].max.year + 1)]

    studies = generate_entities(Studies, config['studies_number'], lambda: (random.choice(students).pesel, random.choice(groups).id, config))
    grades = generate_entities(Grades, config['grades_number'], lambda: (random.choice(students).pesel, random.choice(subjects).id, random.choice(GRADE_TITLES)))
    surveys = generate_entities(Surveys, config['surveys_number'], lambda: (random.choice(students).pesel, random.choice(subjects).id, random.choice(teachers).pesel, config))
    teachings = generate_entities(Teachings, config['teachings_number'], lambda: (random.choice(subjects).id, random.choice(teachers).pesel, random.choice(groups).id))
    assessments = [Assessments(survey.id, question) for question in ASSESSMENTS_QUESTIONS for survey in surveys]
    consultations = [
        consultation 
        for teacher in teachers 
        for consultation in generate_entities(Consultations, CONSULTATIONS_PER_TEACHER_RANGE.random(), lambda: (teacher.pesel, config))
    ]

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


def save_data(path, data_dict):
    for file_name, data in data_dict.items():
        save_to_csv(data, path, file_name)


def generate(config_number):
    start_time = time.time()
    data = generate_data(get_config_set(config_number))
    save_data(f'time{config_number}', data)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time {config_number}: {execution_time:.2f} seconds")

def main():
    generate(config_number=1)
    generate(config_number=2)


if __name__ == "__main__":
    main()
