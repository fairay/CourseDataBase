DROP TABLE Accounts CASCADE;

CREATE TABLE IF NOT EXISTS Accounts(
	Login 			TEXT 			PRIMARY KEY,
	PersType 		TEXT 			NOT NULL,
	Salt 			TEXT			NOT NULL,
	HashedPassword	TEXT			NOT NULL
);

DROP TABLE Person CASCADE;
CREATE TABLE IF NOT EXISTS Person(
	Login			TEXT			REFERENCES Accounts(Login) NOT NULL PRIMARY KEY,
	Surname 		VARCHAR(40) 	NOT NULL,
	Forename 		VARCHAR(40)		NOT NULL,
	DOB				DATE			NOT NULL,
	Gender			CHAR			NOT NULL,
	PhoneNumber 	TEXT
);

DROP TABLE Delivery CASCADE;
CREATE TABLE IF NOT EXISTS Delivery (
	OrderID 		SERIAL			PRIMARY KEY,
	Login			TEXT			REFERENCES Person(Login),
	Address 		TEXT 			NOT NULL,
	PhoneNumber 	VARCHAR(40)		NOT NULL,
	CreationTime	TIMESTAMP		NOT NULL,
	CompletionTime	TIMESTAMP,
	Status			VARCHAR(20)		NOT NULL,
	Description 	TEXT			NOT NULL
);
ALTER TABLE Delivery 
ADD CONSTRAINT check_status
CHECK (Status='delivered' OR Status='in_transit' OR Status='not_assigned');


CREATE TABLE IF NOT EXISTS Trucks (
	PlateNumber		TEXT			PRIMARY KEY,
	Category		VARCHAR(40)		NOT NULL,
	Model			VARCHAR(40)		NOT NULL
);
CREATE TABLE IF NOT EXISTS Checkpoints (
	CheckpointID	SERIAL			PRIMARY KEY,
	Address 		TEXT 			NOT NULL,
	PhoneNumber 	VARCHAR(40)		NOT NULL
);


CREATE TABLE IF NOT EXISTS PassRecords (
	RecordID 		SERIAL			PRIMARY KEY,
	PlateNumber		TEXT			REFERENCES Trucks(PlateNumber) NOT NULL,
	CheckpointID	INT				REFERENCES Checkpoints(CheckpointID) NOT NULL,
	PassTime		TIMESTAMP		NOT NULL,
	Direction		VARCHAR(3)		NOT NULL
	CONSTRAINT direction_valid CHECK (Direction='in' OR Direction='out')
);


CREATE TABLE IF NOT EXISTS GuardDutys (
	DutyID 			SERIAL			PRIMARY KEY,
	CheckpointID	INT				REFERENCES Checkpoints(CheckpointID) NOT NULL,
	Login			TEXT			REFERENCES Person(Login) NOT NULL,
	BeginDate		DATE			NOT NULL,
	EndDate			DATE,
	BeginTime		TIME			NOT NULL,
	EndTime			TIME			NOT NULL,
	DOW				VARCHAR(7)		NOT NULL
);

CREATE TABLE IF NOT EXISTS DriverDutys (
	DutyID 			SERIAL			PRIMARY KEY,
	PlateNumber		TEXT			REFERENCES Trucks(PlateNumber) NOT NULL,
	Login			TEXT			REFERENCES Person(Login) NOT NULL,
	BeginDate		DATE			NOT NULL,
	EndDate			DATE,
	BeginTime		TIME			NOT NULL,
	EndTime			TIME			NOT NULL,
	DOW				VARCHAR(7)
);

CREATE TABLE IF NOT EXISTS LogActions (
	Actor 		VARCHAR(15)			NOT NULL,
	ActTime		TIMESTAMP			NOT NULL,
	Description	TEXT
);