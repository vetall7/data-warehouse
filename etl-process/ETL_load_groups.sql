use SchoolDW;
GO

Declare @EntryDate datetime; 
SELECT @EntryDate = GETDATE();

MERGE INTO Groups as TT
	USING School.dbo.Groups as ST
		ON TT.name = ST.name
			WHEN Not Matched
				THEN
					INSERT Values (
					ST.name,
                    ST.grade,
                    @EntryDate,
                    NULL
					)
			WHEN Matched -- when Group name match, 
			-- but Grade doesn't...
				AND ST.grade <> TT.grade
			THEN
				UPDATE
				SET TT.expiration_date = @EntryDate
            WHEN Not Matched BY Source
			AND TT.Name != 'UNKNOWN' -- do not update the UNKNOWN tuple
			THEN
				UPDATE
				SET TT.expiration_date = @EntryDate
			;

-- INSERTING CHANGED ROWS TO THE GENRES TABLE
INSERT INTO Groups(
	name, 
	grade,  
	creation_date, 
	expiration_date
	)
	SELECT 
		name,
        grade,
        @EntryDate, 
		NULL 
	FROM School.dbo.Groups
	EXCEPT
	SELECT 
		name,
        grade,
        @EntryDate, 
		NULL 
	FROM Groups;