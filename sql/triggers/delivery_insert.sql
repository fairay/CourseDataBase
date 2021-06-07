CREATE OR REPLACE FUNCTION LogDeliveryIns()
RETURNS TRIGGER
AS $$
BEGIN
	INSERT INTO LogActions VALUES 
	(current_user, NOW(), 'Created delivery №' || NEW.OrderID);
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER LogDeliveryIns
AFTER INSERT
ON Delivery
	FOR EACH ROW
		EXECUTE PROCEDURE LogDeliveryIns();

