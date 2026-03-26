from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class TaskStatus(str, PyEnum):
    TODO = "To-Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    blocked_by_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
    )
    # NEW: Position for ordering / swapping
    position = Column(Integer, nullable=False, index=True)