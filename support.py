from fastmcp import FastMCP
from pydantic import BaseModel
import os
from datetime import datetime
import json
from pathlib import Path
import logging

app = FastMCP("Software Development Support MCP Server")

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
    log_file = "work_log.json"
    current_time = datetime.now().isoformat()
    
    # Create new log entryo
    log_entry = {
        "timestamp": current_time,
        "description": work.description
    }
    
    # Load existing logs or create new list
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
        
    # Append new log
    logs.append(log_entry)
    
    # Save updated logs
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
        
    return WorkLogResponse(
        timestamp=current_time,
        description=work.description,
        success=True
    )

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    logging.basicConfig(filename="mcpServer.log", level=logging.INFO)

    logger.info("Starting MCP server...")
    app.run(transport="stdio")