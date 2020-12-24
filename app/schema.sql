DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR,
  email VARCHAR(40) UNIQUE NOT NULL 
);

INSERT INTO users (username,password,email) VALUES ('bobhenson','andwhat13','bob@gmail.com');
