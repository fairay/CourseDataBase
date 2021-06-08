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

