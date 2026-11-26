# Module 03: Context Management

These programs explore three ways an agent can use context: summarizing a
conversation, loading task-specific instructions, and keeping separate
memories for different users. The project details are fictional.

## 1. Conversation summarization

[m3_1_homework.py](./m3_1_homework.py) starts a conversation about Project
Bluebird, an on-premises-to-cloud migration with a $48,000 budget. After
several turns, it asks the agent to recall the project name and budget.

The goal is to trigger summarization at least twice and see whether the agent
can still recall the early details. The script prints summarization events
and checks the conversation history for saved sections.

- `MemorySaver` keeps the conversation state between turns in the same thread.
- `MAX_INPUT_TOKENS` sets the model profile value used for the summarization
  threshold in this exercise. Results can vary by model and conversation.
- The history path is a virtual path in the agent state, not a local file.
  The state is in memory and is lost when the process ends.

## 2. Skills and reference files

[m3_2_homework.py](./m3_2_homework.py) asks the agent to decide whether a
fictional migration pilot is ready for cutover. It demonstrates how a skill
can provide task-specific instructions and point to a separate reference file.

- [SKILL.md](./skills/migration-readiness/SKILL.md) describes when to use the
  skill and tells the agent what steps to follow.
- [reference.md](./skills/migration-readiness/reference.md) contains the
  fictional readiness criteria.
- `FilesystemBackend` gives the agent access to the project-local skill files.
- The script checks whether the agent called `read_file` on the reference.

The example's expected decision is **NO-GO**: the reported replication delay
is 10 minutes, above the reference's fictional 8-minute limit. A skill guides
the agent; it does not guarantee that the agent follows every instruction.

## 3. Memory isolation

[m3_3_homework.py](./m3_3_homework.py) uses one agent with two user contexts
in the same workspace. Each user starts with different migration project notes.

The script asks user A's project question, asks the agent to save a new detail
for A, and then asks the same project question as user B. It prints checks for
recall, A's update, and whether B's stored memory remains unchanged.

- `InMemoryStore` holds the memory during the running process.
- `namespace_from_context` builds a namespace using the workspace and user IDs.
- `memory_namespace` uses the current run's context to select a namespace for
  the `StoreBackend`.
- The checks demonstrate this example's behavior; they are not a complete
  security test. The in-memory store is lost when the process ends.

## Running the programs

From the practice repository root, with the project environment and model
credentials configured:

```bash
python -m homework.module_03.m3_1_homework
python -m homework.module_03.m3_2_homework
python -m homework.module_03.m3_3_homework
```

These programs call a model, so they require access to the configured provider
and may incur usage costs. Agent responses and summarization counts can vary.
