# Module 01: Agent Basics

These programs explore how to guide an agent, give it tools, manage
conversation state, and ask a person to review an action.

## 1. System prompts

[m1_4_system_prompt.py](./m1_4_system_prompt.py) gives the agent a quantum
physics role and asks it to redirect questions outside that topic. It sends
one question about physics and another about geography to see how the agent
responds. A prompt guides behavior but does not guarantee compliance.

## 2. Custom tools

[m1_5_custom_tools.py](./m1_5_custom_tools.py) defines a `lookup_fact` tool
with a small collection of facts. The agent is instructed to use the tool
when answering factual questions. The example asks about Python.

## 3. MCP tools

[m1_6_mcp_tools.py](./m1_6_mcp_tools.py) connects to the DeepWiki MCP server,
discovers its tools, and selects `ask_wiki_question`. The agent then asks
about filesystem backends in the Deep Agents repository. This example needs
network access and sends the question to an external service; avoid including
private information.

## 4. Conversation threads

[m1_7_memory_threads.py](./m1_7_memory_threads.py) shares a favorite
programming language in one thread, then asks about it in the same thread, a
different thread, and a new agent with a fresh `MemorySaver`.

The goal is to compare conversation state across threads and checkpointers.
The responses are printed for inspection, not automatically graded.
`MemorySaver` keeps state in memory and does not persist it after the process
ends.

## 5. Human approval

[m1_8_human_approval.py](./m1_8_human_approval.py) pauses before a simulated
Slack action. In an interactive terminal, a person can approve, edit, or
reject the proposed action. The tool only simulates the action; it does not
send a real Slack message.

## Running the programs

From the practice repository root, with the project environment and model
credentials configured:

```bash
python -m homework.module_01.m1_4_system_prompt
python -m homework.module_01.m1_5_custom_tools
python -m homework.module_01.m1_6_mcp_tools
python -m homework.module_01.m1_7_memory_threads
python -m homework.module_01.m1_8_human_approval
```

These programs call a model and may incur usage costs. Responses and tool
choices can vary between runs.
