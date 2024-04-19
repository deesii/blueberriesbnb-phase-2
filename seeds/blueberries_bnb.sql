-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.
-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS bookings;
DROP SEQUENCE IF EXISTS user_id_seq;
DROP TABLE IF EXISTS properties;
DROP SEQUENCE IF EXISTS property_id_seq;
DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS booking_id_seq;
-- Then, we recreate them
CREATE SEQUENCE IF NOT EXISTS user_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);
CREATE SEQUENCE IF NOT EXISTS property_id_seq;
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    property_name VARCHAR(255),
    user_id INTEGER,
    description VARCHAR(255),
    price_per_night FLOAT,
    constraint fk_user foreign key(user_id)
    references users(id)
    on delete cascade
);
CREATE SEQUENCE IF NOT EXISTS booking_id_seq;
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    property_id INTEGER,
    dates_booked_from VARCHAR,
    dates_booked_to VARCHAR,
    approved BOOLEAN,
    booker_id INTEGER,
    constraint fk_user foreign key(booker_id)
    references users(id)
    on delete cascade,
    constraint fk_property foreign key(property_id)
    references properties(id)
    on delete cascade
);

INSERT INTO users (email, password) VALUES ('blob@hotmail.com', 'scrypt:32768:8:1$D5hPxJWs7M5vRKiG$c7b58270a7aa94d2c46562cf7997242b2e125b64efc2e606334d6cec4bfa109476cf42834d6c6a2bc3a7e7e731c59652a14ea954d1f565796f6cd47aebd180bf');
INSERT INTO users (email, password) VALUES ('email2@hotmail.com', 'scrypt:32768:8:1$0oFHlAmpvTynd2Cu$827d8271180250b1c2ac44d0f43c98e5da2bdb85e3b2327cb97386794a5327e1ceeb56b672d2a7dc8f5074d9c7afabfe4526be6f347bf8e83a4acfa762972080');
INSERT INTO users (email, password) VALUES ('email3@email.com', 'scrypt:32768:8:1$4zgtCgNqq9Xa2XXL$182dcccc5e52fd9d8955b551c171a5de7da0703556bc6e4ebe8a6d21f089645c07d981294bbdc2a6500e8ea4a4a69d02744afb81686fbac214c6be27fe49319f');
INSERT INTO users (email, password) VALUES ('email4@email.com', 'scrypt:32768:8:1$Lf5XkQnZG1pgvVQX$cfb10e933e3e89deb8838717e44834cf5044edf092829fc46508acbd8ff6d97eb391749ff093fccb05be65e797321d41b2912b77715382640f8812f2b72b8693');
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property1', 1, 'hot', 25.40);
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property2', 2, 'cold', 45.70);
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property3', 3, 'windy', 83.00);
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property4', 4, 'snow', 56.80);
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property5', 4, 'cloud', 83.20);
INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (1, '2024-03-27', '2024-03-29', TRUE, 2);
INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (3, '2024-07-01', '2024-07-10', TRUE, 4);
INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (3, '2024-06-01', '2024-06-10', TRUE, 4);
INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (3, '2024-05-01', '2024-05-10', FALSE, 4);




















