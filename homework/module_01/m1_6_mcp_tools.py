"""M1.6: Connect an agent to a different MCP server.

Choose a public MCP server, fetch its tools, and allow only the ones you need.
Ask a question relevant to that server. Check a server's trustworthiness and
privacy policy before sending it data.

Run from the repository root:
    uv run --no-project python -m homework.module_01.m1_6_mcp_tools
"""

import asyncio

from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from hello_agent import model


async def build_tools():
    # TODO: Configure a streamable_http MCP client with your chosen server.
    # Await client.get_tools(), filter by tool name, and return the list.
    client = MultiServerMCPClient({
            "deepwiki": {
                "transport": "streamable_http",
                "url": "https://mcp.deepwiki.com/mcp",
            }
        })
    
    tools = await client.get_tools()
    ALLOWED = {"ask_wiki_question"}
    selected_tools = [t for t in tools if t.name in ALLOWED]
    if not selected_tools:
        raise RuntimeError(
            f"No allowed DeepWiki tools found. Available: {[t.name for t in tools]}"
        )
    return selected_tools
    # raise NotImplementedError("Connect to your MCP server and filter its tools.")


QUESTION = (
    "Use the DeepWiki tool to ask the langchain-ai/deepagents GitHub repo: "
    "what filesystem backends does deepagents support?"
)


async def main():
    # TODO: Get the filtered tools, create an agent, and use await agent.ainvoke
    # with a question suited to the server. Print the final answer.
    tools = await build_tools()
    agent = create_deep_agent(model=model, tools=tools)
    result = await agent.ainvoke({"messages": [{"role": "user", "content": QUESTION}]})
    print(result["messages"][-1].text)



if __name__ == "__main__":
    asyncio.run(main())
