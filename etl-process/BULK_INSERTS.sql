use School; 

BULK INSERT Teachers
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\teachers.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Students
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\students.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Consultations
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\consultations.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Specializations
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\specializations.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Groups
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\groups.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Studies
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\studies.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Subjects
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\subjects.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Teachings
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\teachings.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Grades
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\grades.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Surveys
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\surveys.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT Assessments
FROM 'D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\assessments.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);
