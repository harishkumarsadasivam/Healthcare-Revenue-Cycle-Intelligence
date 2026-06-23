# Entity Relationship Diagram

## Logical Data Model

DIVISIONS
----------
division_id (PK)
division_name
avg_wrvu_per_visit
avg_collection_per_visit
        |
        | 1-to-Many
        |
PROVIDERS
----------
provider_id (PK)
division_id (FK)
provider_name
provider_type
active_flag
        |
        | 1-to-Many
        |
ENCOUNTERS
----------
encounter_id (PK)
provider_id (FK)
division_id (FK)
mrn
fin
date_of_service
encounter_type
payer_type
encounter_status
      /     |      \
     /      |       \
    /       |        \
DOCUMENTATION_ISSUES  CHARGES  PAYMENTS
-------------------   -------  --------
issue_id (PK)         charge_id (PK)
encounter_id (FK)     encounter_id (FK)
issue_type            charge_amount
issue_status          charge_status

payment_id (PK)
encounter_id (FK)
payment_amount
payment_date

        |
        |
WORKFLOW_STATUS
---------------
workflow_id (PK)
encounter_id (FK)
workflow_status
status_date
email_count
last_action 

## Relationships

- One Division → Many Providers
- One Division → Many Encounters
- One Provider → Many Encounters
- One Encounter → Many Documentation Issues
- One Encounter → Many Workflow Status Records
- One Encounter → One Charge Record
- One Encounter → Zero or More Payment Records