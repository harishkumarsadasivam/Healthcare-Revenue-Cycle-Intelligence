# Healthcare Revenue Cycle Intelligence Platform

## Overview

The Healthcare Revenue Cycle Intelligence Platform is an end-to-end healthcare analytics project designed to identify revenue cycle risks associated with documentation delays, charge lag, coding workflows, and unresolved encounters.

The platform simulates a healthcare organization's revenue cycle operations and demonstrates the complete analytics lifecycle from data generation and ETL processing to database analytics and executive reporting.

---

## Business Problem

Healthcare organizations frequently experience revenue leakage due to:

- Missing provider documentation
- Delayed attestations
- Coding clarification requests
- Charge posting delays
- Workflow bottlenecks
- Aging encounters approaching timely filing limits

This project provides a framework for monitoring these risks and generating actionable operational insights.

---

## Technology Stack

### Data Engineering

- Python
- PostgreSQL
- SQLAlchemy

### Analytics

- PostgreSQL
- SQL Views
- KPI Layer

### Reporting

- Power BI

### Development

- Git
- GitHub
- VS Code

---

## Architecture

Synthetic Data Generator
        ↓
CSV Data Files
        ↓
Python ETL Pipeline
        ↓
PostgreSQL Database
        ↓
Analytics Views
        ↓
KPI Layer
        ↓
Power BI Dashboard

---

## Project Components

### Synthetic Data Generation

Generates realistic healthcare revenue cycle data including:

- Divisions
- Providers
- Encounters
- Documentation Issues
- Workflow Activity
- Charges
- Payments

---

### Automated ETL Pipeline

Automated workflow:

Generate Data
      ↓
Load PostgreSQL
      ↓
Validate Data
      ↓
Analytics Ready

Run the full pipeline:

python3 python/run_pipeline.py 

---

## Database Schema

Core tables:

| Table | Description |
|---------|---------|
| divisions | Clinical specialty information |
| providers | Provider information |
| encounters | Encounter-level fact table |
| documentation_issues | Documentation deficiencies |
| workflow_status | Operational workflow tracking |
| charges | Charge posting activity |
| payments | Payment activity |

---

## Analytics Views

| View | Purpose |
|---------|---------|
| vw_encounter_aging | Aging bucket calculations |
| vw_revenue_at_risk | Revenue and wRVU risk estimates |
| vw_charge_lag | Charge lag calculations |
| vw_provider_performance | Provider metrics |
| vw_division_performance | Division metrics |

---

## Dataset Statistics

Current synthetic dataset:

| Metric | Volume |
|---------|---------|
| Divisions | 8 |
| Providers | 75 |
| Encounters | 10,000 |
| Documentation Issues | 5,503 |
| Workflow Records | 18,040 |
| Charges | 10,000 |
| Payments | 5,882 |

---

## Key Performance Indicators

### Operational

- Current Open Encounters
- Resolved Encounters
- Documentation Compliance
- Workflow Status Distribution

### Financial

- Revenue At Risk
- Collection At Risk
- wRVUs At Risk
- Charge Lag

### Provider Performance

- Resolution Rate
- Documentation Issue Rate
- Open Encounters by Provider

---

## Repository Structure

Healthcare-Revenue-Cycle-Intelligence/

├── data/
├── docs/
├── images/
├── notebooks/
├── powerbi/
├── python/
├── sql/
├── README.md
├── LICENSE
└── requirements.txt

---

## Future Enhancements

- Power BI Executive Dashboard
- Predictive Modeling
- Revenue Forecasting
- Automated Email Reporting
- Encounter Escalation Engine
- Healthcare KPI Monitoring

---

## Disclaimer

All data used in this project is synthetically generated and intended solely for educational and portfolio purposes.

No real patient, provider, payer, or organizational information is included.
