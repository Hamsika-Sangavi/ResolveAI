from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import sqlite3
import uuid
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Load trained model
model = joblib.load(os.path.join(BASE_DIR,'../ml_model/complaint_classifier.pkl'))

# Department mapping
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

# Resolution time mapping (in days)
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

# Initialize FastAPI
app = FastAPI(title="ResolveAI API")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'resolveai.db'))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id TEXT PRIMARY KEY,
            complaint_text TEXT,
            category TEXT,
            department TEXT,
            resolution_time TEXT,
            status TEXT,
            email TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Request models
class ComplaintRequest(BaseModel):
    complaint_text: str
    email: str

class StatusUpdate(BaseModel):
    status: str

# Send email notification
def send_email(to_email: str, subject: str, body: str):
    try:
        sender_email = "your_gmail@gmail.com"
        sender_password = "your_app_password"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Email failed: {e}")

# Routes

@app.get("/")
def home():
    return {"message": "ResolveAI backend is running"}

@app.post("/submit-complaint")
def submit_complaint(request: ComplaintRequest):
    # Predict category
    predicted_category = model.predict([request.complaint_text])[0]
    department = DEPARTMENT_MAP.get(predicted_category, "General Grievance Department")
    resolution_time = RESOLUTION_TIME.get(department, "7-10 days")

    # Generate complaint ID
    complaint_id = str(uuid.uuid4())[:8].upper()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to database
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'resolveai.db'))
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO complaints VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        complaint_id,
        request.complaint_text,
        predicted_category,
        department,
        resolution_time,
        "Submitted",
        request.email,
        created_at,
        created_at
    ))
    conn.commit()
    conn.close()

    # Send email
    send_email(
        request.email,
        f"ResolveAI - Complaint Received | ID: {complaint_id}",
        f"""Dear Citizen,

Your complaint has been successfully submitted to ResolveAI.

Complaint ID: {complaint_id}
Department: {department}
Expected Resolution: {resolution_time}
Status: Submitted

Please save your Complaint ID to track your status.

Team ResolveAI"""
    )

    return {
        "complaint_id": complaint_id,
        "category": predicted_category,
        "department": department,
        "resolution_time": resolution_time,
        "status": "Submitted",
        "message": "Complaint submitted successfully"
    }

@app.get("/complaint-status/{complaint_id}")
def get_status(complaint_id: str):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'resolveai.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM complaints WHERE id = ?', (complaint_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Complaint ID not found"}

    return {
        "complaint_id": row[0],
        "category": row[2],
        "department": row[3],
        "resolution_time": row[4],
        "status": row[5],
        "created_at": row[7]
    }

@app.put("/update-status/{complaint_id}")
def update_status(complaint_id: str, update: StatusUpdate):
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(os.path.join(BASE_DIR, 'resolveai.db'))
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE complaints SET status = ?, updated_at = ? WHERE id = ?
    ''', (update.status, updated_at, complaint_id))
    conn.commit()

    cursor.execute('SELECT * FROM complaints WHERE id = ?', (complaint_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Complaint ID not found"}

    # Notify user by email
    send_email(
        row[6],
        f"ResolveAI - Complaint Update | ID: {complaint_id}",
        f"""Dear Citizen,

Your complaint status has been updated.

Complaint ID: {complaint_id}
Department: {row[3]}
New Status: {update.status}

Team ResolveAI"""
    )

    return {
        "complaint_id": complaint_id,
        "status": update.status,
        "message": "Status updated successfully"
    }

@app.get("/dashboard-stats")
def dashboard_stats():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'resolveai.db'))
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM complaints')
    total = cursor.fetchone()[0]

    cursor.execute('SELECT department, COUNT(*) FROM complaints GROUP BY department')
    by_department = [{"department": row[0], "count": row[1]} for row in cursor.fetchall()]

    cursor.execute('SELECT status, COUNT(*) FROM complaints GROUP BY status')
    by_status = [{"status": row[0], "count": row[1]} for row in cursor.fetchall()]

    cursor.execute('SELECT * FROM complaints ORDER BY created_at DESC LIMIT 10')
    recent = [
        {
            "complaint_id": row[0],
            "department": row[3],
            "status": row[5],
            "created_at": row[7]
        } for row in cursor.fetchall()
    ]

    conn.close()

    return {
        "total_complaints": total,
        "by_department": by_department,
        "by_status": by_status,
        "recent_complaints": recent
    }
