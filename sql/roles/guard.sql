REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM guard;
DROP USER guard;
CREATE ROLE guard WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	NOINHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'guard';

GRANT SELECT, INSERT ON Passrecords TO guard;
GRANT SELECT ON Accounts TO guard;
GRANT SELECT ON Person TO guard;
GRANT SELECT ON GuardDutys TO guard;
GRANT SELECT, INSERT ON PassRecords TO guard;
GRANT ALL PRIVILEGES ON SEQUENCE passrecords_recordid_seq TO guard;
GRANT SELECT ON Checkpoints TO guard;
GRANT SELECT ON Trucks TO guard;
GRANT INSERT ON LogActions TO guard;

GRANT SELECT ON GuardDuty TO guard;
GRANT SELECT ON DutyRules TO guard;
