
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_core.messages import (SystemMessage,HumanMessage)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from llm.model import get_chat_model
from graph.mcp_workflow import build_mcp_graph

SERVER_PATH = PROJECT_ROOT / "mcp_server" / "server.py"


def display_response(content):

    if isinstance(content, str):
        print(content)
        return

    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            print(item["text"])

        elif hasattr(item, "text"):
            print(item.text)

        else:
            print(item)


async def main():

    #  Configure MCP server
    server_params = StdioServerParameters(command=sys.executable,args=[str(SERVER_PATH)],cwd=str(PROJECT_ROOT))
    #  Start MCP server and connect client
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("Connected to MCP Server!")

            #  Discover  MCP tools
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

            print("\nAvailable MCP tools:")

            for tool in tools_result.tools:
                print(f"- {tool.name}")

            #  Initialize Gemini
            llm = get_chat_model()

            #  Build LangGraph workflow
            app = build_mcp_graph(session,  llm,gemini_tools)
            print("\n===== LANGGRAPH + GEMINI + MCP =====")


            messages = [
                SystemMessage(
                    content=(
                        "You are a helpful Personal AI Study Assistant. "

                        "Use the available MCP tools for study questions, "
                        "note summaries, MCQ quizzes and descriptive quizzes. "

                        "IMPORTANT INSTRUCTIONS: "

                        "1. When a user asks a study question, use ask_question "
                        "and provide the actual explanation returned by the tool. "

                        "2. After receiving a tool result, carefully read it "
                        "and include its useful content in your final response. "

                        "3. Never respond with only a generic acknowledgement "
                        "such as 'I have explained this' or 'Let me know if you "
                        "need anything else'. "

                        "4. For summaries and quizzes, present the actual "
                        "summary, questions, answers and explanations returned "
                        "by the tools. "

                        "5. If multiple tools are called, combine their actual "
                        "results into one well-structured response. "

                        "6. If a tool returns an error, clearly explain the error. "

                        "7. Ask the user for missing required information. "
                        "Never invent file paths or tool arguments. "

                        "8. Give clear, educational explanations with examples "
                        "when the tool provides them."
                    )
                )
            ]


            # Interactive conversation
            while True:

                user_input = input("\nYou: ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                messages.append(
                    HumanMessage(content=user_input)
                )

                try:

                    result = await app.ainvoke(
                        {"messages": messages},
                        config={"recursion_limit": 15}
                    )

                    messages = result["messages"]

                    print("\nAssistant:")

                    display_response(messages[-1].content)

                except Exception as e:

                    print(f"\nWorkflow error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
