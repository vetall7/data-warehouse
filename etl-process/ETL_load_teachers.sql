DROP View IF EXISTS TeacherCategories;

GO

CREATE VIEW TeacherCategories AS
  WITH TeacherBase AS (
        SELECT DISTINCT id
        FROM School.dbo.Teachers
    ),
    ConsultationsStats AS (
        SELECT
            teacher_id,
            COUNT(*) * 1.0 / NULLIF(DATEDIFF(WEEK, MIN(date), GETDATE()), 0) AS avg_per_week,
            AVG(DATEDIFF(MINUTE, '00:00:00', duration)) AS avg_duration_minutes 
        FROM School.dbo.Consultations
        GROUP BY teacher_id
    ),
    TeacherGrades AS (
        SELECT
            teacher_id,
            AVG(survey_avg_grade) AS avg_grade
        FROM (
            SELECT
                S.teacher_id,
                AVG(A.grade * 1.0) AS survey_avg_grade
            FROM School.dbo.Surveys AS S
            INNER JOIN School.dbo.Assessments AS A
                ON S.id = A.survey_id
            GROUP BY S.teacher_id, S.id
        ) AS SurveyGrades
        GROUP BY teacher_id
    )
    SELECT
        TB.id,
        CASE 
            WHEN CS.avg_per_week IS NULL THEN 'brak'
            WHEN CS.avg_per_week <= 0.8 THEN 'rzadko'
            WHEN CS.avg_per_week > 0.8 AND CS.avg_per_week <= 1.2 THEN 'przeciętnie'
            ELSE 'często'
        END AS consultations_freq_category,
        CASE 
            WHEN CS.avg_duration_minutes IS NULL THEN 'brak'
            WHEN CS.avg_duration_minutes <= 60 THEN 'krótkie'
            WHEN CS.avg_duration_minutes > 60 AND CS.avg_duration_minutes <= 120 THEN 'średnie'
            ELSE 'długie'
        END AS consultations_duration_category,
        CASE 
            WHEN TG.avg_grade IS NULL THEN 'brak'
            WHEN TG.avg_grade < 3 THEN 'niskie'
            WHEN TG.avg_grade >= 3 AND TG.avg_grade <= 4 THEN 'średnie'
            ELSE 'wysokie'
        END AS surveys_grade_category
    FROM TeacherBase AS TB
    LEFT JOIN ConsultationsStats AS CS
        ON TB.id = CS.teacher_id
    LEFT JOIN TeacherGrades AS TG
        ON TB.id = TG.teacher_id;
GO

DECLARE @EntryDate DATETIME;
SELECT @EntryDate = GETDATE();

MERGE INTO Teachers AS TT
    USING (
        SELECT
            ST.pesel,
            ST.name,
            ST.email,
            ST.phone,
            TC.consultations_freq_category,
            TC.consultations_duration_category,
            TC.surveys_grade_category
        FROM School.dbo.Teachers AS ST
        LEFT JOIN TeacherCategories AS TC
            ON ST.id = TC.id
    ) AS Source
        ON TT.pesel = Source.pesel
            WHEN NOT MATCHED THEN
                INSERT (pesel, name, email, phone, consultations_freq_category, consultations_duration_category, surveys_grade_category, creation_date, expiration_date)
                VALUES (
                    Source.pesel,
                    Source.name,
                    Source.email,
                    Source.phone,
                    Source.consultations_freq_category,
                    Source.consultations_duration_category,
                    Source.surveys_grade_category,
                    @EntryDate,
                    NULL
                )
            WHEN MATCHED
                AND (Source.phone <> TT.phone OR Source.email <> TT.email)
            THEN
                UPDATE
                SET TT.expiration_date = @EntryDate;


INSERT INTO Teachers(
	pesel,
    name,
    email,
    phone,
    consultations_freq_category,
    consultations_duration_category,
    surveys_grade_category,
    creation_date, 
	expiration_date
	)
	SELECT
        ST.pesel,
        ST.name,
        ST.email,
        ST.phone,
        TC.consultations_freq_category,
        TC.consultations_duration_category,
        TC.surveys_grade_category,
        @EntryDate, 
		NULL 
    FROM School.dbo.Teachers AS ST
        LEFT JOIN TeacherCategories AS TC
            ON ST.id = TC.id
	EXCEPT
	SELECT 
		pesel,
        name,
        email,
        phone,
        consultations_freq_category,
        consultations_duration_category,
        surveys_grade_category,
        @EntryDate, 
		NULL 
	FROM Teachers;

DROP View TeacherCategories;
