"""M1.4: Scope an agent to a topic using a system prompt.

Choose a subject and instruct the agent to redirect unrelated questions.
Test one question inside the subject and one outside it; print both answers.

Run from the repository root:
    uv run --no-project python -m homework.module_01.m1_4_system_prompt
"""

import warnings

from deepagents import create_deep_agent

from hello_agent import model

warnings.filterwarnings("ignore", category=DeprecationWarning)


def main():
    # TODO: Replace this with a prompt that describes your chosen subject
    # and explains what to do with unrelated questions.
    system_prompt = "You are an expert in quantum physics. If a question is unrelated to quantum physics, politely redirect the user to ask a relevant question."

    # TODO: Create an agent with model=model and system_prompt=system_prompt.
    agent = create_deep_agent(model=model, system_prompt=system_prompt, name="QuantumPhysicsAgent")
    
    # Then invoke it with two different user messages and print each answer.
    user_message_inside_subject = "What is the Heisenberg uncertainty principle?"
    user_message_outside_subject = "What is the capital of France?"

    for question in [user_message_inside_subject, user_message_outside_subject]:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )
        print(f"Question: {question}\nAnswer: {result["messages"][-1].text}\n")

  


if __name__ == "__main__":
    main()
