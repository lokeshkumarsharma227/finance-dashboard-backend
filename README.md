# Finance Dashboard Backend

A RESTful backend API for a finance dashboard system built with FastAPI.
Different users interact with financial records based on their role.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (via SQLAlchemy ORM)
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic v2
- **Password Hashing**: bcrypt (via passlib)
- **Language**: Python 3.10+

## Project Structure
```
finance_dashboard/
├── app/
│   ├── api/v1/              # Route handlers (HTTP layer)
│   │   ├── auth.py          # Login, Register
│   │   ├── users.py         # User management
│   │   ├── finance.py       # Financial records CRUD
│   │   └── dashboard.py     # Summary analytics
│   ├── core/                # App configuration
│   │   ├── config.py        # Environment settings
│   │   ├── security.py      # JWT + password hashing
│   │   └── exceptions.py    # Custom HTTP exceptions
│   ├── db/
│   │   └── session.py       # Database connection
│   ├── models/              # SQLAlchemy ORM tables
│   │   ├── user.py          # Users table
│   │   └── finance.py       # Finance records table
│   ├── schemas/             # Pydantic data contracts
│   │   ├── user.py          # User schemas
│   │   ├── finance.py       # Finance schemas
│   │   └── dashboard.py     # Dashboard schemas
│   ├── repositories/        # Database query layer
│   │   ├── base.py          # Generic CRUD
│   │   ├── user_repository.py
│   │   └── finance_repository.py
│   ├── services/            # Business logic layer
│   │   ├── user_service.py
│   │   ├── finance_service.py
│   │   └── dashboard_service.py
│   └── permissions/         # Access control layer
│       ├── roles.py         # Permission matrix
│       ├── base.py          # Permission checker
│       └── guards.py        # FastAPI dependencies
├── main.py                  # App entry point
├── requirements.txt
└── .env
```

## Architecture

This project follows a strict layered architecture:
```
HTTP Request
     ↓
Routes (api/)          → thin HTTP handlers only
     ↓
Permissions (guards)   → JWT auth + role checks
     ↓
Services               → business logic
     ↓
Repositories           → database queries
     ↓
Models                 → database tables
     ↓
Database (SQLite)
```

## Design Patterns Used

- **Repository Pattern** — all database queries centralized
- **Service Layer Pattern** — business logic separated from routes
- **Dependency Injection** — FastAPI's built-in DI system
- **Strategy Pattern** — permission checking via PermissionChecker class
- **Generic Base Repository** — reusable CRUD via TypeVar and Generic

## SOLID Principles Applied

- **S** — Each class has one responsibility (routes handle HTTP, services handle logic, repositories handle DB)
- **O** — Adding new roles doesn't require modifying existing permission code
- **L** — UserRepository and FinanceRepository are substitutable with BaseRepository
- **I** — Schemas are segregated by use case (UserCreate vs UserResponse)
- **D** — Services depend on repository abstractions injected via constructor

## Setup and Installation

### Prerequisites
- Python 3.10+
- pip

### Steps

1. Clone the repository
```bash
git clone https://github.com/lokeshkumarsharma227/finance-dashboard-backend.git
cd finance-dashboard-backend
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file in project root
```env
APP_NAME=Finance Dashboard
DEBUG=True
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./finance.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

5. Run the server
```bash
uvicorn main:app --reload
```

6. Open API documentation
```
http://localhost:8000/docs
```

## API Endpoints

### Authentication
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/v1/auth/register` | Register new user | Public |
| POST | `/api/v1/auth/login` | Login and get JWT token | Public |

### Users
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/v1/users/me` | Get own profile | Any logged in user |
| GET | `/api/v1/users/` | Get all users | Admin only |
| GET | `/api/v1/users/{id}` | Get user by id | Admin only |
| PATCH | `/api/v1/users/{id}` | Update user | Admin only |
| DELETE | `/api/v1/users/{id}` | Delete user | Admin only |

### Finance Records
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/v1/records/` | Create record | Analyst, Admin |
| GET | `/api/v1/records/` | Get own records | Any logged in user |
| GET | `/api/v1/records/filter` | Filter records | Any logged in user |
| GET | `/api/v1/records/{id}` | Get single record | Any logged in user |
| PATCH | `/api/v1/records/{id}` | Update record | Analyst, Admin |
| DELETE | `/api/v1/records/{id}` | Delete record | Admin only |

### Dashboard
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/v1/dashboard/summary` | Get summary analytics | Analyst, Admin |

## Role Permissions

| Action | Viewer | Analyst | Admin |
|--------|--------|---------|-------|
| Read records | ✅ | ✅ | ✅ |
| Read dashboard | ✅ | ✅ | ✅ |
| Create records | ❌ | ✅ | ✅ |
| Update records | ❌ | ✅ | ✅ |
| Delete records | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

## Authentication Flow
```
1. Register → POST /api/v1/auth/register
2. Login    → POST /api/v1/auth/login → receive JWT token
3. Use token in header → Authorization: Bearer <token>
4. Token expires in 30 minutes
```

## Dashboard Summary Response
```json
{
    "total_income": 50000.0,
    "total_expenses": 20000.0,
    "net_balance": 30000.0,
    "total_records": 3,
    "category_totals": [
        {"category": "salary", "total": 50000.0},
        {"category": "rent", "total": 15000.0},
        {"category": "food", "total": 5000.0}
    ]
}
```

## Assumptions Made

1. SQLite used for simplicity — switchable to PostgreSQL by changing `DATABASE_URL`
2. Analyst can create and update records but cannot delete — only Admin can delete
3. Users can only see and modify their own financial records
4. JWT tokens expire in 30 minutes — no refresh token in this version
5. Passwords must be provided at registration — no password reset flow
6. All amounts stored as Float — currency assumed to be single denomination

## Tradeoffs Considered

| Decision | Chose | Reason |
|----------|-------|--------|
| Database | SQLite | Zero config for local dev — PostgreSQL ready |
| Auth | JWT stateless | No session storage needed |
| Roles | Enum + matrix | Simple, readable, extensible |
| Handlers | Synchronous | Simpler code — FastAPI supports async upgrade |
| Soft delete | Not implemented | Out of scope — easy to add with `is_deleted` flag |

## What I Would Add With More Time

- Unit tests for services
- Integration tests for routes
- Refresh token mechanism
- Soft delete for records
- Pagination metadata in responses
- Rate limiting
- Switch to PostgreSQL
- Docker setup

## Data Models

### User
```
id, full_name, email, hashed_password,
role (viewer/analyst/admin), is_active,
created_at, updated_at
```

### FinanceRecord
```
id, amount, transaction_type (income/expense),
category, date, description, user_id,
created_at, updated_at
```