DROP DATABASE IF EXISTS dbird;
CREATE DATABASE dbird DEFAULT CHARACTER SET utf8;
USE dbird;

CREATE TABLE users (
  id_user INT NOT NULL AUTO_INCREMENT,
  user_name VARCHAR(50) NOT NULL,
  email VARCHAR(45) NOT NULL,
  city VARCHAR(20) NOT NULL,
  is_activeu TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (id_user, user_name)
);              

CREATE TABLE post (
  id_post INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(45) NOT NULL,
  content VARCHAR(140) NULL,
  url VARCHAR(45) NULL,
  id_user INT NOT NULL,
  is_activep TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (id_post),
  CONSTRAINT fk_post_user
    FOREIGN KEY (id_user) REFERENCES users (id_user)
);

CREATE TABLE views (
  id_user INT NOT NULL,
  id_post INT NOT NULL,
  browser VARCHAR(10) NOT NULL,
  IP VARCHAR(15) NOT NULL,
  device VARCHAR(20) NOT NULL,
  view_date TIMESTAMP NOT NULL,
  PRIMARY KEY (id_user, id_post),
  
  CONSTRAINT fk_user_post_user1
    FOREIGN KEY (id_user) REFERENCES users (id_user),
    
  CONSTRAINT fk_user_post_post1
    FOREIGN KEY (id_post) REFERENCES post (id_post)
);

CREATE TABLE bird (
  id_bird INT NOT NULL AUTO_INCREMENT,
  bird_name VARCHAR(30) NULL,
  PRIMARY KEY (id_bird)
);

CREATE TABLE user_bird (
  id_user INT NOT NULL,
  id_bird INT NOT NULL,
  is_activeub TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (id_user, id_bird),
  
  CONSTRAINT fk_user_bird_user1
    FOREIGN KEY (id_user) REFERENCES users (id_user),
    
  CONSTRAINT fk_user_bird_bird1
    FOREIGN KEY (id_bird) REFERENCES bird (id_bird)
);

CREATE TABLE bird_mention (
  id_post INT NOT NULL,
  id_bird INT NOT NULL,
  is_activebm TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (id_post, id_bird),
  
  CONSTRAINT fk_bird_mention_post1
    FOREIGN KEY (id_post) REFERENCES post (id_post),
    
  CONSTRAINT fk_bird_mention_bird1
    FOREIGN KEY (id_bird) REFERENCES bird (id_bird)
  );

CREATE TABLE user_mention (
  id_post INT NOT NULL,
  id_user INT NOT NULL,
  is_activeum TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (id_post, id_user),
  
  CONSTRAINT fk_user_mention_post1
    FOREIGN KEY (id_post) REFERENCES post (id_post),
    
  CONSTRAINT fk_user_mention_user1
    FOREIGN KEY (id_user) REFERENCES users (id_user)
);