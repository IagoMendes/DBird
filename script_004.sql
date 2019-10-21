USE dbird;

CREATE VIEW popular AS
    SELECT u.id_user as id, u.user_name as uname, u.city as city, COUNT(lp.like_value) as likes
    FROM 
        users as u
        INNER JOIN post as p USING (id_user)
        INNER JOIN like_post as lp USING (id_post)
    WHERE
        lp.like_value = 1 AND
        u.is_activeu = 1 AND
        p.is_activep = 1
    GROUP BY u.city
    ORDER BY likes DESC