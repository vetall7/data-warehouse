import random
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


def generate_data():
    specializations = [Specializations(name) for name in SPECIALIZATIONS]
    students = generate_entities(Students, STUDENTS_NUMBER)
    teachers = generate_entities(Teachers, TEACHERS_NUMBER)
    groups = generate_entities(Groups, GROUPS_NUMBER, lambda: random.choice(specializations).id)
    subjects = generate_entities(Subjects, SUBJECTS_NUMBER)

    studies = generate_entities(Studies, STUDIES_NUMBER, lambda: (random.choice(students).pesel, random.choice(groups).id))
    grades = generate_entities(Grades, GRADES_NUMBER, lambda: (random.choice(students).pesel, random.choice(subjects).id, random.choice(GRADE_TITLES)))
    surveys = generate_entities(Surveys, SURVEYS_NUMBER, lambda: (random.choice(students).pesel, random.choice(subjects).id, random.choice(teachers).pesel))
    teachings = generate_entities(Teachings, TEACHINGS_NUMBER, lambda: (random.choice(subjects).id, random.choice(teachers).pesel, random.choice(groups).id))
    assessments = [Assessments(survey.id, question) for question in ASSESSMENTS_QUESTIONS for survey in surveys]
    consultations = [
        consultation 
        for teacher in teachers 
        for consultation in generate_entities(Consultations, CONSULTATIONS_PER_TEACHER_RANGE.random(), lambda: teacher.pesel)
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


def save_data(data_dict):
    for file_name, data in data_dict.items():
        save_to_csv(data, file_name)


def main():
    data = generate_data()
    save_data(data)


if __name__ == "__main__":
    main()
