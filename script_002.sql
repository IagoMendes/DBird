USE dbird;

DROP TRIGGER IF EXISTS trig_delete_user;
delimiter //
CREATE TRIGGER trig_delete_user
	BEFORE UPDATE ON dbird.users
	FOR EACH ROW
	BEGIN
		IF NEW.is_activeu = 0 THEN
			UPDATE dbird.post 
            SET is_activep = 0
			WHERE post.id_user = NEW.id_user;
		END IF;
	END//
delimiter ;

DROP TRIGGER IF EXISTS trig_delete_post;
delimiter //
CREATE TRIGGER trig_delete_post
	AFTER UPDATE ON post
	FOR EACH ROW
	BEGIN
		IF NEW.is_activep = 0 THEN
			UPDATE user_mention 
            INNER JOIN post USING(id_post) 
            INNER JOIN bird_mention USING(id_post)
            SET is_activeum = 0,
            is_activebm = 0
			WHERE post.id_post = user_mention.id_post AND post.id_post = bird_mention.id_post;
		END IF;
	END//
delimiter ;