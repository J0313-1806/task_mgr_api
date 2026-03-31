# FastAPI + PostgreSQL Backend

This is the backend service for the Flutter Task Manager App. It provides RESTful APIs for managing tasks, including CRUD operations, search, blocking/unblocking logic, and integration with the Flutter frontend. Built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

---

## 🚀 Setup Instructions

### Prerequisites
- **Python 3.10+**
- **pip** (Python package manager)
- **PostgreSQL** installed and running
- Recommended: **virtualenv** or **conda** for environment management

### Step-by-Step Setup
1. **Clone the repository**
   ```bash
   git clone <your-backend-repo-link>
   cd <backend-folder>
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
4. **Configure database**
   Create a PostgreSQL database (e.g., task_manager_db).
   Update the DATABASE_URL in config.py or .env file:
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/task_manager_db
   ```
   Run migrations (if using Alembic):
   ```bash
   alembic upgrade head
5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```


✨ Features

    CRUD Endpoints
        Create, Read, Update, Delete tasks

    Search
        Filter tasks by title, description, or due date

    Blocking logic
        Tasks can be blocked by other tasks
        Once a blocking task is marked Done, dependent tasks are automatically unblocked

    Integration
        Designed to work seamlessly with the Flutter frontend



🛠️ Tech Stack

    Framework: FastAPI
    ORM: SQLAlchemy
    Database: PostgreSQL
    Validation: Pydantic
    Migrations: Alembic


📱 Usage

    Start the backend server:
    uvicorn main:app --reload
    
    Access API docs at:
        Swagger UI: http://127.0.0.1:8000/docs
        ReDoc: http://127.0.0.1:8000/redoc

    Connect the Flutter frontend by pointing its API base URL to the backend server.

