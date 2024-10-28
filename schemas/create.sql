CREATE TABLE Students (
    pesel CHAR(11) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    phone VARCHAR(24),
    address VARCHAR(512)
);

CREATE TABLE Subjects (
    id INT PRIMARY KEY,
    year SMALLINT NOT NULL,
    name VARCHAR(256) NOT NULL
);

CREATE TABLE Grades (
    id INT PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    grade TINYINT NOT NULL,
    student_id CHAR(11) NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(pesel),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id)
);

CREATE TABLE Specializations (
    id INT PRIMARY KEY,
    name VARCHAR(256) NOT NULL
);

CREATE TABLE Groups (
    id INT PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    grade TINYINT NOT NULL,
    specialization_id INT NOT NULL,
    FOREIGN KEY (specialization_id) REFERENCES Specializations(id)
);

CREATE TABLE Studies (
    id INT PRIMARY KEY,
    student_id CHAR(11) NOT NULL,
    group_id INT NOT NULL,
    year SMALLINT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(pesel),
    FOREIGN KEY (group_id) REFERENCES Groups(id)
);

CREATE TABLE Teachers (
    pesel CHAR(11) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    email VARCHAR(128),
    phone VARCHAR(24)
);

CREATE TABLE Teachings (
    id INT PRIMARY KEY,
    subject_id INT NOT NULL,
    teacher_id CHAR(11) NOT NULL,
    group_id INT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES Subjects(id),
    FOREIGN KEY (teacher_id) REFERENCES Teachers(pesel),
    FOREIGN KEY (group_id) REFERENCES Groups(id)
);

CREATE TABLE Consultations (
    id INT PRIMARY KEY,
    teacher_id CHAR(11) NOT NULL,
    date DATETIME NOT NULL,
    duration TIME,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(pesel)
);

CREATE TABLE Surveys (
    id INT PRIMARY KEY,
    date DATE NOT NULL,
    student_id CHAR(11) NOT NULL,
    subject_id INT NOT NULL,
    teacher_id CHAR(11) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(pesel),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id),
    FOREIGN KEY (teacher_id) REFERENCES Teachers(pesel)
);

CREATE TABLE Assessments (
    id INT PRIMARY KEY,
    grade TINYINT NOT NULL,
    question VARCHAR(1024) NOT NULL,
    survey_id INT NOT NULL,
    FOREIGN KEY (survey_id) REFERENCES Surveys(id)
);
