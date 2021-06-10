REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM driver;
DROP USER driver;
CREATE ROLE driver WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	NOINHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'driver';

GRANT SELECT, INSERT ON Passrecords TO driver;
GRANT SELECT ON Accounts TO driver;
GRANT SELECT ON Person TO driver;
GRANT SELECT, UPDATE ON Delivery TO driver;
GRANT SELECT ON DriverDutys TO driver;
GRANT INSERT ON LogActions TO driver;

GRANT SELECT ON DriverDuty TO driver;
GRANT SELECT ON DutyRules TO driver;