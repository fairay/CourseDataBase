DROP TABLE Person CASCADE;
DROP TABLE Accounts CASCADE;

CREATE TABLE IF NOT EXISTS Accounts(
	Login 			TEXT 			PRIMARY KEY,
	PersType 		TEXT 			NOT NULL,
	Salt 			TEXT			NOT NULL,
	HashedPassword	TEXT			NOT NULL
);

CREATE TABLE IF NOT EXISTS Person(
	PersonID 		SERIAL			PRIMARY KEY,
	Login			TEXT			REFERENCES Accounts(Login) NOT NULL,
	Surname 		VARCHAR(40) 	NOT NULL,
	Forename 		VARCHAR(40)		NOT NULL,
	DOB				DATE			NOT NULL,
	Gender			CHAR			NOT NULL,
	PhoneNumber 	TEXT
);



