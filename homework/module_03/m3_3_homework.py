"""M3.3 Homework: Prove Memory Isolation Between Users.

THE IDEA
Run the same agent under two user contexts in one workspace and verify memory
does not leak from user A to user B.

WHAT YOU FILL IN
  TODO 1: write two different seed memories (A and B).
  TODO 2: write three prompts to test recall and leak isolation.

RUN
  python -m homework.module_03.m3_3_homework
"""

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from deepagents.backends.utils import create_file_data
from langgraph.store.memory import InMemoryStore

from hello_agent import model

store = InMemoryStore()
memory_path = "/memories/AGENTS.md"
store_memory_path = "/AGENTS.md"

CONTEXT_A = {"workspace_id": "homework", "user_id": "u_you"}
CONTEXT_B = {"workspace_id": "homework", "user_id": "u_teammate"}


def namespace_from_context(context):
    return ("memory", context["workspace_id"], context["user_id"])


def memory_namespace(runtime):
    return namespace_from_context(runtime.context)


def build_seed_memory_a() -> str:
    """Return user A's fictional migration project notes."""
    return """\
# Migration Project Notes

- My project is Project Bluebird.
- My migration cutover is scheduled for Saturday.
"""


def build_seed_memory_b() -> str:
    """Return user B's fictional migration project notes."""
    return """\
# Migration Project Notes

- My project is Project Cedar.
- My migration cutover is scheduled for Sunday.
"""


store.put(
    namespace_from_context(CONTEXT_A),
    store_memory_path,
    create_file_data(build_seed_memory_a()),
)
store.put(
    namespace_from_context(CONTEXT_B),
    store_memory_path,
    create_file_data(build_seed_memory_b()),
)

agent = create_deep_agent(
    model=model,
    name="Homework_Memory_Agent",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={"/memories/": StoreBackend(namespace=memory_namespace)},
    ),
    store=store,
    memory=[memory_path],
    system_prompt="You are a helpful personal assistant for this project.",
)

RECALL_QUESTION = "What is my migration project name and cutover day?"
REMEMBER_MESSAGE = (
    "Remember this new detail for my migration project: the rollback code is "
    "ORION-472. Update /memories/AGENTS.md with this detail."
)
LEAK_CHECK_QUESTION = RECALL_QUESTION

result_a1 = agent.invoke(
    {"messages": [{"role": "user", "content": RECALL_QUESTION}]}, context=CONTEXT_A
)
print("--- Context A, Question 1 ---")
print(result_a1["messages"][-1].text)

result_a2 = agent.invoke(
    {"messages": [{"role": "user", "content": REMEMBER_MESSAGE}]}, context=CONTEXT_A
)
print("\n--- Context A, Question 2 (remember) ---")
print(result_a2["messages"][-1].text)

result_b = agent.invoke(
    {"messages": [{"role": "user", "content": LEAK_CHECK_QUESTION}]}, context=CONTEXT_B
)
print("\n--- Context B, leak-check question ---")
print(result_b["messages"][-1].text)

memory_a = store.get(namespace_from_context(CONTEXT_A), store_memory_path).value[
    "content"
]
memory_b = store.get(namespace_from_context(CONTEXT_B), store_memory_path).value[
    "content"
]
print("\n--- Context A's stored AGENTS.md ---")
print(memory_a)
print("\n--- Context B's stored AGENTS.md ---")
print(memory_b)

answer_a = result_a1["messages"][-1].text.casefold()
answer_b = result_b["messages"][-1].text.casefold()
checks = {
    "A recalls its project and cutover day": (
        "bluebird" in answer_a and "saturday" in answer_a
    ),
    "A's new rollback code was stored": "orion-472" in memory_a.casefold(),
    "B recalls its own project and cutover day": (
        "cedar" in answer_b and "sunday" in answer_b
    ),
    "A's project and rollback code are absent from B's answer": (
        "bluebird" not in answer_b and "orion-472" not in answer_b
    ),
    "B's stored memory remains unchanged": memory_b == build_seed_memory_b(),
}
print("\n--- Memory checks ---")
for label, passed in checks.items():
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
