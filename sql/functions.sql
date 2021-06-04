--
-- GUARDS
--
CREATE OR REPLACE FUNCTION GDutyRange(BeginD DATE, EndD DATE)
RETURNS TABLE (LIKE GuardDutys)
AS
$$
BEGIN
	RETURN QUERY (
		SELECT *
		FROM GuardDutys 
		WHERE (
			((EndDate IS NULL) AND (BeginDate <= EndD)) OR 
		    (NOT (EndDate IS NULL) AND 
			   (
			   (BeginDate BETWEEN BeginD AND EndD) OR
			   (EndDate BETWEEN BeginD AND EndD) OR
			   (BeginD BETWEEN BeginDate AND EndDate)
				)
			)
		)
	);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION GDutyInf(BeginD DATE)
RETURNS TABLE (LIKE GuardDutys)
AS
$$
BEGIN
	RETURN QUERY (
		SELECT *
		FROM GuardDutys 
		WHERE (
			(EndDate IS NULL) OR 
			(EndDate >= BeginD)
		)
	);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION GDutyNow()
RETURNS TABLE (LIKE GuardDutys)
AS
$$
DECLARE
	NowDate	DATE;
	NowTime TIME;
	NowDow TEXT;
BEGIN
	SELECT *
	FROM CAST(NOW() AS DATE)
	INTO NowDate;
	
	SELECT *
	FROM CAST(NOW() AS TIME)
	INTO NowTime;
	
	SELECT CAST(Date_Part - 1 AS TEXT)
	FROM EXTRACT(isodow FROM NowDate)
	INTO NowDow;
	
	RETURN QUERY (
		SELECT *
		FROM GDutyRange(NowDate, NowDate) 
		WHERE (
			(POSITION(NowDow in Dow) != 0) AND
			(NowTime BETWEEN BeginTime AND EndTime)
			)
	);
END;
$$
LANGUAGE plpgsql;

--
-- DRIVERS
--
CREATE OR REPLACE FUNCTION DDutyRange(BeginD DATE, EndD DATE)
RETURNS TABLE (LIKE DriverDutys)
AS
$$
BEGIN
	RETURN QUERY (
		SELECT *
		FROM DriverDutys 
		WHERE (
			((EndDate IS NULL) AND (BeginDate <= EndD)) OR 
		    (NOT (EndDate IS NULL) AND 
			   (
			   (BeginDate BETWEEN BeginD AND EndD) OR
			   (EndDate BETWEEN BeginD AND EndD) OR
			   (BeginD BETWEEN BeginDate AND EndDate)
				)
			)
		)
	);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION DDutyInf(BeginD DATE)
RETURNS TABLE (LIKE DriverDutys)
AS
$$
BEGIN
	RETURN QUERY (
		SELECT *
		FROM DriverDutys 
		WHERE (
			(EndDate IS NULL) OR 
			(EndDate >= BeginD)
		)
	);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION DDutyNow()
RETURNS TABLE (LIKE DriverDutys)
AS
$$
DECLARE
	NowDate	DATE;
	NowTime TIME;
	NowDow TEXT;
BEGIN
	SELECT *
	FROM CAST(NOW() AS DATE)
	INTO NowDate;
	
	SELECT *
	FROM CAST(NOW() AS TIME)
	INTO NowTime;
	
	SELECT CAST(Date_Part - 1 AS TEXT)
	FROM EXTRACT(isodow FROM NowDate)
	INTO NowDow;
	
	RETURN QUERY (
		SELECT *
		FROM DDutyRange(NowDate, NowDate) 
		WHERE (
			(POSITION(NowDow in Dow) != 0) AND
			(NowTime BETWEEN BeginTime AND EndTime)
			)
	);
END;
$$
LANGUAGE plpgsql;

SELECT * 
FROM DDutyRange('2021-06-10', '2021-06-12');

SELECT * 
FROM DDutyInf('2021-06-11');

SELECT *
FROM DDutyNow();