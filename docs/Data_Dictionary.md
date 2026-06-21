# Data Dictionary

## Overview

This document defines the structure, meaning, and intended use of all fields within the Healthcare Revenue Cycle Intelligence Platform.

---

# Table: divisions

| Column | Data Type | Description |
|----------|----------|----------|
| division_id | Integer | Unique division identifier |
| division_name | Text | Clinical specialty/division name |
| avg_wrvu_per_visit | Decimal | Average work RVUs generated per visit |
| avg_collection_per_visit | Decimal | Average collections generated per visit |

---

# Table: providers

| Column | Data Type | Description |
|----------|----------|----------|
| provider_id | Integer | Unique provider identifier |
| provider_name | Text | Provider name |
| division_id | Integer | Associated division |
| provider_type | Text | Physician, APP, Fellow, Resident |
| active_flag | Boolean | Indicates whether provider is active |

---

# Table: encounters

| Column | Data Type | Description |
|----------|----------|----------|
| encounter_id | Integer | Unique encounter identifier |
| mrn | Text | Synthetic Medical Record Number |
| fin | Text | Synthetic Financial Identification Number |
| provider_id | Integer | Provider responsible for encounter |
| division_id | Integer | Division associated with encounter |
| date_of_service | Date | Date encounter occurred |
| encounter_type | Text | Outpatient, Inpatient, Consult |
| payer_type | Text | Medicare, Medicaid, Commercial, Self-Pay |
| encounter_status | Text | Open, Resolved, Closed |

---

# Table: documentation_issues

| Column | Data Type | Description |
|----------|----------|----------|
| issue_id | Integer | Unique documentation issue identifier |
| encounter_id | Integer | Encounter associated with issue |
| issue_type | Text | Category of documentation deficiency |
| issue_reason | Text | Description of issue |
| issue_created_date | Date | Date issue identified |
| issue_resolved_date | Date | Date issue resolved |
| issue_status | Text | Open, Escalated, Resolved |

---

# Table: workflow_status

| Column | Data Type | Description |
|----------|----------|----------|
| workflow_id | Integer | Workflow record identifier |
| encounter_id | Integer | Encounter associated with workflow |
| workflow_status | Text | Operational follow-up stage |
| status_date | Date | Date status was assigned |
| email_count | Integer | Number of provider communications sent |
| last_action | Text | Most recent workflow action |

---

# Table: charges

| Column | Data Type | Description |
|----------|----------|----------|
| charge_id | Integer | Charge record identifier |
| encounter_id | Integer | Associated encounter |
| charge_posted_date | Date | Date charge was posted |
| charge_amount | Decimal | Total charge amount |
| charge_status | Text | Pending, Posted, Denied |

---

# Table: payments

| Column | Data Type | Description |
|----------|----------|----------|
| payment_id | Integer | Payment record identifier |
| encounter_id | Integer | Associated encounter |
| payment_date | Date | Date payment received |
| payment_amount | Decimal | Payment amount received |
| payer_type | Text | Payer responsible for payment |

---

# Business Definitions

## Open Encounter

An encounter with unresolved documentation, coding, or billing activity.

---

## Charge Lag

Number of days between the Date of Service and Charge Posted Date.

Formula:

Charge Lag = Charge Posted Date − Date of Service

---

## Revenue At Risk

Estimated collectible revenue associated with encounters that remain open and unbilled.

---

## Documentation Compliance

Percentage of encounters with no unresolved documentation deficiencies.

---

## Aging Bucket Definitions

| Bucket | Days Open |
|----------|----------|
| Current | 0–30 Days |
| Moderate Risk | 31–60 Days |
| High Risk | 61–90 Days |
| Critical Risk | Greater than 90 Days |

---

## Workflow Status Definitions

| Status | Description |
|----------|----------|
| New | Newly identified issue |
| Email Sent | Initial provider communication sent |
| Reminder 1 | First reminder sent |
| Reminder 2 | Second reminder sent |
| Escalated | Escalated to leadership |
| Sent to Coding | Returned to coding team |
| Resolved | Issue resolved |

---

## Project Data Notes

All data contained within this repository is synthetically generated for educational and portfolio purposes only.

No real patient, provider, payer, or organizational data is included.