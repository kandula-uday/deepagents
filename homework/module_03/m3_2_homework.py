"""M3.2 Homework: Bundle a Reference File Into Your Skill.

THE IDEA
Create a skill where SKILL.md tells the agent to read reference.md for key
details, then verify the agent actually reads that file.

The skill files are in skills/migration-readiness beside this script.

RUN
  python -m homework.module_03.m3_2_homework
"""

from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend

from hello_agent import model

SKILL_NAME = "migration-readiness"
REFERENCE_PATH = f"/skills/{SKILL_NAME}/reference.md"


module_dir = Path(__file__).resolve().parent
skill_dir = module_dir / "skills" / SKILL_NAME
backend = FilesystemBackend(root_dir=str(module_dir), virtual_mode=True)
print(f"Skill files located at: {skill_dir}")

SYSTEM_PROMPT = (
    "You are a cloud migration project assistant. Be clear and practical, "
    "and use the available skills when relevant."
)
USER_QUESTION = (
    "Assess whether the Project Bluebird data migration pilot is ready for "
    "cutover. Data validation matched 99.7% of records, replication delay "
    "is 10 minutes, the rollback test passed, and business approval was "
    "received. Give a GO or NO-GO decision and explain each check."
)

agent = create_deep_agent(
    model=model,
    name="Homework_Agent",
    backend=backend,
    skills=["/skills"],
    system_prompt=SYSTEM_PROMPT,
)

result = agent.invoke({"messages": [{"role": "user", "content": USER_QUESTION}]})
print(result["messages"][-1].text)

read_calls = [
    call
    for msg in result["messages"]
    for call in getattr(msg, "tool_calls", [])
    if call["name"] == "read_file"
]
reference_was_read = any(
    call["args"].get("file_path") == REFERENCE_PATH for call in read_calls
)
print(f"\n--- Did the agent read {REFERENCE_PATH}? {reference_was_read} ---")
if not reference_was_read:
    print(
        "It didn't. Either SKILL.md isn't clearly telling it to, or the "
        "task is answerable without details from reference.md."
    )
