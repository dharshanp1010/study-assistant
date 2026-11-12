
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# MCP server configuration
SERVER_PATH = PROJECT_ROOT / "mcp_server" / "server.py"

server_params = StdioServerParameters(
    command=sys.executable,
    args=[str(SERVER_PATH)],
    cwd=str(PROJECT_ROOT)
)


# Function to display MCP tool results
def display_result(result):

    if result.isError:
        print("\nTool execution failed.")
        for content in result.content:
            if content.type == "text":
                print(content.text)
        return

    for content in result.content:
        if content.type == "text":
            print(content.text)


# Main client function
async def main():

    print("Connecting to MCP server...")

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize connection
            await session.initialize()

            print("\nConnected successfully!")

            # Discover tools
            tools_result = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in tools_result.tools:
                print(f"- {tool.name}")

            # Application menu
            while True:

                print("\n========== PERSONAL AI STUDY ASSISTANT ==========")
                print("1. Ask a Question")
                print("2. Summarize Study Notes")
                print("3. Generate MCQ Quiz")
                print("4. Generate Descriptive Quiz")
                print("5. Exit")

                choice = input("\nEnter your choice: ").strip()

                # Option 1 qa
                if choice == "1":

                    subject = input("Enter subject: ")
                    question = input("Enter question: ")
                    level = input(
                        "Enter difficulty (Beginner/Intermediate/Advanced): "
                    )

                    result = await session.call_tool(
                        name="ask_question",
                        arguments={
                            "subject": subject,
                            "question": question,
                            "level": level
                        }
                    )

                    display_result(result)

                # Option 2 Summarize notes
                elif choice == "2":

                    subject = input("Enter subject: ")
                    note_path = input("Enter note path: ")

                    result = await session.call_tool(
                        name="summarize_notes",
                        arguments={
                            "subject": subject,
                            "note_path": note_path
                        }
                    )

                    display_result(result)

                # Option 3 MCQ quiz
                elif choice == "3":

                    subject = input("Enter subject: ")
                    note_path = input("Enter note path: ")

                    num_questions = int(
                        input("Enter number of questions: ")
                    )

                    difficulty = input(
                        "Enter difficulty (Easy/Intermediate/Advanced): "
                    )

                    result = await session.call_tool(
                        name="generate_mcq",
                        arguments={
                            "subject": subject,
                            "note_path": note_path,
                            "num_questions": num_questions,
                            "difficulty": difficulty
                        }
                    )

                    display_result(result)

                # Option 4 descriptive quiz
                elif choice == "4":

                    subject = input("Enter subject: ")
                    note_path = input("Enter note path: ")

                    num_questions = int(
                        input("Enter number of questions: ")
                    )

                    difficulty = input(
                        "Enter difficulty (Easy/Intermediate/Advanced): "
                    )

                    marks = int(
                        input("Enter marks per question: ")
                    )

                    result = await session.call_tool(
                        name="generate_descriptive_quiz_tool",
                        arguments={
                            "subject": subject,
                            "note_path": note_path,
                            "num_questions": num_questions,
                            "difficulty": difficulty,
                            "marks_per_question": marks
                        }
                    )

                    display_result(result)

                # Option 5 Exit
                elif choice == "5":

                    print("\nExiting Study Assistant...")
                    break

                else:
                    print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    asyncio.run(main())
