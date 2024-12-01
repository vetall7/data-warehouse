use SchoolDW
go

-- Fill DimDates Lookup Table
-- Step a: Declare variables use in processing
Declare @StartDate date; 
Declare @EndDate date;

-- Step b:  Fill the variable with values for the range of years needed
SELECT @StartDate = '2019-01-01', @EndDate = '2025-12-31';

-- Step c:  Use a while loop to add dates to the table
Declare @DateInProcess datetime = @StartDate;

While @DateInProcess <= @EndDate
	Begin
	--Add a row into the date dimension table for this date
		Insert Into [dbo].[Dates] 
		( [Date]
		, [Year]
		, [MonthNo]
		, [DayOfMonthNo]
        , [Semester]
		)
		Values ( 
		  @DateInProcess -- [Date]
		  , Cast( Year(@DateInProcess) as varchar(4)) -- [Year]
		  , Cast( Month(@DateInProcess) as int) -- [MonthNo]
		  , Cast( DATEPART(d, @DateInProcess) as int) -- [DayOfMonthNo]
		  , CASE
				WHEN DATEPART(mm, @DateInProcess) BETWEEN 2 AND 9 THEN 'letni'
				ELSE 'zimowy'
			END
		);  
		-- Add a day and loop again
		Set @DateInProcess = DateAdd(d, 1, @DateInProcess);
	End
go
