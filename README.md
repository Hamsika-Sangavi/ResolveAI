# ResolveAI 🏛️
### AI-Powered Civic Complaint Management System

ResolveAI is a full stack web application that uses Natural Language Processing to automatically classify citizen complaints, route them to the correct government department, predict resolution time, and track status in real time.

---

## 🚀 Live Demo
> Frontend: https://resolveai-frontend.vercel.app
> Backend API: https://resolveai-hrol.onrender.com/docs

---

## 🧠 What It Does

A citizen types their complaint in plain English. ResolveAI:
1. Reads the complaint using an NLP model
2. Classifies it into the correct category
3. Routes it to the right department automatically
4. Predicts how long it will take to resolve
5. Generates a unique complaint ID
6. Sends email notification to the citizen
7. Lets admin update status in real time

---

## 🖥️ Pages

- **Submit Complaint** — citizen submits complaint, gets instant AI classification and complaint ID
- **Track Complaint** — citizen tracks status using complaint ID
- **Admin Dashboard** — admin views all complaints, department stats, and updates status

---

## 📊 ML Model

- Dataset: Consumer Financial Protection Bureau (CFPB) complaints dataset
- Training samples: 380,000+
- Algorithm: Logistic Regression with TF-IDF vectorization
- Accuracy: 74% across 17 complaint categories
- Library: scikit-learn

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Tailwind CSS, Axios |
| Backend | FastAPI, Python |
| ML Model | scikit-learn, TF-IDF, Logistic Regression |
| Database | SQLite |
| Email Alerts | Gmail SMTP |
| Deployment | Render + Vercel |

---

## 📁 Project Structure
ResolveAI/
├── backend/
│   └── main.py          # FastAPI server
├── ml_model/
│   ├── train_model.py   # Model training script
│   ├── add_dummy_data.py
│   └── complaint_classifier.pkl
├── frontend/
│   └── resolveai-frontend/
│       └── src/
│           ├── App.js
│           └── App.css
└── data/                # Dataset (not pushed to GitHub)
---

## ⚙️ Run Locally

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend/resolveai-frontend
npm install
npm start
```

---

## 👨‍💻 Author
Hamsika Sangavi — B.Tech 3rd year Computer Science (Data Science), Anurag University