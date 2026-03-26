from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.task import Task, TaskStatus
from ..schemas.task import TaskCreate, TaskUpdate, TaskSwap
from fastapi import HTTPException


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    # NEW: Always return tasks sorted by position
    return (
        db.query(Task)
        .order_by(Task.position.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task_in: TaskCreate):
    # Validation: blocked_by must exist
    if task_in.blocked_by_id:
        blocker = get_task(db, task_in.blocked_by_id)
        if not blocker:
            raise HTTPException(status_code=400, detail="Blocking task does not exist")

    # NEW: Auto-assign next position if not provided
    if task_in.position is None:
        max_pos = db.query(func.max(Task.position)).scalar() or 0
        position = max_pos + 1
    else:
        position = task_in.position

    db_task = Task(
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        status=task_in.status,
        blocked_by_id=task_in.blocked_by_id,
        position=position,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_in: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    update_data = task_in.model_dump(exclude_unset=True)

    if "blocked_by_id" in update_data:
        new_blocked_id = update_data["blocked_by_id"]
        if new_blocked_id == task_id:
            raise HTTPException(status_code=400, detail="A task cannot block itself")
        if new_blocked_id is not None:
            blocker = get_task(db, new_blocked_id)
            if not blocker:
                raise HTTPException(status_code=400, detail="Blocking task does not exist")

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    # db_task = get_task(db, task_id)
    # if db_task:
    #     db.delete(db_task)
    #     db.commit()
    # return db_task
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_position = db_task.position

    # Delete the task
    db.delete(db_task)
    db.commit()
    
    db.query(Task).filter(Task.position > old_position).update(
        {Task.position: Task.position - 1},
        synchronize_session=False
    )
    db.commit()
    return db_task


def move_task(db: Session, task_id: int, new_position: int):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_position = task.position

    if new_position < old_position: # type: ignore
        # Shift tasks down between new_position and old_position-1
        db.query(Task).filter(
            Task.position >= new_position,
            Task.position < old_position
        ).update({Task.position: Task.position + 1}, synchronize_session=False)
    elif new_position > old_position: # type: ignore
        # Shift tasks up between old_position+1 and new_position
        db.query(Task).filter(
            Task.position <= new_position,
            Task.position > old_position
        ).update({Task.position: Task.position - 1}, synchronize_session=False)

    task.position = new_position # type: ignore
    db.commit()
    db.refresh(task)
    return task


# NEW: Swap positions of two tasks
# def swap_task_positions(db: Session, task1_id: int, task2_id: int):
#     task1 = get_task(db, task1_id)
#     task2 = get_task(db, task2_id)

#     if not task1 or not task2:
#         raise HTTPException(status_code=404, detail="One or both tasks not found")
#     if task1.id == task2.id: # type: ignore
#         raise HTTPException(status_code=400, detail="Cannot swap a task with itself")

#     # Atomic swap
#     task1.position, task2.position = task2.position, task1.position

#     db.commit()
#     db.refresh(task1)
#     db.refresh(task2)

#     return {
#         "message": "Positions swapped successfully",
#         "task1": {"id": task1.id, "position": task1.position},
#         "task2": {"id": task2.id, "position": task2.position},
#     }