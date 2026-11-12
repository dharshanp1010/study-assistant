from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import ToolMessage

def build_mcp_graph(session, llm, gemini_tools):

    # Bind MCP tools to Gemini
    model = llm.bind_tools(gemini_tools)
    # sends message to gemini
    async def agent_node(state):

        response = await model.ainvoke(state["messages"])

        print("\n[Agent] Gemini processed the request.")

        return {
            "messages": [response]
        }
    # exectues tools selected by gemini
    async def tool_node(state):

        last_message = state["messages"][-1]

        tool_messages = []

        for call in last_message.tool_calls:

            tool_name = call["name"]
            tool_arguments = call["args"]

            print(f"\n[ MCP ] Executing tool: {tool_name}")
            print(f"[ MCP ] Arguments: {tool_arguments}")

            try:

                # Execute the selected MCP tool
                result = await session.call_tool(
                    name=tool_name,
                    arguments=tool_arguments
                )

                # Extract text from MCP response
                tool_text = "\n".join(
                    item.text
                    for item in result.content
                    if getattr(item, "text", None) is not None
                )

                if result.isError:
                    tool_text = "MCP tool returned an error: " + tool_text

                if not tool_text:
                    tool_text = "The MCP tool returned no text content."
                print("\n[MCP TOOL RESULT]")
                print(tool_text)
                print("--------------------------")
            except Exception as e:

                tool_text = f"MCP execution failed: {str(e)}"

            # Return result to Gemini
            tool_messages.append(
                ToolMessage(
                    content=tool_text,
                    tool_call_id=call["id"]
                )
            )

        return {
            "messages": tool_messages
        }
    # decides the flow
    def route_after_agent(state):

        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "tools"

        return "end"

    #builder
    builder = StateGraph(MessagesState)

    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            "end": END
        }
    )

    builder.add_edge("tools", "agent")

    # Compile graph
    return builder.compile()