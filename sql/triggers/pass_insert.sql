CREATE OR REPLACE FUNCTION LogPassRecordIns()
RETURNS TRIGGER
AS $$
BEGIN
	INSERT INTO LogActions VALUES 
	(current_user, NOW(), 'Created pass record №' || NEW.RecordID);
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER LogPassRecordIns
AFTER INSERT
ON PassRecords
	FOR EACH ROW
		EXECUTE PROCEDURE LogPassRecordIns();
