CREATE TABLE users (
    name varchar PRIMARY KEY,
    password varchar NOT NULL
);

CREATE TABLE targets (
    uuid varchar PRIMARY KEY,
    name varchar NOT NULL,
    owner varchar REFERENCES users(name) NOT NULL
);
