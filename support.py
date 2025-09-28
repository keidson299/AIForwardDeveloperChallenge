from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="MCP Server", description="Model Context Protocol Server with File Analysis")

class FileRequest(BaseModel):
    file_path: str

class FileAnalysis(BaseModel):
    lineCount: int
    hasTodos: bool
    hasFunctions: bool
    hasComments: bool

@app.post("/analyze-file", response_model=FileAnalysis)
async def analyze_file(request: FileRequest):
    """Analyzes a file and returns metrics about its contents."""
    try:
        if not os.path.exists(request.file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")
        
        with open(request.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.splitlines()
            
            # Calculate metrics
            metrics = FileAnalysis(
                lineCount=len(lines),
                hasTodos="TODO" in content.upper(),
                hasFunctions=any(line.strip().startswith(("def ", "class ", "function ")) for line in lines),
                hasComments=any(line.strip().startswith(("#", "//", "/*", "*", "'''", '"""')) for line in lines)
            )
            
            return metrics
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)