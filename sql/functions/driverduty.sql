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
