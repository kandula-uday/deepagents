# Module 02: Execution and Filesystems

These programs explore how an agent can work with files, run code in a
sandbox, and use an interpreter to coordinate database queries.

## 1. Filesystem backend

[filesystem_backends.py](./filesystem_backends.py) creates fictional cloud
migration meeting notes, then asks the agent to read them and write a summary.
It uses a `FilesystemBackend` rooted in [meeting_notes/](./meeting_notes) and
a permission rule that denies the agent's write operation on `/notes.md`.
The summary is requested at `/notes_summarize.md`.

The script itself rewrites `notes.md` with the seed content every time it
runs. Save any changes you want to keep elsewhere before running it.

## 2. Sandbox execution

[sandbox_execution.py](./sandbox_execution.py) creates a LangSmith sandbox
and gives the agent two tasks:

1. Generate fictional weekly migration data and save it as JSON in the sandbox.
2. Read the same data and create a chart in that sandbox.

The script then reads the chart from the sandbox into a local
`homework_chart.png` file and deletes the sandbox in a `finally` block. Sandbox
access must be enabled for the LangSmith organization; otherwise creation can
fail with a permissions error.

## 3. Interpreter and database

[interpreter.py](./interpreter.py) asks which Chinook artist has the most
albums, how many albums they have, and which album comes first alphabetically.
The local [chinook.db](./chinook.db) is opened in read-only mode by the
`query_chinook` tool.

`CodeInterpreterMiddleware` makes an `eval` tool available to run JavaScript.
That JavaScript can call `query_chinook` to coordinate dependent queries.
After the agent answers, `eval_answer` independently queries the database and
checks whether the expected values appear in the text. This is a simple
content check, not a complete evaluation of the answer.

## Running the programs

From the practice repository root, with the project environment and model
credentials configured:

```bash
python -m homework.module_02.filesystem_backends
python -m homework.module_02.sandbox_execution
python -m homework.module_02.interpreter
```

These programs call a model and may incur usage costs. The sandbox exercise
also requires LangSmith sandbox access. Agent responses and tool choices can
vary between runs.
