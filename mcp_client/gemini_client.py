import asyncio
import sys
from pathlib import Path
from typing import Any, Optional

from pydantic import Field, create_model

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_core.tools import StructuredTool
from langchain_core.messages import (SystemMessage,HumanMessage,ToolMessage)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from llm.model import get_chat_model
SERVER_PATH = PROJECT_ROOT / "mcp_server" / "server.py"


async def main():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        cwd=str(PROJECT_ROOT)
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()
            print("Connected to MCP Server!")

            # Get MCP tools
            tools_result = await session.list_tools()

            gemini_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema
                    }
                }
                for tool in tools_result.tools
            ]

            llm = get_chat_model().bind_tools(gemini_tools)

            # Maintain conversation history
            messages = [
                SystemMessage(
                    content="You are a helpful study assistant. "
                    "Use available tools when required. "
                    "Never invent file paths or arguments."
                )
            ]

            print("\n===== GEMINI STUDY ASSISTANT =====")

            while True:

                user_input = input("\nYou: ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    break

                #user message
                messages.append(HumanMessage(content=user_input))

                # Ask Gemini
                response = await llm.ainvoke(messages)
                messages.append(response)

                if response.tool_calls:

                    for call in response.tool_calls:

                        print(f"\nCalling MCP tool: {call['name']}")

                        result = await session.call_tool(
                            name=call["name"],
                            arguments=call["args"]
                        )

                        tool_text = "\n".join(
                            item.text
                            for item in result.content
                            if hasattr(item, "text")
                        )

                        if result.isError:
                            tool_text = "Tool execution failed: " + tool_text

                        
                        messages.append(
                            ToolMessage(
                                content=tool_text,
                                tool_call_id=call["id"]
                            )
                        )

                    # Gemini generates answer
                    final_response = await llm.ainvoke(messages)

                    messages.append(final_response)

                    print("\nAssistant:", final_response.content)

                else:
                    print("\nAssistant:", response.content)


if __name__ == "__main__":
    asyncio.run(main())

