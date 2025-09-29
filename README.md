# MCP Server Setup Guide

## Overview
This guide explains how to set up and run the MCP server, execute tests, and integrate with Claude Desktop.

## Prerequisites
- Python 3.10 or higher
- fastmcp package installed (pip install fastmcp)
- Claude Desktop application

## Project Structure
```
├── main.py # MCP server implementation
├── test_mcp_tools.py # Test suite
├── config/
│ └── claude_desktop_config.json
├── logs/ # Log files directory
│ ├── mcpServer.log
│ └── work_log.json
└── tasks.json # Task management storage
```

This Project was built and tested in VSCode, and the instructions reflect that. You may have to modify the instructions if you are using a different IDE

## Getting Started

### 1. Setup Required Directories
First, create the necessary directories and files by running these commands in a powershell terminal:
```powershell
mkdir logs
echo "[]" > tasks.json
echo "[]" > logs/work_log.json
```
### 2. Install FastMCP
In a powershell terminal, run the command:
```powershell
pip install fastmcp
```
### 3. Starting the MCP Server
In a PowerShell terminal run the command:
```powershell
python main.py
```
You should see a FastMCP startup text, and no further output as the server communicates through stdin/stdout.

### 4. Running Tests
Open a second PowerShell terminal and run:
```powershell
python test_mcp_tools.py
```
Expected Output:
```
Starting MCP server tests...

Testing analyze_file...
File analysis result: {
"lineCount": 5,
"hasTodos": true,
"hasFunctions": true,
"hasComments": true
}
✅ analyze_file test passed

Testing log_work...
...
```
## Claude Desktop Integration

### 1. Configure Claude Desktop
1. Open Claude Desktop
2. Go to Settings > Developer
3. Enable Developer Mode
4. Update the MCP configuration:
```json
{
   "mcpServers": {
      "software-support": {
         "command": "python",
         "args": ["path/to/server/file/main.py"],
      }
   }
}
```
### 2. Testing the Integration
1. In Claude Desktop, create a new chat
2. Send a test message to use one of the MCP tools:
```
Can you analyze the file test_mcp_tools.py using the analyze_file tool?
```
## Available MCP Tools
- analyze_file: Analyzes code files for metrics
- log_work: Records work activities
- add_task: Creates new tasks
- list_tasks: Shows all tasks
- complete_task: Marks tasks as completed

## Troubleshooting

### Common Issues

1. **Server Not Starting**
   - Check Python version:
   ```powershell
   python --version
   ```
   - Verify fastmcp installation:
   ```powershell
   pip list | findstr fastmcp
   ```
2. **Claude Desktop Connection Failed**
   - Verify the path in claude_desktop_config.json matches your project location
   - Ensure Developer Mode is enabled
   - Check Claude Desktop logs for connection errors

3. **Tests Failing**
   - Make sure the MCP server is running in a separate terminal
   - Check if tasks.json and log files exist
   - Review logs/mcpServer.log for errors

## Logs
Check the following logs for troubleshooting:
   - Server logs: logs/mcpServer.log
   - Work logs: logs/work_log.json

For additional support, review the error messages in the terminal output or check the Claude Desktop developer console.
