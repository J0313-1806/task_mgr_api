from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..database import get_db
from ..schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskOrderRequest
from ..crud.task import (
    get_tasks,
    get_task,
    create_task,
    get_tasks_by_status,
    move_task,
    update_task,
    delete_task,
    bulk_delete_tasks,
    search_tasks,
    reorder_tasks_in_db,
    # swap_task_positions, 
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/add", response_model=TaskRead, status_code=201)
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


@router.delete("/bulk", status_code=200)
def delete_multiple_tasks(task_ids: List[int], db: Session = Depends(get_db)):
   
    result = bulk_delete_tasks(db, task_ids)
    if result["count"] == 0:
        raise HTTPException(status_code=404, detail="No tasks found for given IDs")
    return {"message": f"{result["count"]} Tasks deleted successfully"}


@router.delete("/delete/{task_id}", status_code=200)
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


@router.put("/tasks/reorder")
def reorder_tasks(order_request: TaskOrderRequest, db: Session = Depends(get_db)):
    return reorder_tasks_in_db(db, order_request)


@router.put("/tasks/move/{task_id}", response_model=TaskRead)
def move_task_route(task_id: int, new_position: int, db: Session = Depends(get_db)):
    
    return move_task(db, task_id, new_position)


@router.get("/tasks/search", response_model=List[TaskRead])
def search_tasks_endpoint(
    task_id: Optional[int] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    position: Optional[int] = None,
    due_date: Optional[date] = None,
    status: Optional[str] = None,
    blocked_by_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return search_tasks(
        db,
        task_id=task_id,
        title=title,
        description=description,
        position=position,
        due_date=due_date,
        status=status,
        blocked_by_id=blocked_by_id,
    )


# NEW ENDPOINT: Swap positions of two tasks
# @router.post("/swap-positions", response_model=dict)
# def swap_positions(swap: TaskSwap, db: Session = Depends(get_db)):
#     """Replaces/swaps the position (index) of one task with another task"""
#     return swap_task_positions(db, swap.task_id1, swap.task_id2)