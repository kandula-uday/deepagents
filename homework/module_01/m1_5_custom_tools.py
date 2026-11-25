"""M1.5: Give an agent a custom tool.

Choose a topic, store a small collection of facts, and create a lookup tool.
Give the agent a persona and ask it to use the tool before answering.

Run from the repository root:
    uv run --no-project python -m homework.module_01.m1_5_custom_tools
"""

from deepagents import create_deep_agent
from langchain_core.tools import tool

from hello_agent import model


# TODO: Add @tool to your own function. Give it a descriptive docstring,
# at least one argument, and a string return value from your fact lookup.
@tool("lookup_fact", description="Look up a fact from a small collection of facts.")
def lookup_fact(fact_key: str) -> str:
    facts = {
        "Python": "Python is a high-level programming language.",
        "AI": "AI stands for Artificial Intelligence.",
        "Earth": "Earth is the third planet from the Sun."
    }
    return facts.get(fact_key, "Fact not found.")


def main():
    # TODO: Create an agent with your tool and a system prompt telling it
    # when to call the tool. Ask a question that requires the lookup.
    system_prompt = "you are an expert_agent. Use the lookup_fact tool to answer questions requiring factual information."
    agent = create_deep_agent(
        model=model,
        system_prompt=system_prompt,
        tools=[lookup_fact],
        name="ExpertAgent"
    )

    user_message = "Tell me something about Python."
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
    )
    print(f"Question: {user_message} \n Answer: {result['messages'][-1].text}\n")


if __name__ == "__main__":
    main()
