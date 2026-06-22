-- Healthcare Revenue Cycle Intelligence Platform
-- Analytics Views

DROP VIEW IF EXISTS vw_encounter_aging;
DROP VIEW IF EXISTS vw_revenue_at_risk;
DROP VIEW IF EXISTS vw_charge_lag;
DROP VIEW IF EXISTS vw_provider_performance;
DROP VIEW IF EXISTS vw_division_performance;

-- 1. Encounter Aging View

CREATE VIEW vw_encounter_aging AS
SELECT
    e.encounter_id,
    e.mrn,
    e.fin,
    p.provider_name,
    d.division_name,
    e.date_of_service,
    e.encounter_type,
    e.payer_type,
    e.encounter_status,
    CURRENT_DATE - e.date_of_service AS days_open,
    CASE
        WHEN CURRENT_DATE - e.date_of_service BETWEEN 0 AND 30 THEN 'Current'
        WHEN CURRENT_DATE - e.date_of_service BETWEEN 31 AND 60 THEN 'Moderate Risk'
        WHEN CURRENT_DATE - e.date_of_service BETWEEN 61 AND 90 THEN 'High Risk'
        ELSE 'Critical Risk'
    END AS aging_bucket
FROM encounters e
LEFT JOIN providers p
    ON e.provider_id = p.provider_id
LEFT JOIN divisions d
    ON e.division_id = d.division_id;

-- 2. Revenue At Risk View

CREATE VIEW vw_revenue_at_risk AS
SELECT
    e.encounter_id,
    p.provider_name,
    d.division_name,
    e.date_of_service,
    e.encounter_status,
    c.charge_status,
    d.avg_wrvu_per_visit,
    d.avg_collection_per_visit,
    CASE
        WHEN e.encounter_status = 'Open'
             OR c.charge_status = 'Pending'
        THEN d.avg_collection_per_visit
        ELSE 0
    END AS estimated_collection_at_risk,
    CASE
        WHEN e.encounter_status = 'Open'
             OR c.charge_status = 'Pending'
        THEN d.avg_wrvu_per_visit
        ELSE 0
    END AS estimated_wrvu_at_risk
FROM encounters e
LEFT JOIN providers p
    ON e.provider_id = p.provider_id
LEFT JOIN divisions d
    ON e.division_id = d.division_id
LEFT JOIN charges c
    ON e.encounter_id = c.encounter_id;

-- 3. Charge Lag View

CREATE VIEW vw_charge_lag AS
SELECT
    e.encounter_id,
    p.provider_name,
    d.division_name,
    e.date_of_service,
    c.charge_posted_date,
    c.charge_status,
    CASE
        WHEN c.charge_posted_date IS NOT NULL
        THEN c.charge_posted_date - e.date_of_service
        ELSE NULL
    END AS charge_lag_days
FROM encounters e
LEFT JOIN providers p
    ON e.provider_id = p.provider_id
LEFT JOIN divisions d
    ON e.division_id = d.division_id
LEFT JOIN charges c
    ON e.encounter_id = c.encounter_id;

-- 4. Provider Performance View

CREATE VIEW vw_provider_performance AS
SELECT
    p.provider_id,
    p.provider_name,
    d.division_name,
    COUNT(DISTINCT e.encounter_id) AS total_encounters,
    COUNT(DISTINCT CASE WHEN e.encounter_status = 'Open' THEN e.encounter_id END) AS open_encounters,
    COUNT(DISTINCT CASE WHEN e.encounter_status = 'Resolved' THEN e.encounter_id END) AS resolved_encounters,
    COUNT(DISTINCT di.issue_id) AS documentation_issues,
    ROUND(
        COUNT(DISTINCT CASE WHEN e.encounter_status = 'Resolved' THEN e.encounter_id END)::NUMERIC
        / NULLIF(COUNT(DISTINCT e.encounter_id), 0) * 100,
        2
    ) AS resolution_rate_percent,
    ROUND(
        COUNT(DISTINCT di.issue_id)::NUMERIC
        / NULLIF(COUNT(DISTINCT e.encounter_id), 0) * 100,
        2
    ) AS documentation_issue_rate_percent
FROM providers p
LEFT JOIN divisions d
    ON p.division_id = d.division_id
LEFT JOIN encounters e
    ON p.provider_id = e.provider_id
LEFT JOIN documentation_issues di
    ON e.encounter_id = di.encounter_id
GROUP BY
    p.provider_id,
    p.provider_name,
    d.division_name;

-- 5. Division Performance View

CREATE VIEW vw_division_performance AS
SELECT
    d.division_id,
    d.division_name,
    COUNT(DISTINCT e.encounter_id) AS total_encounters,
    COUNT(DISTINCT CASE WHEN e.encounter_status = 'Open' THEN e.encounter_id END) AS open_encounters,
    COUNT(DISTINCT CASE WHEN e.encounter_status = 'Resolved' THEN e.encounter_id END) AS resolved_encounters,
    COUNT(DISTINCT di.issue_id) AS documentation_issues,
    SUM(
        CASE
            WHEN e.encounter_status = 'Open'
                 OR c.charge_status = 'Pending'
            THEN d.avg_collection_per_visit
            ELSE 0
        END
    ) AS total_collection_at_risk,
    SUM(
        CASE
            WHEN e.encounter_status = 'Open'
                 OR c.charge_status = 'Pending'
            THEN d.avg_wrvu_per_visit
            ELSE 0
        END
    ) AS total_wrvu_at_risk,
    ROUND(
        AVG(
            CASE
                WHEN c.charge_posted_date IS NOT NULL
                THEN c.charge_posted_date - e.date_of_service
                ELSE NULL
            END
        ),
        2
    ) AS avg_charge_lag_days
FROM divisions d
LEFT JOIN encounters e
    ON d.division_id = e.division_id
LEFT JOIN documentation_issues di
    ON e.encounter_id = di.encounter_id
LEFT JOIN charges c
    ON e.encounter_id = c.encounter_id
GROUP BY
    d.division_id,
    d.division_name;