REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM admin;
DROP USER admin;
CREATE ROLE admin WITH
	LOGIN
	SUPERUSER
	NOCREATEDB
	NOCREATEROLE
	NOINHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'admin';
