USE SchoolDW;
GO

MERGE INTO Subjects as TT
	USING School.dbo.Subjects as ST
		ON TT.Name = ST.Name AND TT.Year = ST.Year
			WHEN Not Matched
				THEN
					INSERT
					Values (
					ST.Year, ST.Name
					)
			WHEN Not Matched By Source
				Then
					DELETE
			;
