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

GRANT ALL PRIVILEGES ON Passrecords TO guard;
GRANT SELECT ON Accounts TO guard;
GRANT SELECT ON Person TO guard;
