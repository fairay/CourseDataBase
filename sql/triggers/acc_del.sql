CREATE OR REPLACE FUNCTION BanActiveAccDel()
RETURNS TRIGGER
AS $$
BEGIN
	IF (current_user = 'admin') AND (OLD.PersType NOT LIKE '~%') THEN
		RAISE EXCEPTION 'cannot delete active user';
	END IF;
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER BanActiveAccDel
BEFORE DELETE
ON Accounts
	FOR EACH ROW
		EXECUTE PROCEDURE BanActiveAccDel();
