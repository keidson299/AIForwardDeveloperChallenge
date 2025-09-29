# AI-Forward Developer Take-Home Challenge Project Plan

## Understanding Model Context Protocol

Model Context Protocol (MCP) is a standardized communication protocol that enables AI models to interact with external tools and services. It allows AI models to extend their capabilities beyond text generation by accessing real-world data, performing defined actions, and taking advantage of existing systems and tools.

There are two core components to how MCP works: Servers and Tools

### Servers

Servers are the hosting appliction of the protocol, and handle the JSON-RPC communication that enables AI models to utilize MCP tools. This communication is done either through http or stdio messages. The server does all the normal functions you would imagine a server does (validate requests and responses, store any persistent data, log communication and data transfers, etc), but they also store the function definitions for the tools.

### Tools

Tools are functions that are exposed to the AI model by the server. They perform specfic tasks based on defined structured inputs and return defined structured outputs. These inputs and outputs are built using JSON-RPC. While there is a structure to the inputs and outputs, the functionality any particular tool provides is up to the developer. There are examples ranging from tools that search for specifc files in a computer's file system, to those that connect to a web hosted api to provide specific data when requested (eg a weather tool that reaches out to the National Weather Service API).

## Initial Project Planning

The first step to any new project is to understand the requirements and limitations of the project. After reading through the CHALLENGE.md file, the requirements and limitations can be broken down into 5 major categories:

1. AI models should be utilized in as many places as reasonably possible
2. Project progress should be maintained through a git repository
3. The project has two major coding design and implementation pieces: an MCP Server and AI Agents Designs
   a. The MCP Server should be built with supporting software development in mind and there is a list of examples that can be used to test, develop, and build off of
   b. The MCP Server should work with at least one AI model and evidence is required to demonstrate it working with said model
   c. There should be 1 -3 AI Agents definitions, and they should be focused on improving code quality, have a detailed description of the agents, and information how they are deployed
4. The submission requires all the above code and documentation along with instructions on how to use the server and a brief reflection of how the development went
5. The submission must be sent in within 5 days of receiving the project plan. Prioritization of key functionality is critical

Now that the requirements and limitations have been layed out, they can be tackled using a step by step plan.

## Step 0: Code Language & IDE

This is a simple choice, this project will be using Python in VSCode to design, develop, implement, and test this project. The extensions and libraries, the easy access to any AI model of choice, and the extensive documentation for both make it an easy decision.

## Step 1: AI Model

Now to choose an AI model to utilize through the whole project. While one could use mutliple models, each for a different purpose (ie Chat-GPT for code suggestions, Claude to connect to the server, etc.), using a singular model throughout will avoid any mistakes that may come from having to switch between several AI models. So following that principle, this project will use Claude Sonnet through Github CoPilot and Claude Desktop as the AI model for this project. There are a few reasons to chose this setup for the project:

1. Github CoPilot comes with Claude Sonnet as one of the built in LLMs to choose from and Claude Desktop is a simple installation process, thus removing any tricky installations or confusing configurations
2. As Anthropic developed both Claude and MCP, they have extensive documentation and examples on how to setup, configure, build, and test a MCP server and tools
3. Claude (while requiring an account) is free to the extent necessary to complete this project. While there may be a benefit to having access to larger models, having to pay for either a month or a year for a 5 day timed project is excesive.
4. Speaking for myself, all of the models and corresponding tools are well incorporated into my existing development processes, removing any learning curves for usage, AI prompting, etc.

While there may be some AI models that have slightly better performance in certain areas, these reasons are a solid enough justification to select Claude in CoPilot and Desktop for this project.

## Step 2: Git Repository

Next on the list is the git repository. Standard practice will be to use GitHub for this, which is what this project will be doing as well. Similar to with the AI model selection, Github is well established, has extensive documentation and examples, and is integrated into VSCode, removing barriers that could hinder development.

For my iteration of this project, my repository is AIForwardDeveloperChallenge and is publicly available to view at https://github.com/keidson299/AIForwardDeveloperChallenge

## Step 3: Building the features

Now that the environment, language, AI tools, repository, and other setup steps are completed, the time has come to begin developing the required features. The features can be broken up into two main categories: the MCP Server, and the AI Agents. While not explicitly mentioned in each step, ideally after each new piece of functionality is added, commits to the repository will be made for code management.

### Step 3a: MCP Server

First, we start with the AI model to see what it suggests in terms of first steps and simple code output for the creation of the server. This can also be verified or built up using info on https://modelcontextprotocol.io. The website also provides information on MCP server architecture, connections, and developer tools.

Once a simple server has been created, next is to start expanding the funtionality. Both Claude and the modelcontextprotocol.io site will be used to build the tools one at a time. The code and structure will be left to Claude, however it's still important to use the MCP io site and other documentation sites as artifacts of truth. This way the AI model's accelerated coding can be taken full advantage of, while also catching issues from hallucination before spiralling out of control. Importantly, build each tool one at a time to allow for easier debugging.

Then, there is the process of writing a testing script to automate the testing of the tools. This will allow for easier and faster testing. Claude can be leveraged (through utilizing the context from our server and testing script file) to output more usable code, acccelerating the expansion of the script to test new tools as they get added.

After a tool has been built a validated using both terminal communication and the testing script, the final step is to connect the server to Claude Desktop to validate the AI model's ability to communicate with and utilize the tool. For this, there will have to be a configuration file and test files to properly connect to the MCP server, and have consistent data to test the tools with.

Once there is a working MCP server, and a tool or two, successfully tested with the terminal, test script, and Claude Desktop (and committed to the repository) the same steps can be followed again: Use Claude to generate the code for a new tool and test (both using the context of the existing files), then validate the tools using the terminal, testing script, and Claude Desktop. Repeat this until all the functionality is implemented.

### Step 3b: Agent Design

As the requirements only ask for the design of AI Agents, it is much easier take advantage of Claude. We can use it for both the research step to determine how best to structure, configure, command, and deploy an AI Agent, as well as ask for suggestions on how to design one for a specifc purpose.

While the plan for this requirement is much simpler (as this does not require testing), much more of the resulting output will be reliant on having clear and concise wording, effective use of the AI model, and proficient knowledge of AI Agents. As such, research on AI Agent design and deployment, as well as ensuring any hallucinatory "facts" being stamped out is critical for this step.

## Step 4: Clean up for submission

Since this project is not just a personal project but will be submitted for review, take appropriate time before submitting to review it. This will invlove:

1. Ensuring that all of the required documents, screenshots, code, etc are included
2. Looking over code to inspect for any errant lins, poorly worded syntax, and useless
   functionality
3. Reviewing documentation so that a reader can reasonably follow not only the development process
   but also properly recreate the setup and test the project for themselves

Once these check are complete, write a debrief of the project. Use this to reflect on issues that were or were not overcome, interesting things learned, how to utilize this new knowledge in other porjects, etc.

# Step 5: Submit

Finally, all that's left is to zip the files up and submit them for review.
