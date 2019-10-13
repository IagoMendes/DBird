USE dbird;

DROP TRIGGER IF EXISTS trig_delete_user;
delimiter //
CREATE TRIGGER trig_delete_user
	AFTER UPDATE ON users
	FOR EACH ROW
	BEGIN
		IF NEW.is_activeu = 0 THEN
			UPDATE post 
            INNER JOIN user_bird USING(id_user) 
            SET is_activep = 0,
            is_activebm = 0
			WHERE post.id_user = users.id_user;
		END IF;
	END;//

DROP TRIGGER IF EXISTS trig_delete_post;
delimiter //
CREATE TRIGGER trig_delete_post
	AFTER UPDATE ON post
	FOR EACH ROW
	BEGIN
		IF NEW.is_activep = 0 THEN
			UPDATE user_metion 
            INNER JOIN post USING(id_post) 
            INNER JOIN bird_mention USING(id_post)
            SET is_activeum = 0,
            is_activebm = 0
			WHERE post.id_post = user_mention.id_post AND post.id_post = bird_mention.id_post;
		END IF;
	END;//