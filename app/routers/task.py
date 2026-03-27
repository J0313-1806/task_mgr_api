from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskSwap
from ..crud.task import (
    get_tasks,
    get_task,
    create_task,
    get_tasks_by_status,
    move_task,
    update_task,
    delete_task,
    # swap_task_positions, 
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=201)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


@router.get("/", response_model=List[TaskRead])
def read_all_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return get_tasks(db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
def read_single_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=TaskRead)
def update_existing_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", status_code=200)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}


@router.get("/tasks/filter", response_model=List[TaskRead])
def filter_tasks(status: str, db: Session = Depends(get_db)):
   
    db_task = get_tasks_by_status(db, status)
    if not db_task:
        raise HTTPException(status_code=404, detail=f"No tasks found with status '{status}'")
    return db_task


@router.put("/tasks/{task_id}/move", response_model=TaskRead)
def move_task_route(task_id: int, new_position: int, db: Session = Depends(get_db)):
    """
    Move a task to a new position in the list.
    Adjusts other tasks accordingly.
    """
    return move_task(db, task_id, new_position)

# NEW ENDPOINT: Swap positions of two tasks
# @router.post("/swap-positions", response_model=dict)
# def swap_positions(swap: TaskSwap, db: Session = Depends(get_db)):
#     """Replaces/swaps the position (index) of one task with another task"""
#     return swap_task_positions(db, swap.task_id1, swap.task_id2)