"""M1.7: Explore thread memory and checkpoint scope.

Choose a fact other than a favourite colour. Show:
1. A follow-up in the same thread can use the earlier message.
2. A different thread has no access to the first thread's conversation.
3. A new agent with a fresh MemorySaver has no saved state, even if it uses
   the first thread's ID.
Print the responses from all three comparisons.

Run from the repository root:
    uv run --no-project python -m homework.module_01.m1_7_memory_threads
"""

from deepagents import create_deep_agent
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

from hello_agent import model


def main():
    # TODO: Create an agent with MemorySaver() and two thread configurations.
    # Share your fact in the first thread, then ask for it in that thread,
    # the second thread, and a new agent's fresh checkpointer.
    agent = create_deep_agent(
        model=model,
        checkpointer=MemorySaver(),
        name="ThreadMemoryAgent"
    )
    thread_1_id: RunnableConfig = { "configurable": {"thread_id": "thread-a"} }  
    
    thread_2_id: RunnableConfig = { "configurable": {"thread_id": "thread-b"} }  

    # Share a fact in the first thread
    user_fact = "My favourite programming language is Python."
    
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_fact
                    
                }
            ]
            
        },
        config= thread_1_id,
    )
    
    print(f"Thread 1 fact shared: {user_fact}")
    print(f"Thread 1 initial: {result['messages'][-1].text}")

    # Follow-up in the same thread
    follow_up_message = "What is my favourite programming language?"
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": follow_up_message,
                   
                }
            ]
           
        },
        config= thread_1_id,
    )
    print(f"Thread 1 follow-up question: {follow_up_message}")
    print(f"Thread 1 follow-up: {result['messages'][-1].text}")

    # Ask in a different thread
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": follow_up_message,
                    
                }
            ]
            
        },
        config= thread_2_id,
    )
    print(f"Thread 2 question: {follow_up_message} the result shopuld be different")
    print(f"Thread 2: {result['messages'][-1].text}")

    # New agent with fresh MemorySaver
    new_agent = create_deep_agent(
        model=model,
        checkpointer=MemorySaver(),
        name="FreshAgent"
    )
    result = new_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": follow_up_message,
                    
        
                }
            ]
            
        },
        config= thread_1_id,
    )
    print("\nFresh agent, thread_a's thread_id (should NOT know):")
    print(
            "Same thread_id, but a different MemorySaver instance has no record "
            "of it: persistence is scoped to the checkpointer, not the thread_id "
            "string alone."
        )
    print(f"Fresh agent: {result['messages'][-1].text}")


if __name__ == "__main__":
    main()
