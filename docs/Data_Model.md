# Data Model

## Overview

This project uses a relational data model to support healthcare revenue cycle analytics. The model is designed to track encounters, providers, divisions, documentation issues, charges, payments, and workflow status.

---

## Tables

### 1. Divisions

Stores department or specialty-level information.

| Column | Description |
|---|---|
| division_id | Unique division identifier |
| division_name | Name of the clinical division |
| avg_wrvu_per_visit | Average wRVU value per visit |
| avg_collection_per_visit | Average collection amount per visit |

---

### 2. Providers

Stores provider-level information.

| Column | Description |
|---|---|
| provider_id | Unique provider identifier |
| provider_name | Provider name |
| division_id | Division associated with provider |
| provider_type | Physician, APP, Fellow, Resident |
| active_flag | Whether provider is active |

---

### 3. Encounters

Main fact table for patient encounters.

| Column | Description |
|---|---|
| encounter_id | Unique encounter identifier |
| mrn | Synthetic medical record number |
| fin | Synthetic financial identification number |
| provider_id | Provider linked to encounter |
| division_id | Division linked to encounter |
| date_of_service | Encounter date |
| encounter_type | Outpatient, Inpatient, Consult |
| payer_type | Medicare, Medicaid, Commercial, Self-Pay |
| encounter_status | Open, Resolved, Closed |

---

### 4. Documentation Issues

Tracks missing or incomplete documentation.

| Column | Description |
|---|---|
| issue_id | Unique issue identifier |
| encounter_id | Encounter linked to issue |
| issue_type | Missing attestation, missing note, coding clarification, etc. |
| issue_reason | Details of the documentation issue |
| issue_created_date | Date issue was first identified |
| issue_resolved_date | Date issue was resolved |
| issue_status | Open, Resolved, Escalated |

---

### 5. Workflow Status

Tracks operational follow-up activity.

| Column | Description |
|---|---|
| workflow_id | Unique workflow record |
| encounter_id | Encounter linked to workflow |
| workflow_status | New, Email Sent, Reminder 1, Reminder 2, Escalated, Sent to Coding, Resolved |
| status_date | Date workflow status was updated |
| email_count | Number of emails sent |
| last_action | Most recent action taken |

---

### 6. Charges

Tracks charge posting activity.

| Column | Description |
|---|---|
| charge_id | Unique charge identifier |
| encounter_id | Encounter linked to charge |
| charge_posted_date | Date charge was posted |
| charge_amount | Simulated charge amount |
| charge_status | Pending, Posted, Denied |

---

### 7. Payments

Tracks payment activity.

| Column | Description |
|---|---|
| payment_id | Unique payment identifier |
| encounter_id | Encounter linked to payment |
| payment_date | Date payment was received |
| payment_amount | Simulated payment amount |
| payer_type | Medicare, Medicaid, Commercial, Self-Pay |

---

## Key Relationships

- One division has many providers.
- One provider has many encounters.
- One encounter can have one or more documentation issues.
- One encounter can have multiple workflow status updates.
- One encounter can have one charge record.
- One encounter can have one or more payment records.

---

## Analytics Supported

This model supports the following analytics:

- Encounter aging
- Charge lag
- Revenue at risk
- wRVUs at risk
- Documentation compliance
- Provider performance
- Division-level revenue risk
- Workflow escalation tracking