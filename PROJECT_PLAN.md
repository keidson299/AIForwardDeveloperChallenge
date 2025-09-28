# AI-Forward Developer Take-Home Challenge Project Plan

# Initial Project Planning

The first step to any new project is to understand the requirements and limitations of the project.
After reading through the CHALLENGE.md file, there are a few important pieces of information to
take note of:

1. AI tools should be utilized in as many places as reasonably possible
2. Project progress should be maintained through a git repository
3. The project has two pieces MCP Server and Agents:
   a. The MCP (Model Context Protocol) Server should be built with supporting
   software development in mind and there is a list of examples that can be used to
   test, develop, and build off of
   b. The MCP Server should work with at least one AI tool and evidence is required to
   demonstrate it working with said tool
   c. There should be 1 -3 agents, they should be focused on improving code quality,
   and have a detailed description of the agents and how they are built, operated and used
4. The submission requires all the above code and documentation along with
   instructions on how to use the server and a brief reflection of how the development
   went
5. The submission must be sent in within 5 days of receiving the project plan. Therefore
   prioritization of key functionality is critical

Now that I have layed out the requirements and some limitations, we can begin by going step by
step through the list.

# Step 0: Code Language & IDE

This is a simple choice, I will be using Python in VSCode to design, develop, implement, and
test this project. The extensions and libraries to enable use of developer tools I find, easy
access to my preferred AI tool, and my extensive work history with both make it an easy decision.

# Step 1: AI Tool

Now to choose an AI tool to utilize through the whole project. While I could use mutliple tools,
each for a different purpose (ie Chat-GPT for code suggestions, Claude to connect to the server),
I believe that using a singular tool throughout will avoid any mistakes that may come from having
to switch between several tools. So following that principle, I have chosen to user Github
CoPilot with Claude Sonnet 3.5 as my AI coding tool for this project. There are a few I reasons I
chose this setup for the project:

1. It is the tool I am most comfortable using both in terms of total time using, but also with
   understanding its limitations, letting me know when to step in before things go awry
2. It is already integrated into my development environments and workflow. Avoiding extra module
   integrations will help to prevent issues that concern the tools rather than the project
3. I already have a microsoft account. Creating a whole array of new accounts is something I
   generally like to avoid

While there may be some AI tools that have slightly better performance in certain areas, I believe
these reasons are justification enough for me to select CoPilot with Claude on my system. Since its
already installed and configured, there are no extra steps for this requirement besides using the tool.

# Step 2: Git Repository

Next on the list is the git repository. I will be using GitHub for this as, similar to with the AI
tool selection, I know the tool and have experience with it, it is already integrated into my
workflow, and I have a preexisting account I can use for this project.

I have named my repository AIForwardDeveloperChallenge and it is publicly available to view at
https://github.com/keidson299/AIForwardDeveloperChallenge

# Step 3a: MCP Server

Now is the time to start building. But first, I need to do more research on how exactly MCP
Servers work, any existing standards and conventions that exist, and any tools or documentation
I can lean on.

First, I can start with our AI tool to see what information it provides, and I can look up info
on https://modelcontextprotocol.io. The website also provides information on the server
architecture, connections, and developer tools I can use.

Once I have a strong enough understanding of MCP, how its used, and how to preoperly build it out
I can use both Claude and the modelcontextprotocol.io site to build the server. The initial code
and structure I will leave to the code output from Claude, however I still feel its important to
use the MCP io site as an artifact of truth. That way I can take advantage of the accelerated
coding provided by the tool, while also being able to catch issues before they spiral out of control
through referencing the documentation and guides provided on the site.

Once I have a basic server built up, I can then start adding the unique functionality specified in
the requirements. I will start with the example functionality provided in the CHALLENGE.md file,
and if I have any further ideas while developing those, I can attempt to include them if there's
enough time.

Once I have a comfortable amount of functionality built up, I then integrate it into Claude Desktop
such that the defined functionality outputs correct and relevant information. There is some leniancy
due to the hallucinatory nature of LLMs, however, I believe through good and highly specific
implementation, I can avoid most of that issue.

# Step 3b: Agent Design

Similar to the creation of the MCP Server, I will begin the Agent design by doing research with both
Claude and online resources that I can find. Using these I will develop a strong enough
understanding of Agent design structure and limitations to be able to make between 1-3 agents. And
also similar to the MCP server step, depending on the time left and any other development that I
may have to do, I can attempt to design more agents.

Based on the agents design and definitions, I will also write a brief review on how these could be
deployed alongside other information regarding their uses, platform and tool requirements, etc.

# Step 4: Clean up for submission

Since this project is not just a personal project but wil be submitted for review, I will take
appropriate time before I submit my project to review it. This will invlove:

1. Ensuring that all of the required documents, screenshots, code, etc are included
2. Looking over code to inspect for any errant lins, poorly worded syntax, and useless
   functionality
3. Reviewing documentation so that a reader can reasonably follow not only my development process
   but also properly recreate my setup and test the project for themselves

Once these check are complete, I will write a overarching review of the project. I will use this to
reflect on issues that I had to overcome, issues I wasn't able to overcome, interesting things I
learned, how I can utilize this new knowledge in other porjects, etc.

# Step 5: Submit

Finally, the project is built, tested, and reviewed. All that's left is to zip the files up and
submit them for review.
