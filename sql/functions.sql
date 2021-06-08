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

-------------------------------------------------------------------
-- 								GUARDS							 --
-------------------------------------------------------------------
CREATE TYPE GDutyJoin AS
(
	DutyID 			INT,
	CheckpointID	INT,
	Login			TEXT,
	
	RuleID			INT,
	BeginDate		DATE,
	EndDate			DATE,
	BeginTime		TIME,
	EndTime			TIME,
	DOW				VARCHAR(7)
);

CREATE OR REPLACE FUNCTION MomentGDuty(Moment TIMESTAMP, QLogin TEXT, CheckID INT)
RETURNS SETOF GDutyJoin AS
$$
BEGIN
	RETURN QUERY (
		SELECT DutyID, CheckpointID, Login, t1.RuleID, 
				BeginDate, EndDate, BeginTime, EndTime, DOW
		FROM GuardDuty JOIN DutyAtMoment(Moment) AS "t1" ON GuardDuty.RuleID = t1.RuleID
		WHERE (
			((QLogin IS NULL) OR (QLogin = Login)) AND
			((CheckID IS NULL) OR (CheckID = CheckpointID))
		)
	);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION CurrentGDuty(QLogin TEXT, CheckID INT)
RETURNS SETOF GDutyJoin AS
$$
BEGIN
	RETURN QUERY (
		SELECT DutyID, CheckpointID, Login, t1.RuleID, 
				BeginDate, EndDate, BeginTime, EndTime, DOW
		FROM GuardDuty JOIN CurrentDuty() AS "t1" ON GuardDuty.RuleID = t1.RuleID
		WHERE (
			((QLogin IS NULL) OR (QLogin = Login)) AND
			((CheckID IS NULL) OR (CheckID = CheckpointID))
		)
	);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION GetGDuty(BeginD DATE, EndD DATE, QLogin TEXT, CheckID INT)
RETURNS SETOF GDutyJoin AS
$$
BEGIN
	RETURN QUERY (
		SELECT DutyID, CheckpointID, Login, t1.RuleID, 
				BeginDate, EndDate, BeginTime, EndTime, DOW
		FROM GuardDuty JOIN DutyByRange(BeginD, EndD) AS "t1" ON GuardDuty.RuleID = t1.RuleID
		WHERE (
			((QLogin IS NULL) OR (QLogin = Login)) AND
			((CheckID IS NULL) OR (CheckID = CheckpointID))
		)
	);
END;
$$
LANGUAGE plpgsql;


SELECT * FROM MomentGDuty(CAST(NOW() + interval '0 day' AS TIMESTAMP), NULL, NULL);
SELECT * FROM CurrentGDuty(NULL, NULL);
SELECT * FROM GetGDuty(CAST(NOW() AS DATE), NULL, NULL, NULL);

-------------------------------------------------------------------
-- 								DRIVERS							 --
-------------------------------------------------------------------
CREATE TYPE DDutyJoin AS
(
	DutyID 			INT,
	PlateNumber		TEXT,
	Login			TEXT,
	
	RuleID			INT,
	BeginDate		DATE,
	EndDate			DATE,
	BeginTime		TIME,
	EndTime			TIME,
	DOW				VARCHAR(7)
);

CREATE OR REPLACE FUNCTION MomentDDuty(Moment TIMESTAMP, QLogin TEXT, PlateN TEXT)
RETURNS SETOF DDutyJoin AS
$$
BEGIN
	RETURN QUERY (
		SELECT DutyID, PlateNumber, Login, t1.RuleID, 
				BeginDate, EndDate, BeginTime, EndTime, DOW
		FROM DriverDuty JOIN DutyAtMoment(Moment) AS "t1" ON DriverDuty.RuleID = t1.RuleID
		WHERE (
			((QLogin IS NULL) OR (QLogin = Login)) AND
			((PlateN IS NULL) OR (PlateN = PlateNumber))
		)
	);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION CurrentDDuty(QLogin TEXT, PlateN TEXT)
RETURNS SETOF DDutyJoin AS
$$
BEGIN
	RETURN QUERY (
		SELECT DutyID, PlateNumber, Login, t1.RuleID, 
				BeginDate, EndDate, BeginTime, EndTime, DOW
		FROM DriverDuty JOIN CurrentDuty() AS "t1" ON DriverDuty.RuleID = t1.RuleID
		WHERE (
			((QLogin IS NULL) OR (QLogin = Login)) AND
			((PlateN IS NULL) OR (PlateN = PlateNumber))
		)
	);
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION GetDDuty(BeginD DATE, EndD DATE, QLogin TEXT, PlateN TEXT)
RETURNS SETOF DDutyJoin AS
$$
BEGIN
	RETURN QUERY (
		SELECT DutyID, PlateNumber, Login, t1.RuleID, 
				BeginDate, EndDate, BeginTime, EndTime, DOW
		FROM DriverDuty JOIN DutyByRange(BeginD, EndD) AS "t1" ON DriverDuty.RuleID = t1.RuleID
		WHERE (
			((QLogin IS NULL) OR (QLogin = Login)) AND
			((PlateN IS NULL) OR (PlateN = PlateNumber))
		)
	);
END;
$$
LANGUAGE plpgsql;


SELECT * FROM MomentDDuty(CAST(NOW() + interval '3 day' AS TIMESTAMP), NULL, NULL);
SELECT * FROM CurrentDDuty();
