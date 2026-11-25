from pathlib import Path
from uuid import uuid4

from deepagents import create_deep_agent
from deepagents.backends.langsmith import LangSmithSandbox
from langsmith.sandbox import SandboxClient

from hello_agent import model


def main():
    SYSTEM_PROMPT = (
        "You are a data analyst helping a team plan a cloud data migration. "
        "Use only fictional data for this exercise. When asked to run code, "
        "write a Python script to a file in the sandbox before executing it. "
        "If you need to install a package in this sandbox, use "
        "`pip install --break-system-packages <package>`. Use matplotlib "
        "for charts, and report the paths of files you create."
    )

    TASK_ONE = (
        "Generate eight weeks of fictional cloud migration data: for each week, "
        "record the week number and the number of gigabytes migrated that week. "
        "Write and run a Python script that saves the data as a JSON list to "
        "/migration_data.json, then print the saved data."
    )
    TASK_TWO = (
        "Read the existing /migration_data.json file from the first task; do not "
        "regenerate or replace the data. Write and run a Python script that uses "
        "matplotlib to create a bar chart of gigabytes migrated per week. "
        "Label the axes and save the chart to /migration_chart.png. If the "
        "data file is missing, report the error instead of inventing new data."
    )

    CHART_PATH = "/migration_chart.png"

    client = SandboxClient()
    sandbox = client.create_sandbox(name=f"migration-homework-{uuid4().hex[:8]}")
    try:
        print(f"Sandbox: {sandbox.name} (id: {sandbox.id})")
        sandbox_backend = LangSmithSandbox(sandbox=sandbox)
        # TODO: Create an agent with sandbox_backend and run the two tasks.
        agent = create_deep_agent(
            model=model,
            backend=sandbox_backend,
            system_prompt=SYSTEM_PROMPT,
        )
        result = agent.invoke({"messages": [{"role": "user", "content": TASK_ONE}]})
        print("--- Task 1 ---")
        print(result["messages"][-1].text)

        result = agent.invoke({"messages": [{"role": "user", "content": TASK_TWO}]})
        print("\n--- Task 2 (same sandbox, should see Task 1's file) ---")
        print(result["messages"][-1].text)

      

        chart_bytes = sandbox.read(CHART_PATH)
        out_path = Path(__file__).parent / "homework_chart.png"
        out_path.write_bytes(chart_bytes)
        print(f"Chart saved to {out_path}")
    finally:
        client.delete_sandbox(sandbox.name)


if __name__ == "__main__":
    main()
