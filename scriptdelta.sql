USE dbird;

CREATE TABLE like_post
(
    id_post INT NOT NULL,
    id_user INT NOT NULL,
    like_value TINYINT NOT NULL,
    PRIMARY KEY (id_post, id_user),
    FOREIGN KEY (id_user) REFERENCES users (id_user),
    FOREIGN KEY (id_post) REFERENCES post  (id_post)
);