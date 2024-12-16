from sqlalchemy.orm import Session
from models import Task

def add_task(db: Session, title: str, description: str):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()

def list_tasks(db: Session):
    return db.query(Task).all()

def mark_completed(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = True
        db.commit()

def delete_task_by_id(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False

def export_tasks_to_json(db: Session, file_path: str):
    tasks = db.query(Task).all()
    tasks_data = [{"id": t.id, "title": t.title, "description": t.description, "completed": t.completed} for t in tasks]
    with open(file_path, "w") as file:
        import json
        json.dump(tasks_data, file, indent=4)

def import_tasks_from_json(db: Session, file_path: str):
    import json
    with open(file_path, "r") as file:
        tasks_data = json.load(file)
        for task in tasks_data:
            new_task = Task(title=task['title'], description=task['description'], completed=task['completed'])
            db.add(new_task)
        db.commit()
