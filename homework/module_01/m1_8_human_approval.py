"""M1.8: Request human approval before an agent calls an action tool.

Create a simulated action tool that returns a confirmation without performing
a real-world action. Configure the agent to interrupt before that tool, then
review and resume the pending request. Test approval and rejection separately.

Run from the repository root in an interactive terminal:
    uv run --no-project python -m homework.module_01.m1_8_human_approval
"""

from deepagents import create_deep_agent
from langchain.agents.middleware import InterruptOnConfig
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from hello_agent import model


@tool
def simulate_action_tool(action: str) -> str:
    """Simulates performing an action by returning a confirmation string."""
    return f"Action '{action}' has been simulated."


SYSTEM_PROMPT = """You are an assistant that helps prepare Slack messages for clients.
Read each request carefully and ask for clarification if the recipient or message
is unclear. Before taking an action, propose it using simulate_action_tool so a
human can review it. Never claim that a real Slack message was sent: the tool
only simulates the action."""

INITIAL_PROMPT = (
    "Simulate sending a Slack message to client Alex: "
    "'The project update is ready for your review.'"
)
INTERRUPT_ON: dict[str, bool | InterruptOnConfig] = {
    "simulate_action_tool": {"allowed_decisions": ["approve", "edit", "reject"]}
}


def main():
    agent = create_deep_agent(
        model=model,
        tools=[simulate_action_tool],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver(),
        name="HumanApprovalSlackAgent",
        interrupt_on=INTERRUPT_ON,
    )
    config: RunnableConfig = {"configurable": {"thread_id": "m1-8-homework-approval"}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content": INITIAL_PROMPT}]},
        config=config,
        version="v2",
    )
    print(f"Initial request: {INITIAL_PROMPT}")

    while result.interrupts:
        pending = result.interrupts[0].value
        decisions = []
        for request in pending["action_requests"]:
            print(f"\nApproval required for {request['name']}:")
            print(request["args"])

            while True:
                choice = input(
                    "\nApprove, edit, or reject? (approve/edit/reject): "
                ).strip().lower()
                if choice in ("approve", "yes", "y"):
                    decisions.append({"type": "approve"})
                    break
                if choice in ("edit", "e"):
                    new_action = input("New simulated action: ").strip()
                    if not new_action:
                        print("The action cannot be empty.")
                        continue
                    edited_args = dict(request["args"])
                    edited_args["action"] = new_action
                    decisions.append(
                        {
                            "type": "edit",
                            "edited_action": {
                                "name": request["name"],
                                "args": edited_args,
                            },
                        }
                    )
                    break
                if choice in ("reject", "no", "n"):
                    decisions.append(
                        {"type": "reject", "message": "User rejected this action."}
                    )
                    break
                print("Please enter approve, edit, or reject.")

        result = agent.invoke(
            Command(resume={"decisions": decisions}),
            config=config,
            version="v2",
        )

    for message in result.value["messages"]:
        if getattr(message, "name", None) == "simulate_action_tool":
            print(f"\nTool result: {message.text}")
    print(f"\nAgent: {result.value['messages'][-1].text}")


if __name__ == "__main__":
    main()
