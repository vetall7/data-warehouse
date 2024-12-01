USE SchoolDW;

CREATE TABLE Dates (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date DATE NOT NULL,
    year SMALLINT NOT NULL,
    monthNo TINYINT NOT NULL CHECK (monthNo BETWEEN 1 AND 12),
    dayOfMonthNo TINYINT NOT NULL CHECK (dayOfMonthNo BETWEEN 1 AND 31),
    semester VARCHAR(24) NOT NULL CHECK (semester IN ('zimowy', 'letni'))
);


CREATE TABLE Subjects (
    id INT PRIMARY KEY IDENTITY(1,1),
    year SMALLINT NOT NULL,
    name VARCHAR(96) NOT NULL
);

CREATE TABLE Teachers (
    id INT PRIMARY KEY IDENTITY(1,1),
    pesel CHAR(11) NOT NULL,
    name VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL,
    phone VARCHAR(24) NOT NULL,
    consultations_freq_category NVARCHAR(32) CHECK (consultations_freq_category IN ('brak', 'rzadko', 'przeciętnie', 'często')),
    consultations_duration_category NVARCHAR(32) CHECK (consultations_duration_category IN ('brak', 'krótkie', 'długie', 'średnie')),
    surveys_grade_category NVARCHAR(32) CHECK (surveys_grade_category IN ('brak', 'niskie', 'średnie', 'wysokie')),
    creation_date DATE NOT NULL,
    expiration_date DATE
);


CREATE TABLE Groups (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(32) NOT NULL,
    grade TINYINT CHECK (grade BETWEEN 8 AND 12),
    creation_date DATE NOT NULL,
    expiration_date DATE
);


CREATE TABLE ConductingLesson (
    date_id INT NOT NULL,
    subject_id INT NOT NULL,
    teacher_id INT NOT NULL,
    group_id INT NOT NULL,
    attendance_rate REAL CHECK (attendance_rate BETWEEN 0 AND 100),
    average_grade REAL CHECK (average_grade BETWEEN 0 AND 10),
    grades_number TINYINT NOT NULL CHECK (grades_number >= 0),
    PRIMARY KEY (date_id, subject_id, teacher_id, group_id),
    FOREIGN KEY (date_id) REFERENCES Dates(id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id),
    FOREIGN KEY (teacher_id) REFERENCES Teachers(id),
    FOREIGN KEY (group_id) REFERENCES Groups(id)
);
 