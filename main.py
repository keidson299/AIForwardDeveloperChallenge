from fastmcp import FastMCP
from pydantic import BaseModel
import os
from datetime import datetime
import json
from pathlib import Path
import logging
from typing import List, Optional
from enum import Enum

class FileRequest(BaseModel):
    file_path: str

class FileAnalysis(BaseModel):
    lineCount: int
    hasTodos: bool
    hasFunctions: bool
    hasComments: bool

class WorkLog(BaseModel):
    description: str

class WorkLogResponse(BaseModel):
    timestamp: str
    description: str
    success: bool

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str
    completed_at: Optional[str] = None

class AddTaskRequest(BaseModel):
    title: str

class CompleteTaskRequest(BaseModel):
    task_id: int

class TaskResponse(BaseModel):
    success: bool
    message: str
    task: Optional[Task] = None

class TaskListResponse(BaseModel):
    tasks: List[Task]

app = FastMCP("Software Development Support MCP Server")

@app.tool()
async def analyze_file(request: FileRequest) -> FileAnalysis:
    """
    Analyzes a file and returns metrics about its contents.
    Accepts either a file path or direct file content with filename.
    
    Args:
        request: Either a FileRequest with file_path or FileContent with content and file_name
        
    Returns:
        FileAnalysis object with metrics about the file
    """
    try:
        logger.info(f"Received analyze_file request: {request}")

        # If the input is a string, try to parse it as JSON
        if isinstance(request, str):
            logger.info("Parsing request string as JSON")
            try:
                data = json.loads(request)
                logger.info(f"Data {data}")
                if "file_path" in data:
                    request = FileRequest(**data)
                    logger.info(f"File request: {request}")
                else:
                    logger.info("Invalid input format")
                    raise ValueError("Invalid input format")
            except json.JSONDecodeError:
                logger.info("Invalid JSON format")
                raise ValueError("Invalid JSON format")

        content = ""
        logger.info("Content initialized")
        if isinstance(request, FileRequest):
            logger.info(f"Reading file from path: {request.file_path}")
            file_path = Path(request.file_path)
            if not file_path.exists():
                logger.info("Empty file content")
                return FileAnalysis(
                    lineCount=0,
                    hasTodos=False,
                    hasFunctions=False,
                    hasComments=False
                )
            content = file_path.read_text(encoding='utf-8')
        
        if not content:
            logger.info("Empty file content")
            return FileAnalysis(
                lineCount=0,
                hasTodos=False,
                hasFunctions=False,
                hasComments=False
            )

        lines = content.splitlines()
        
        logger.info("File being analyzed")

        return FileAnalysis(
            lineCount=len(lines),
            hasTodos="TODO" in content.upper(),
            hasFunctions=any(line.strip().startswith(("def ", "class ", "function ")) for line in lines),
            hasComments=any(line.strip().startswith(("#", "//", "/*", "*", "'''", '"""')) for line in lines)
        )

    except Exception as e:
        print(f"Error analyzing file: {str(e)}")
        return FileAnalysis(
            lineCount=0,
            hasTodos=False,
            hasFunctions=False,
            hasComments=False
        )
    
@app.tool()
async def log_work(work: WorkLog):
    """Logs work with timestamp and description to a JSON file."""
    log_file = "logs/work_log.json"
    current_time = datetime.now().isoformat()
    
    logger.info("Creating work log entry")
    # Create new log entryo
    log_entry = {
        "timestamp": current_time,
        "description": work.description
    }
    
    logger.info("Loading existing logs or creating new list")
    # Load existing logs or create new list
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
        
    logger.info("Appending new log entry")
    # Append new log
    logs.append(log_entry)
    
    logger.info("Saving updated logs to file")
    # Save updated logs
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
        
    logger.info("Returning response")
    return WorkLogResponse(
        timestamp=current_time,
        description=work.description,
        success=True
    )

@app.tool()
async def add_task(request: AddTaskRequest) -> TaskResponse:
    """Adds a new task to the task list."""
    tasks_file = "tasks.json"
    current_time = datetime.now().isoformat()

    logger.info("Adding a new task to the list")
    
    # Load existing tasks or create new list
    if os.path.exists(tasks_file):
        logger.info("File exists")
        with open(tasks_file, 'r') as f:
            logger.info("Loading existing tasks")
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                logger.info("JSON decode error, initializing empty tasks list")
                tasks = []
    else:
        logger.info("Log file does not exist, creating new one")
        tasks = []
    
    logger.info("Creating new task")
    # Generate new task ID
    task_id = len(tasks) + 1
    
    # Create new task
    new_task = {
        "id": task_id,
        "title": request.title,
        "status": TaskStatus.PENDING.value,
        "created_at": current_time,
        "completed_at": None
    }

    logger.info(f"New Task created {new_task}")
    
    # Add task to list
    tasks.append(new_task)
    
    logger.info("Appended new task to tasks list")

    # Save updated tasks
    with open(tasks_file, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    logger.info("Wrote to file and returning response")

    return TaskResponse(
        success=True,
        message=f"Task '{request.title}' added successfully",
        task=Task(**new_task)
    )

@app.tool()
async def list_tasks() -> TaskListResponse:
    """Returns a list of all tasks."""
    tasks_file = "tasks.json"
    
    logger.info("Finding tasks")
    if not os.path.exists(tasks_file):
        return TaskListResponse(tasks=[])
    
    logger.info("Loading tasks from file")
    with open(tasks_file, 'r') as f:
        tasks = json.load(f)
    
    logger.info("Returning task list")
    return TaskListResponse(
        tasks=[Task(**task) for task in tasks]
    )

@app.tool()
async def complete_task(request: CompleteTaskRequest) -> TaskResponse:
    """Marks a task as completed."""
    tasks_file = "tasks.json"
    current_time = datetime.now().isoformat()
    
    logger.info("Finding task file")
    if not os.path.exists(tasks_file):
        return TaskResponse(
            success=False,
            message="No tasks found",
            task=None
        )
    
    logger.info("Loading tasks from file")
    with open(tasks_file, 'r') as f:
        tasks = json.load(f)
    
    logger.info("Searching for task by ID")
    # Find task by ID
    task_found = False
    for task in tasks:
        if task["id"] == request.task_id:
            if task["status"] == TaskStatus.COMPLETED.value:
                logger.info("Task already completed")
                return TaskResponse(
                    success=False,
                    message="Task already completed",
                    task=Task(**task)
                )
            logger.info("Marking task as completed")
            task["status"] = TaskStatus.COMPLETED.value
            task["completed_at"] = current_time
            task_found = True
            completed_task = task
            break
    
    if not task_found:
        logger.info("Task not found")
        return TaskResponse(
            success=False,
            message=f"Task with ID {request.task_id} not found",
            task=None
        )
    
    logger.info("Task marked as completed, saving to file")
    # Save updated tasks
    with open(tasks_file, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    logger.info("Returning response")
    return TaskResponse(
        success=True,
        message=f"Task {request.task_id} marked as completed",
        task=Task(**completed_task)
    )

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    logging.basicConfig(filename="logs/mcpServer.log", level=logging.INFO)

    logger.info("Starting MCP server...")
    app.run(transport="stdio")