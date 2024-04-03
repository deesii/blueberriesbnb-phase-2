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

INSERT INTO users (email, password) VALUES ('blob@hotmail.com', 'scrypt:32768:8:1$M60JBIdOoYHi08nh$137a9beb34d68195ddf14648e2f56a4763e5514ddda166c8f24b8a19a439e8eea76693c056dfe379652210637a5cd31cd334e642773518dbb20cf4554cf80322');
INSERT INTO users (email, password) VALUES ('email2@hotmail.com', 'scrypt:32768:8:1$VHIoPXPuUnh06Q0z$03481d7e4881aa6d4ec6536fb3b237eb31f5d6a295c40ec91018232c08e63e1d7134711f07012f605c2e9c45b0ebd7d042914a9992a10ae5fef564582a8e5cfd');
INSERT INTO users (email, password) VALUES ('email3@email.com', 'scrypt:32768:8:1$apjurr0BybKD5iFD$18e78d03cbff3c49feb56ff2ac934aba6d2cbd0026f1a3fba0a22c3a3cf4c66f6a7f99bca234a74e0bcf4417ada78c2457e09945f47819bf4dbc85b016022e46');
INSERT INTO users (email, password) VALUES ('email4@email.com', 'scrypt:32768:8:1$SLdsXarTogkK2Lsm$5accedbf4c228a605a4163260d39641834dc259ff0aa4a35cc858cfa8575d3896aa68286a9015062e0015a5d77653a50ab2a427c009bc6a2e84f7e694f849daf');
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property1', 1, 'hot', 25.40);
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property2', 2, 'cold', 45.70);
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property3', 3, 'windy', 83.00);
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property4', 4, 'snow', 56.80);
INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES ('Property5', 4, 'cloud', 83.20);
INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (1, '2024-03-27', '2024-03-29', TRUE, 2);
INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (3, '2024-07-01', '2024-07-10', TRUE, 4);
INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (3, '2024-06-01', '2024-06-10', TRUE, 4);
INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (3, '2024-05-01', '2024-05-10', FALSE, 4);




















