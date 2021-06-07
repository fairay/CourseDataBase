CREATE OR REPLACE FUNCTION LogDeliveryUpd()
RETURNS TRIGGER
AS $$
BEGIN
	IF NEW.Status = 'delivered' THEN 
		INSERT INTO LogActions VALUES 
		(current_user, NOW(), 'Set delivery №' || NEW.OrderID || ' status = delivered');
	ELSE
		INSERT INTO LogActions VALUES 
		(current_user, NOW(), 'Assigned delivery №' || NEW.OrderID || ' to ' || NEW.Login);
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER LogDeliveryUpd
AFTER UPDATE
ON Delivery
	FOR EACH ROW
		EXECUTE PROCEDURE LogDeliveryUpd();

