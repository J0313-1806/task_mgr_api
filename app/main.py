from fastapi import FastAPI
from .database import engine, Base
from .routers.task import router as task_router

# Create tables on startup (development only - use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="Full CRUD backend for tasks with PostgreSQL.",
    version="1.0.0",
)

app.include_router(task_router)


@app.get("/")
def root():
    return {
        "message": "Task Management API is running! 🚀",
        "docs": "/docs",
        "tasks_endpoint": "/tasks",
    }