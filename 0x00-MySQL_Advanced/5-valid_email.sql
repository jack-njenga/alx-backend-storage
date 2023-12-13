-- creates a trigger that resets the attribute valid_email only when the email has been changed.
DELIMITER |

CREATE TRIGGER validateemailv2 AFTER UPDATE on users
FOR EACH ROW
BEGIN
	UPDATE users set valid_email = 0 where users.email!= NEW.email AND users.id = NEW.id;
END;
|
DELIMITER ;