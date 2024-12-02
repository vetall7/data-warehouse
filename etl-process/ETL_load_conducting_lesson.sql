-- Create a staging table to temporarily hold the raw data. 
-- Enable xp_cmdshell (if not done already)
DROP TABLE IF EXISTS #Files;

EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

-- Create a temporary table to hold file names
CREATE TABLE #Files (FileName NVARCHAR(255));

-- Insert file names into the table from the target directory
INSERT INTO #Files (FileName)
EXEC xp_cmdshell 'dir D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\attendance\ /b';

-- Declare variables for dynamic SQL execution
DECLARE @FileName NVARCHAR(255);
DECLARE @SQL NVARCHAR(MAX);

-- Cursor to iterate over file names
DECLARE FileCursor CURSOR FOR
SELECT FileName FROM #Files WHERE FileName LIKE '%.csv';

OPEN FileCursor;
FETCH NEXT FROM FileCursor INTO @FileName;

WHILE @@FETCH_STATUS = 0
BEGIN


    DROP TABLE IF EXISTS Attendance;
    DROP TABLE IF EXISTS StagingDates;
    DROP TABLE IF EXISTS StagingAttendanceRate;
    DROP TABLE IF EXISTS StagingCSVRaw;
    DROP TABLE IF EXISTS StagingCSV;
    DROP TABLE IF EXISTS StagingGrades;
    DROP TABLE IF EXISTS StagingAverageGrades;
    DROP TABLE IF EXISTS StagingAttendance;
    

	CREATE TABLE StagingCSV (
        LineNumber INT IDENTITY(1,1) PRIMARY KEY,
        RawLine NVARCHAR(MAX)
	);

	CREATE TABLE StagingCSVRaw (
			RawLine NVARCHAR(MAX)
    );

    CREATE TABLE StagingDates (
        id INT IDENTITY(1,1) PRIMARY KEY,
        date DATE NOT NULL
     );

    CREATE TABLE Attendance (
        AttendanceID INT IDENTITY(1,1) PRIMARY KEY,
        StudentName NVARCHAR(255),
        StudentPesel CHAR(11),
        SubjectName NVARCHAR(255),
        SubjectYear INT,
        AttendanceDate DATE,
        AttendanceStatus BIT
    );

    CREATE TABLE StagingAttendanceRate (
        date DATE NOT NULL,
        attendanceRate FLOAT NOT NULL,
    );

    CREATE TABLE StagingGrades (
        studentPesel CHAR(11),
        date DATE,
        grade INT,
    );

    CREATE TABLE StagingAverageGrades (
        date DATE,
        grades_number INT,
        average_grade FLOAT
    );


    SET @SQL = N'BULK INSERT StagingCSVRaw
                 FROM ''D:\Studying\sem_5\hd\data-warehouse\generator\data\time1\attendance\' + @FileName + '''
                 WITH (
                     FIELDTERMINATOR = '','', 
                     ROWTERMINATOR = ''\n'',
                     FIRSTROW = 1
                 );';

    -- Execute the dynamic SQL
    EXEC sp_executesql @SQL;


    INSERT INTO StagingCSV(RawLine)
    SELECT RawLine from StagingCSVRaw;

    -- Extract Subject and Group Information

    DECLARE @group_name VARCHAR(256);
    DECLARE @subject_name NVARCHAR(255);
    DECLARE @subject_year INT;
    DECLARE @teacher_pesel CHAR(11);

    SELECT 
        @subject_name = TRIM(SUBSTRING(RawLine, 1, LEN(RawLine) - CHARINDEX(' ', REVERSE(RawLine)))),
        @subject_year = CAST(SUBSTRING(RawLine, LEN(RawLine) - CHARINDEX(' ', REVERSE(RawLine)) + 2, CHARINDEX(',', RawLine) - LEN(RawLine) + CHARINDEX(' ', REVERSE(RawLine)) - 2) AS INT),
        @teacher_pesel = SUBSTRING(RawLine, CHARINDEX(',', RawLine) + 1, 11)
    FROM StagingCSV
    WHERE LineNumber = 1;

    SELECT 
        @group_name = TRIM(SUBSTRING(RawLine, CHARINDEX(' ', RawLine) + 1, LEN(RawLine) - CHARINDEX(' ', RawLine)))
    FROM StagingCSV
    WHERE LineNumber = 2;

    -- Extract and insert dates into the Dates table
    DECLARE @dates NVARCHAR(MAX);
    DECLARE @date NVARCHAR(10);
    DECLARE @pos INT;

    -- Extract the cleaned dates from the 3rd line
    SELECT @dates = REPLACE(RawLine, ',,', ',')
    FROM StagingCSV
    WHERE LineNumber = 3;

    -- Initialize the position for parsing
    SET @pos = CHARINDEX(',', @dates);

    -- Parse and insert each date into the Dates table
    WHILE @pos > 0
    BEGIN
        SET @date = LEFT(@dates, @pos - 1); -- Get the current date
        SET @dates = SUBSTRING(@dates, @pos + 1, LEN(@dates)); -- Remove the processed date
        SET @pos = CHARINDEX(',', @dates); -- Find the next comma

        -- Insert into the Dates table (ignore empty entries)
        IF LEN(@date) > 0
            INSERT INTO StagingDates (date)
            VALUES (CAST(@date AS DATE));
    END;

    -- Insert the last date (if any, after the loop ends)
    IF LEN(@dates) > 0
        INSERT INTO StagingDates (date)
        VALUES (CAST(@dates AS DATE));


    -- Loop through each student's row after the headers and insert records.

    DECLARE @lineNumber INT = 4; -- Start from line 4 assuming lines 1-3 are headers
    DECLARE @totalLines INT = (SELECT COUNT(*) FROM StagingCSV);
    DECLARE @student_name NVARCHAR(255);
    DECLARE @student_pesel CHAR(11);
    DECLARE @attendance_data NVARCHAR(MAX);
    DECLARE @dateIndex INT;

    DECLARE @startIndex INT = 2;
    DECLARE @endIndex INT = 0;
    DECLARE @value NVARCHAR(10); -- Holds the current attendance status ('True' or 'False')

    WHILE @lineNumber <= @totalLines - 1

    BEGIN

        SELECT 
                @student_name = TRIM(SUBSTRING(RawLine, 1, CHARINDEX(',', RawLine) - 1)),
                @student_pesel = TRIM(SUBSTRING(RawLine, CHARINDEX(',', RawLine) + 1, 11)),
                @attendance_data = TRIM(SUBSTRING(RawLine, CHARINDEX(',', RawLine) + 12, LEN(RawLine)))
            FROM StagingCSV
            WHERE LineNumber = @lineNumber;

        CREATE TABLE StagingAttendance (
                attendanceDate DATE NOT NULL,
                status BIT );
        
        SET @dateIndex = 1;
        SET @startIndex = 2;
        SET @endIndex = 0;

        WHILE @dateIndex <= (SELECT COUNT(*) FROM StagingDates)
        BEGIN
            SET @endIndex = CAST(CHARINDEX(',', @attendance_data, @startIndex) AS INT);
            IF @endIndex = 0
                SET @endIndex = LEN(@attendance_data) + 1;

            -- Extract the current attendance value
            SET @value = TRIM(SUBSTRING(@attendance_data, @startIndex, @endIndex - @startIndex));

            INSERT INTO StagingAttendance (attendanceDate, status)
            SELECT 
                D.date, 
                CASE 
                    WHEN @value = 'True' THEN 1
                    WHEN @value = 'False' THEN 0
                    ELSE NULL -- Handle unexpected cases if needed
                END
            FROM StagingDates D
            WHERE D.id = @dateIndex
            AND @dateIndex <= LEN(@attendance_data);

            SET @startIndex = @endIndex + 1;
            -- Skip next True/False value
            SET @endIndex = CAST(CHARINDEX(',', @attendance_data, @startIndex) AS INT);
            IF @endIndex = 0
            SET @endIndex = LEN(@attendance_data) + 1;
            SET @startIndex = @endIndex + 1;

            SET @dateIndex = @dateIndex + 1;
        END

            -- Insert attendance data into the main Attendance table
        INSERT INTO Attendance (StudentName, StudentPesel, SubjectName, SubjectYear, AttendanceDate, AttendanceStatus)
            SELECT 
                @student_name, 
                @student_pesel, 
                @subject_name, 
                @subject_year, 
                attendanceDate, 
                status
        FROM StagingAttendance;

        -- Drop the temporary table
        DROP TABLE StagingAttendance;

        -- Move to the next student row
        SET @lineNumber = @lineNumber + 1;
    END


    -- Fill Attendance rate using the last line
   
    SET @dateIndex = 1;
    SET @startIndex = 3;
    SET @endIndex = 0;

    SELECT 
        @attendance_data = TRIM(RawLine)
        FROM StagingCSV
        WHERE LineNumber = @totalLines;


    WHILE @dateIndex <= (SELECT COUNT(*) FROM StagingDates)
        BEGIN
            SET @endIndex = CAST(CHARINDEX(',', @attendance_data, @startIndex) AS INT);
            IF @endIndex = 0
                SET @endIndex = LEN(@attendance_data) + 1;

            -- Extract the current attendance value
            SET @value = TRIM(SUBSTRING(@attendance_data, @startIndex, @endIndex - @startIndex));

            INSERT INTO StagingAttendanceRate (date, attendanceRate)
            SELECT 
                D.date, 
                CAST(@value AS FLOAT)
            FROM StagingDates D
            WHERE D.id = @dateIndex
            AND @dateIndex <= LEN(@attendance_data);

            SET @startIndex = @endIndex + 1;
            -- Skip next True/False value
            SET @endIndex = CAST(CHARINDEX(',', @attendance_data, @startIndex) AS INT);
            IF @endIndex = 0
            SET @endIndex = LEN(@attendance_data) + 1;
            SET @startIndex = @endIndex + 1;

            SET @dateIndex = @dateIndex + 1;
    END

    -- Extract and insert grades into the StagingGrades table
    -- get grade data from Grades table from School database
    INSERT INTO StagingGrades (studentPesel, date, grade)
        SELECT S.pesel, G.grade_date, G.grade
        FROM School.dbo.Grades G
        INNER JOIN School.dbo.Students S ON G.student_id = S.id
        WHERE G.subject_id = (
            SELECT subject_id
            FROM School.dbo.Subjects Sub
            WHERE Sub.name = @subject_name AND Sub.year = @subject_year
        ) AND S.pesel IN (SELECT StudentPesel FROM Attendance) ;



    INSERT INTO StagingAverageGrades (date, grades_number, average_grade)
        SELECT G.date, COUNT(G.grade) as grades_number, AVG(CAST(G.grade AS FLOAT)) as average_grade
        FROM StagingDates D
        INNER JOIN StagingGrades G ON D.date = G.date
        GROUP BY G.date;
    

    -- Inserting data to the Fact Table
        CREATE TABLE #ETLConductingLesson (
                date_id INT,
                subject_id INT,
                teacher_id INT,
                group_id INT,
                attendance_rate FLOAT,
                average_grade FLOAT,
                grades_number INT
        );

        INSERT INTO #ETLConductingLesson (date_id, subject_id, teacher_id, group_id, attendance_rate, average_grade, grades_number)
        SELECT 
                DD.id AS date_id, 
                Sub.id AS subject_id, 
                T.id AS teacher_id, 
                G.id AS group_id,  
                AR.attendanceRate AS attendance_rate, 
                ISNULL(AG.average_grade, 0) AS average_grade, 
                ISNULL(AG.grades_number, 0)  AS grades_number 
        FROM StagingDates D
        JOIN SchoolDW.dbo.Dates DD ON D.date = DD.date
        JOIN SchoolDW.dbo.Subjects Sub ON Sub.name = @subject_name AND Sub.year = @subject_year
        JOIN SchoolDW.dbo.Groups G ON G.name = @group_name
        LEFT JOIN StagingAttendanceRate AR ON D.date = AR.date
        LEFT JOIN StagingAverageGrades AG ON D.date = AG.date
        JOIN SchoolDW.dbo.Teachers T ON T.pesel = @teacher_pesel
        GROUP BY DD.id, Sub.id, T.id, G.id, AR.attendanceRate, AG.average_grade, ISNULL(AG.grades_number, 0);

        -- Merge data into the Fact Table
        MERGE INTO ConductingLesson AS TT
        USING #ETLConductingLesson AS ST
        ON TT.date_id = ST.date_id AND TT.subject_id = ST.subject_id AND TT.teacher_id = ST.teacher_id AND TT.group_id = ST.group_id
        WHEN NOT MATCHED THEN
                INSERT (date_id, subject_id, teacher_id, group_id, attendance_rate, average_grade, grades_number)
                VALUES (ST.date_id, ST.subject_id, ST.teacher_id, ST.group_id, ST.attendance_rate, ST.average_grade, ST.grades_number);

        DROP TABLE #ETLConductingLesson;

    -- Fetch the next file
    FETCH NEXT FROM FileCursor INTO @FileName;
END;

-- Cleanup
CLOSE FileCursor;
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS StagingDates;
DROP TABLE IF EXISTS StagingAttendanceRate;
DROP TABLE IF EXISTS StagingCSVRaw;
DROP TABLE IF EXISTS StagingCSV;
DROP TABLE IF EXISTS StagingGrades;
DROP TABLE IF EXISTS StagingAverageGrades;
DROP TABLE IF EXISTS StagingAttendance;
DEALLOCATE FileCursor;

DROP TABLE #Files;
