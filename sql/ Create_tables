-- Healthcare Revenue Cycle Intelligence Platform
-- Database Schema

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS charges;
DROP TABLE IF EXISTS workflow_status;
DROP TABLE IF EXISTS documentation_issues;
DROP TABLE IF EXISTS encounters;
DROP TABLE IF EXISTS providers;
DROP TABLE IF EXISTS divisions;

CREATE TABLE divisions (
    division_id SERIAL PRIMARY KEY,
    division_name VARCHAR(100) NOT NULL,
    avg_wrvu_per_visit NUMERIC(6,2),
    avg_collection_per_visit NUMERIC(10,2)
);

CREATE TABLE providers (
    provider_id SERIAL PRIMARY KEY,
    provider_name VARCHAR(100) NOT NULL,
    division_id INT REFERENCES divisions(division_id),
    provider_type VARCHAR(50),
    active_flag BOOLEAN DEFAULT TRUE
);

CREATE TABLE encounters (
    encounter_id SERIAL PRIMARY KEY,
    mrn VARCHAR(20),
    fin VARCHAR(20),
    provider_id INT REFERENCES providers(provider_id),
    division_id INT REFERENCES divisions(division_id),
    date_of_service DATE NOT NULL,
    encounter_type VARCHAR(50),
    payer_type VARCHAR(50),
    encounter_status VARCHAR(50)
);

CREATE TABLE documentation_issues (
    issue_id SERIAL PRIMARY KEY,
    encounter_id INT REFERENCES encounters(encounter_id),
    issue_type VARCHAR(100),
    issue_reason TEXT,
    issue_created_date DATE,
    issue_resolved_date DATE,
    issue_status VARCHAR(50)
);

CREATE TABLE workflow_status (
    workflow_id SERIAL PRIMARY KEY,
    encounter_id INT REFERENCES encounters(encounter_id),
    workflow_status VARCHAR(100),
    status_date DATE,
    email_count INT DEFAULT 0,
    last_action VARCHAR(150)
);

CREATE TABLE charges (
    charge_id SERIAL PRIMARY KEY,
    encounter_id INT REFERENCES encounters(encounter_id),
    charge_posted_date DATE,
    charge_amount NUMERIC(10,2),
    charge_status VARCHAR(50)
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    encounter_id INT REFERENCES encounters(encounter_id),
    payment_date DATE,
    payment_amount NUMERIC(10,2),
    payer_type VARCHAR(50)
);