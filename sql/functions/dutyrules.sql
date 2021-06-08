CREATE OR REPLACE FUNCTION DutyByRange(BeginD DATE, EndD DATE)
RETURNS TABLE (LIKE DutyRules)
AS
$$
BEGIN
	RETURN QUERY (
		SELECT *
		FROM DutyRules 
		WHERE (
			((EndD IS NULL) AND  -- Диапазон от
			(
				(EndDate IS NULL) OR 
				(EndDate >= BeginD)
			))  OR
			((EndD IS NOT NULL) AND -- Диапазон от и до
			(
				((EndDate IS NULL) AND (BeginDate <= EndD)) OR 
				(NOT (EndDate IS NULL) AND 
				   (
				   (BeginDate BETWEEN BeginD AND EndD) OR
				   (EndDate BETWEEN BeginD AND EndD) OR
				   (BeginD BETWEEN BeginDate AND EndDate)
					)
				)
			))
		)
	);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION DutyAtMoment(Moment TIMESTAMP)
RETURNS TABLE (LIKE DutyRules)
AS
$$
DECLARE
	NowDate	DATE;
	NowTime TIME;
	NowDow TEXT;
BEGIN
	SELECT *
	FROM CAST(Moment AS DATE)
	INTO NowDate;
	
	SELECT *
	FROM CAST(Moment AS TIME)
	INTO NowTime;
	
	SELECT CAST(Date_Part - 1 AS TEXT)
	FROM EXTRACT(isodow FROM NowDate)
	INTO NowDow;
	
	RETURN QUERY (
		SELECT *
		FROM DutyByRange(NowDate, NowDate) 
		WHERE (
			(POSITION(NowDow in Dow) != 0) AND
			(NowTime BETWEEN BeginTime AND EndTime)
			)
	);
END;
$$
LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION CurrentDuty()
RETURNS TABLE (LIKE DutyRules)
AS
$$
BEGIN
	RETURN QUERY (
		SELECT *
		FROM DutyAtMoment(CAST(NOW() AS TIMESTAMP) ) 
	);
END;
$$
LANGUAGE plpgsql;

SELECT * FROM CurrentDuty();
