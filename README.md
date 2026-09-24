# StudyApp

> A gamified, collaborative web application designed to help students sync study sessions, build consistent habits, and achieve academic goals together.

---

## Overview

**StudyApp** transforms solitary studying into an engaging, team-oriented experience. By incorporating study streaks, group sessions, and weekly analytics, the platform keeps students accountable and motivated while tracking their academic progress across subjects and projects.

This project serves as a full-stack portfolio showcase built with modern software architecture, robust data validation, and clean code practices.

---

## ✨ Key Features

- **Authentication & Authorization:** Secure user registration, login, and JWT-based session management.
- **Social & Group System:** Add friends, create study groups, and collaborate in real-time.
- **Study Streaks:** Gamified streak tracking to reward daily study consistency.
- **Session Management:** Host individual or group study sessions with customizable session goals.
- **Subject & Project Organization:** Categorize study time by specific courses, topics, or deliverables.
- **Weekly Reports & Analytics:** Visual insights into total hours studied, goal completion rates, and subject distribution.

---

## Tech Stack

### **Backend**

- **Framework:** FastAPI (Python 3.10+)
- **Database ORM:** SQLAlchemy
- **Data Validation & Schemas:** Pydantic
- **Database:** PostgreSQL (Running in Docker)
- **Testing:** Pytest

### **Frontend**

- **Framework:** React.js
- **HTTP Client:** Axios / Fetch API

### **DevOps & Tooling**

- **Environment:** WSL2 (Ubuntu) & Python Virtual Environments (`.venv`)
- **Containerization:** Docker & Docker Compose
- **Version Control:** Git & GitHub (Atomic Commits / Conventional Commits)

---

## 📂 Project Structure

```text
study_app/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes and endpoints
│   │   ├── core/         # Security, JWT, and global configuration
│   │   ├── db/           # Database setup and connection
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic schemas for request/response validation
│   │   ├── services/     # Business logic layer
│   │   └── main.py       # Application entry point
│   ├── tests/            # Automated test suite with Pytest
│   ├── .env.example
│   └── requirements.txt
├── docs/                 # ERD diagrams and API documentation
├── .gitignore
└── README.md
```
