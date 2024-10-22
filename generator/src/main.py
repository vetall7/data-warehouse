from faker import Faker
import random
from tables import *

faker = Faker(FAKER_LOCALIZATION)

def generate_data():
    specializations = [Specializations(name) for name in SPECIALIZATIONS]
    students = [Students() for _ in range(STUDENTS_NUMBER)]
    teachers = [Teachers() for _ in range(TEACHERS_NUMBER)]
    groups = [Groups(random.choice(specializations).id) for _ in range(GROUPS_NUMBER)]
    subjects = [Subjects() for _ in range(SUBJECTS_NUMBER)]
    
    studies = [Studies(random.choice(students).pesel, random.choice(groups).id) for _ in range(STUDIES_NUMBER)]
    grades = [Grades(random.choice(students).pesel, random.choice(subjects).id, random.choice(GRADE_TITLES)) for _ in range(GRADES_NUMBER)]
    surveys = [Surveys(random.choice(students).pesel, random.choice(subjects).id, random.choice(teachers).pesel) for _ in range(SURVEYS_NUMBER)]
    assessments = [Assessments(survey.id, question) for question in ASSESSMENTS_QUESTIONS for survey in surveys]
    teachings = [Teachings(random.choice(subjects).id, random.choice(teachers).pesel, random.choice(groups).id) for _ in range(TEACHINGS_NUMBER)]
    consultations = [
        Consultations(teacher.pesel)\
            for _ in range(CONSULTATIONS_PER_TEACHER_RANGE.min, CONSULTATIONS_PER_TEACHER_RANGE.max)\
                for teacher in teachers
    ]
    
    print("\nSpecializations:")
    for spec in specializations:
        print(vars(spec))

    print("\nStudents:")
    for student in students:
        print(vars(student))
    
    print("\nStudies:")
    for study in studies:
        print(vars(study))

    print("\nSurveys:")
    for survey in surveys:
        print(vars(survey))

    print("\nGrades:")
    for grade in grades:
        print(vars(grade))
    
    print("\nAssessments:")
    for assessment in assessments:
        print(vars(assessment))

    print("\nTeachings:")
    for teaching in teachings:
        print(vars(teaching))
    
    print("\nConsultations:")
    for cons in consultations:
        print(vars(cons))



if __name__ == "__main__":
    generate_data()
