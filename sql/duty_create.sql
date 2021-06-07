CREATE TABLE IF NOT EXISTS DutyRules (
	RuleID			SERIAL			PRIMARY KEY,
	BeginDate		DATE			NOT NULL,
	EndDate			DATE,
	BeginTime		TIME			NOT NULL,
	EndTime			TIME			NOT NULL,
	DOW				VARCHAR(7)		NOT NULL
);

CREATE TABLE IF NOT EXISTS GuardDuty (
	DutyID 			SERIAL			PRIMARY KEY,
	CheckpointID	INT				REFERENCES Checkpoints(CheckpointID) NOT NULL,
	Login			TEXT			REFERENCES Person(Login) NOT NULL,
	RuleID			INT				REFERENCES DutyRules(RuleID) NOT NULL
);

CREATE TABLE IF NOT EXISTS DriverDuty (
	DutyID 			SERIAL			PRIMARY KEY,
	PlateNumber		TEXT			REFERENCES Trucks(PlateNumber) NOT NULL,
	Login			TEXT			REFERENCES Person(Login) NOT NULL,
	RuleID			INT				REFERENCES DutyRules(RuleID) NOT NULL
);