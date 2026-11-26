"""M3.1 Homework: Trigger Chained Summarization.

THE IDEA
Lab 1 showed SummarizationMiddleware compressing a conversation once. On a
long enough thread, summarization can happen multiple times. This homework
asks you to trigger it at least twice and confirm the agent can still recall
an early detail.

WHAT YOU FILL IN
  TODO 1: Write your own list of user turns (at least 8) about one topic.
  TODO 2: Pick max_input_tokens so summarization fires at least twice.

RUN
  python -m homework.module_03.m3_1_homework
"""

import asyncio

from deepagents import create_deep_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

from hello_agent import model


def build_turns() -> list[str]:
    """Build a conversation about a fictional cloud migration project."""
    return [
        "I am planning an on-premises to cloud data migration project called "
        "Project Bluebird. Our fixed migration budget is $48,000.",
        "We need to move the customer and sales databases to the cloud without "
        "interrupting the daily reports used by the business team.",
        "What should we include in an initial inventory of databases, "
        "applications, and dependencies?",
        "The team includes a project manager, two data engineers, a cloud "
        "engineer, a database administrator, and a security specialist.",
        "How should the team identify sensitive data and decide what needs "
        "encryption before the migration?",
        "We plan to use a pilot migration for a small sales database before "
        "moving the remaining data.",
        "What checks should we run before starting the pilot to make sure "
        "the source database and network are ready?",
        "The migration will use an initial full copy followed by incremental "
        "updates until the final cutover.",
        "How can we compare the source and destination data after the initial "
        "copy? Suggest a few useful checks.",
        "The business team can allow a short maintenance window on a Saturday "
        "evening for the final cutover.",
        "What should the cutover checklist include, and who should approve "
        "the decision to switch?",
        "We also need a rollback plan in case the application cannot connect "
        "to the new database after cutover.",
        "What information should be included in a rollback plan, and how "
        "should the team test it?",
        "After the migration, the team will monitor database performance, "
        "cloud spending, and application errors for two weeks.",
        "How should we organize the handover to the operations team after "
        "those two weeks?",
        "Quick recap: what is the project name and the fixed migration budget "
        "I gave you at the beginning?",
    ]


MAX_INPUT_TOKENS = 6000

model.profile = {**model.profile, "max_input_tokens": MAX_INPUT_TOKENS}

agent = create_deep_agent(
    model=model,
    checkpointer=MemorySaver(),
    system_prompt="You are a helpful assistant. Keep every response to one sentence.",
)

THREAD: RunnableConfig = {"configurable": {"thread_id": "homework"}}
HISTORY_PATH = f"/conversation_history/{THREAD['configurable']['thread_id']}.md"


async def turn(message: str) -> str:
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=message)]},
        config=THREAD,
    )
    return result["messages"][-1].text


async def show_state(seen_cutoffs: set) -> bool:
    """Print state after a turn. Return True if a new summarization happened."""
    state = await agent.aget_state(THREAD)
    messages = state.values.get("messages", [])
    event = state.values.get("_summarization_event")
    print(f"  stored : {len(messages)} message(s) (raw history, never trimmed)")
    if not event:
        return False
    cutoff = event.get("cutoff_index", "?")
    is_new_event = cutoff not in seen_cutoffs
    seen_cutoffs.add(cutoff)
    tag = "  <-- NEW EVENT" if is_new_event else ""
    print(f"  model saw : summary + messages[{cutoff}:]  [SUMMARIZED]{tag}")
    return is_new_event


async def main() -> None:
    turns = build_turns()
    seen_cutoffs: set = set()
    event_count = 0
    for i, message in enumerate(turns, 1):
        print(f"\n{'─' * 50}")
        print(f"Turn {i}  User:  {message}")
        response = await turn(message)
        print(f"Turn {i}  Agent: {response}")
        if await show_state(seen_cutoffs):
            event_count += 1

    print(f"\nSummarization fired {event_count} time(s) across {len(turns)} turns.")
    if event_count < 2:
        print(
            "That's fewer than 2. Lower MAX_INPUT_TOKENS, or add more turns/detail, "
            "so it fires again before the conversation ends."
        )

    state = await agent.aget_state(THREAD)
    history_file = state.values.get("files", {}).get(HISTORY_PATH)
    if history_file:
        content = (
            history_file["content"] if isinstance(history_file, dict) else history_file
        )
        sections = content.count("## Summarized at")
        print(f"\n--- {HISTORY_PATH} ({sections} section(s)) ---")
        print(content)


if __name__ == "__main__":
    asyncio.run(main())
