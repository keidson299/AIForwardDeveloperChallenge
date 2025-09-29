# Deploying AI Agents

## Overview

This document outlines a possible deployment strategy for the ReadabilityGuardian and OptimizationExpert AI agents using VS Code integration and Github CI/CD pipelines.

## Why This Approach?

This approach matches with the current environment and development tools used to build out the existing mcp server, those mainly being VS Code and Github.

**1. IDE Integration**

VS Code integration provides several key benefits:

- Real-time feedback during development
- Seamless developer experience
- Integrated task management
- Native code analysis visualization

**2. CI/CD Integration**

GitHub Actions integration ensures:

- Consistent code quality across all contributions
- Automated quality gates for PRs
- Historical tracking of code quality metrics
- Team-wide enforcement of standards

## Implementation Strategy

**1. VS Code Extension**

Create a VS Code extension to host both agents:

```python
import * as vscode from 'vscode';
import { ReadabilityGuardian, OptimizationExpert } from './agents';
import { MCPClient } from './mcp-client';

export function activate(context: vscode.ExtensionContext) {
    const mcpClient = new MCPClient('localhost:3000');
    const readabilityAgent = new ReadabilityGuardian(mcpClient);
    const optimizationAgent = new OptimizationExpert(mcpClient);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('codeQuality.analyzeReadability', async () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                await readabilityAgent.analyzeFile(editor.document.uri);
            }
        }),
        vscode.commands.registerCommand('codeQuality.analyzeEfficiency', async () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                await optimizationAgent.analyzeFile(editor.document.uri);
            }
        })
    );
}
```

By using a vscode.ExtensionContext, we are able to integrate into VS Code's UI by having the commands available in the Palette. The extension also enables real-time file analysis, and uses a singular client to reduce connection overhead.

**2. Agent Implementation**

Next we create our agent implementation. This is an example of the implementation for the ReadabilityGuardian defined in CodeReadabilityAgent.md

```python
export class ReadabilityGuardian {
    private diagnosticCollection: vscode.DiagnosticCollection;

    constructor(private mcpClient: MCPClient) {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('readability');
    }

    async analyzeFile(fileUri: vscode.Uri): Promise<void> {
        const analysis = await this.mcpClient.callTool('analyze_file', {
            file_path: fileUri.fsPath
        });

        if (!analysis.hasComments || !analysis.hasFunctions) {
            await this.createImprovementTask(fileUri, analysis);
            await this.logAnalysisWork(fileUri);
            await this.updateDiagnostics(fileUri, analysis);
        }
    }

    private async updateDiagnostics(fileUri: vscode.Uri, analysis: any): Promise<void> {
        const diagnostics: vscode.Diagnostic[] = [];
        this.diagnosticCollection.set(fileUri, diagnostics);
    }
}
```

This agent structure integrates directly with VS Code diagnostics creating a soother experience when using it. The agent is able to automatically create tasks using the add_task mcp tool, and log the work done by using the log_work mcp tool.

**3. GitHub Actions Integration**

Moving to the CI\CD implementation, we create a Github Actions workflow:

```
name: Code Quality Analysis

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  analyze:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install fastmcp

      - name: Start MCP Server
        run: |
          start /B python main.py
          timeout /T 5

      - name: Run Code Quality Analysis
        run: python run_analysis.py
```

This workflow allows for automatic quality checks on all PR's a user creates, not only providing a consistent CI\CD pipeline for deployment, but also granting a tracking of quality metrics to examine long-term trends.

**4. Analysis Runner**

Up next, we implement an Analysis Runner:

```python
import asyncio
from pathlib import Path
from mcp.transport import Client
from typing import Dict, List

class QualityAnalysisRunner:
    def __init__(self):
        self.client = Client("main.py")
        self.issues_found: Dict[str, List[str]] = {}

    async def analyze_repository(self):
        source_files = Path('.').rglob('*.py')

        async with self.client:
            for file in source_files:
                await self.analyze_single_file(file)

    async def analyze_single_file(self, file: Path):
        analysis = await self.client.call_tool(
            "analyze_file",
            {"request": {"file_path": str(file)}}
        )

        if not analysis.value.get("hasComments", False):
            self.issues_found.setdefault(str(file), []).append("Missing documentation")

if __name__ == "__main__":
    runner = QualityAnalysisRunner()
    asyncio.run(runner.analyze_repository())
```

This runner provides repo-wide analysis by iterating through each file, and using the mcp tools to analyze the files. Right now the implementation only has comment tracking, but the functionality can be expanded

**5. Configuration**

Finally, the agent configurations:

```
agents:
  readability_guardian:
    enabled: true
    rules:
      - check_docstrings
      - check_naming_conventions
    thresholds:
      min_comment_ratio: 0.2

  optimization_expert:
    enabled: true
    rules:
      - check_complexity
      - check_memory_usage

mcp_server:
  host: localhost
  port: 3000
  log_level: info
```

These definitions describe how and what the agents can use. Right now they have a few example rules and thresholds for their respective focuses

## Deployment Steps

**1. Install the VS Code extension:**

```
code --install-extension path/to/vsix
```

**2. Start the MCP server:**

```
python main.py
```

**3.Configure GitHub repository:**

- Add the workflow file to .github/workflows
- Set up required secrets for GitHub Actions
- Enable GitHub Actions in repository settings

**4.Usage in VS Code:**

- Command Palette: Code Quality: Analyze Readability
- Command Palette: Code Quality: Analyze Efficiency
- View results in Problems panel
- Track tasks in VS Code TODO tree

### The agents will now:

- Run automatically on PR creation
- Be available through VS Code commands
- Log issues and suggestions
- Create and track improvement tasks
- Maintain a work log of all analyses

## Deployment Benefits

**1. Developer Experience**

- Immediate feedback in IDE
- Automated issue detection
- Integrated task management

**2. Team Collaboration**

- Consistent code quality standards
- Automated PR reviews
- Shared configuration

**3.Quality Assurance**

- Continuous code quality monitoring
- Historical tracking
- Automated enforcement

**4.Maintenance**

- Centralized configuration
- Easy updates and modifications
- Plugin architecture
