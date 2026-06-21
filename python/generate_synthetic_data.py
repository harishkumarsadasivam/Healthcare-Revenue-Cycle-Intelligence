import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
from pathlib import Path

fake = Faker()
random.seed(42)
np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

NUM_PROVIDERS = 75
NUM_ENCOUNTERS = 10000

divisions = pd.DataFrame([
    [1, "Hospital Medicine", 2.75, 145.00],
    [2, "Cardiology", 3.50, 220.00],
    [3, "Pulmonary", 3.10, 185.00],
    [4, "Gastroenterology", 4.25, 275.00],
    [5, "Infectious Disease", 2.90, 165.00],
    [6, "Nephrology", 3.20, 195.00],
    [7, "Rheumatology", 2.60, 150.00],
    [8, "Endocrinology", 2.45, 140.00],
], columns=["division_id", "division_name", "avg_wrvu_per_visit", "avg_collection_per_visit"])

provider_types = ["Physician", "APP", "Fellow", "Resident"]
providers = []

for provider_id in range(1, NUM_PROVIDERS + 1):
    division_id = random.choice(divisions["division_id"].tolist())
    providers.append([
        provider_id,
        f"Dr {fake.last_name()}" if random.random() < 0.75 else fake.name(),
        division_id,
        random.choices(provider_types, weights=[65, 20, 10, 5])[0],
        True
    ])

providers = pd.DataFrame(providers, columns=[
    "provider_id", "provider_name", "division_id", "provider_type", "active_flag"
])

encounter_types = ["Outpatient", "Inpatient", "Consult"]
payer_types = ["Medicare", "Medicaid", "Commercial", "Self-Pay"]
encounter_statuses = ["Open", "Resolved", "Closed"]

start_date = datetime(2025, 7, 1)
end_date = datetime(2026, 6, 21)
date_range_days = (end_date - start_date).days

encounters = []

for encounter_id in range(1, NUM_ENCOUNTERS + 1):
    provider = providers.sample(1).iloc[0]
    dos = start_date + timedelta(days=random.randint(0, date_range_days))

    status = random.choices(
        encounter_statuses,
        weights=[32, 58, 10]
    )[0]

    encounters.append([
        encounter_id,
        f"MRN{100000 + encounter_id}",
        f"FIN{200000 + encounter_id}",
        provider["provider_id"],
        provider["division_id"],
        dos.date(),
        random.choices(encounter_types, weights=[65, 25, 10])[0],
        random.choices(payer_types, weights=[38, 22, 35, 5])[0],
        status
    ])

encounters = pd.DataFrame(encounters, columns=[
    "encounter_id", "mrn", "fin", "provider_id", "division_id",
    "date_of_service", "encounter_type", "payer_type", "encounter_status"
])

issue_types = [
    "Missing Attestation",
    "Missing Documentation",
    "Incomplete Note",
    "Coding Clarification",
    "Missing Supervision Statement",
    "Unsigned Encounter",
    "Missing Level of Service",
    "Incomplete Procedure Documentation"
]

documentation_issues = []
issue_id = 1

for _, row in encounters.iterrows():
    if random.random() < 0.55:
        issue_created_date = row["date_of_service"] + timedelta(days=random.randint(1, 14))

        if row["encounter_status"] in ["Resolved", "Closed"]:
            issue_resolved_date = issue_created_date + timedelta(days=random.randint(3, 45))
            issue_status = "Resolved"
        else:
            issue_resolved_date = None
            issue_status = random.choices(
                ["Open", "Escalated"],
                weights=[75, 25]
            )[0]

        documentation_issues.append([
            issue_id,
            row["encounter_id"],
            random.choice(issue_types),
            fake.sentence(nb_words=8),
            issue_created_date,
            issue_resolved_date,
            issue_status
        ])
        issue_id += 1

documentation_issues = pd.DataFrame(documentation_issues, columns=[
    "issue_id", "encounter_id", "issue_type", "issue_reason",
    "issue_created_date", "issue_resolved_date", "issue_status"
])

workflow_options = [
    "New",
    "Email Sent",
    "Reminder 1",
    "Reminder 2",
    "Escalated",
    "Sent to Coding",
    "Resolved"
]

workflow_status = []
workflow_id = 1

for _, row in documentation_issues.iterrows():
    num_steps = random.randint(1, 4)
    selected_steps = workflow_options[:num_steps]

    if row["issue_status"] == "Resolved":
        selected_steps.append("Resolved")
    elif row["issue_status"] == "Escalated":
        selected_steps.append("Escalated")

    selected_steps = list(dict.fromkeys(selected_steps))

    base_date = row["issue_created_date"]

    for i, step in enumerate(selected_steps):
        workflow_status.append([
            workflow_id,
            row["encounter_id"],
            step,
            base_date + timedelta(days=i * random.randint(2, 7)),
            i if step != "New" else 0,
            step
        ])
        workflow_id += 1

workflow_status = pd.DataFrame(workflow_status, columns=[
    "workflow_id", "encounter_id", "workflow_status",
    "status_date", "email_count", "last_action"
])

charges = []

for _, row in encounters.iterrows():
    division = divisions[divisions["division_id"] == row["division_id"]].iloc[0]

    if row["encounter_status"] in ["Resolved", "Closed"]:
        charge_posted_date = row["date_of_service"] + timedelta(days=random.randint(3, 35))
        charge_status = random.choices(
            ["Posted", "Denied"],
            weights=[92, 8]
        )[0]
    else:
        if random.random() < 0.35:
            charge_posted_date = row["date_of_service"] + timedelta(days=random.randint(7, 75))
            charge_status = "Posted"
        else:
            charge_posted_date = None
            charge_status = "Pending"

    charge_amount = round(
        float(division["avg_collection_per_visit"]) * random.uniform(1.8, 3.2),
        2
    )

    charges.append([
        row["encounter_id"],
        row["encounter_id"],
        charge_posted_date,
        charge_amount,
        charge_status
    ])

charges = pd.DataFrame(charges, columns=[
    "charge_id", "encounter_id", "charge_posted_date", "charge_amount", "charge_status"
])

payments = []
payment_id = 1

posted_charges = charges[charges["charge_status"] == "Posted"]

for _, charge in posted_charges.iterrows():
    if random.random() < 0.78:
        encounter = encounters[encounters["encounter_id"] == charge["encounter_id"]].iloc[0]

        payment_date = charge["charge_posted_date"] + timedelta(days=random.randint(10, 65))
        payment_amount = round(
            float(charge["charge_amount"]) * random.uniform(0.45, 0.85),
            2
        )

        payments.append([
            payment_id,
            charge["encounter_id"],
            payment_date,
            payment_amount,
            encounter["payer_type"]
        ])
        payment_id += 1

payments = pd.DataFrame(payments, columns=[
    "payment_id", "encounter_id", "payment_date", "payment_amount", "payer_type"
])

divisions.to_csv(DATA_DIR / "divisions.csv", index=False)
providers.to_csv(DATA_DIR / "providers.csv", index=False)
encounters.to_csv(DATA_DIR / "encounters.csv", index=False)
documentation_issues.to_csv(DATA_DIR / "documentation_issues.csv", index=False)
workflow_status.to_csv(DATA_DIR / "workflow_status.csv", index=False)
charges.to_csv(DATA_DIR / "charges.csv", index=False)
payments.to_csv(DATA_DIR / "payments.csv", index=False)

print("Synthetic healthcare revenue cycle data generated successfully.")
print(f"Divisions: {len(divisions)}")
print(f"Providers: {len(providers)}")
print(f"Encounters: {len(encounters)}")
print(f"Documentation Issues: {len(documentation_issues)}")
print(f"Workflow Status Records: {len(workflow_status)}")
print(f"Charges: {len(charges)}")
print(f"Payments: {len(payments)}")