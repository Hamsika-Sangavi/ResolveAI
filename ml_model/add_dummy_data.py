import sqlite3
import uuid
from datetime import datetime, timedelta
import random

complaints = [
    ("My mortgage payment was debited twice this month without any explanation from the bank.", "mortgage@gmail.com"),
    ("I have been receiving constant calls from a debt collection agency for a debt I already paid.", "debt@gmail.com"),
    ("My credit report shows a late payment that I never made. I need this removed immediately.", "credit@gmail.com"),
    ("The student loan interest rate was changed without any prior notice or communication.", "student@gmail.com"),
    ("My credit card was charged for a subscription I never signed up for.", "card@gmail.com"),
    ("Bank transferred my money to a wrong account and is refusing to reverse the transaction.", "bank@gmail.com"),
    ("I have been trying to close my savings account for 3 months but the bank keeps delaying.", "savings@gmail.com"),
    ("My personal loan EMI was deducted twice in the same month.", "loan@gmail.com"),
    ("Vehicle loan foreclosure charges are much higher than what was mentioned in the agreement.", "vehicle@gmail.com"),
    ("Money transfer to my family was deducted but never received on the other end.", "transfer@gmail.com"),
    ("Prepaid card balance disappeared overnight without any transactions.", "prepaid@gmail.com"),
    ("Payday loan company is charging illegal interest rates beyond the legal limit.", "payday@gmail.com"),
    ("My home loan application was rejected without any valid reason given.", "homeloan@gmail.com"),
    ("Credit card annual fee was charged without prior intimation as promised.", "annualfee@gmail.com"),
    ("Debt collector is threatening me with legal action for a debt that is 10 years old.", "olddebt@gmail.com"),
    ("Student loan repayment plan was changed without my consent.", "repayment@gmail.com"),
    ("Bank account was frozen without any notice or explanation.", "frozen@gmail.com"),
    ("Credit score dropped 100 points due to a bank reporting error.", "score@gmail.com"),
    ("My car loan payment was processed but not reflected in the account.", "carloan@gmail.com"),
    ("Virtual currency transaction was reversed without explanation.", "crypto@gmail.com"),
    ("Mortgage company is refusing to provide loan modification options.", "modify@gmail.com"),
    ("Collection agency contacted my employer about my personal debt illegally.", "employer@gmail.com"),
    ("Credit card limit was reduced without any prior notice.", "limit@gmail.com"),
    ("Student loan servicer lost my payment records completely.", "records@gmail.com"),
    ("Bank is charging hidden fees on every international transaction.", "fees@gmail.com"),
]

DEPARTMENT_MAP = {
    "Mortgage": "Housing & Loans Department",
    "Debt collection": "Financial Grievance Cell",
    "Credit reporting": "Credit Regulatory Wing",
    "Credit reporting, credit repair services, or other personal consumer reports": "Credit Regulatory Wing",
    "Student loan": "Education Finance Wing",
    "Credit card or prepaid card": "Digital Payments Department",
    "Credit card": "Digital Payments Department",
    "Bank account or service": "Banking Services Department",
    "Checking or savings account": "Banking Services Department",
    "Consumer Loan": "Consumer Finance Department",
    "Vehicle loan or lease": "Vehicle Finance Department",
    "Money transfer, virtual currency, or money service": "Digital Payments Department",
    "Payday loan, title loan, or personal loan": "Consumer Finance Department",
    "Payday loan": "Consumer Finance Department",
    "Money transfers": "Digital Payments Department",
    "Prepaid card": "Digital Payments Department",
    "Other financial service": "General Grievance Department",
    "Virtual currency": "Digital Payments Department"
}

RESOLUTION_TIME = {
    "Housing & Loans Department": "15-20 days",
    "Financial Grievance Cell": "7-10 days",
    "Credit Regulatory Wing": "10-15 days",
    "Education Finance Wing": "10-12 days",
    "Digital Payments Department": "3-5 days",
    "Banking Services Department": "5-7 days",
    "Consumer Finance Department": "7-10 days",
    "Vehicle Finance Department": "7-10 days",
    "General Grievance Department": "10-15 days"
}

STATUSES = ["Submitted", "In Progress", "Under Review", "Resolved", "Resolved", "Resolved"]

import joblib
model = joblib.load('complaint_classifier.pkl')

conn = sqlite3.connect('../backend/resolveai.db')
cursor = conn.cursor()

for complaint_text, email in complaints:
    complaint_id = str(uuid.uuid4())[:8].upper()
    predicted_category = model.predict([complaint_text])[0]
    department = DEPARTMENT_MAP.get(predicted_category, "General Grievance Department")
    resolution_time = RESOLUTION_TIME.get(department, "7-10 days")
    status = random.choice(STATUSES)
    days_ago = random.randint(1, 30)
    created_at = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT OR IGNORE INTO complaints VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        complaint_id,
        complaint_text,
        predicted_category,
        department,
        resolution_time,
        status,
        email,
        created_at,
        created_at
    ))

conn.commit()
conn.close()
print("25 dummy complaints added successfully!")