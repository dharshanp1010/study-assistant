from langgraph.graph import StateGraph,START,END
from graph.state import StudyAssistantState
from graph.nodes import (qa_node,mcq_node,descriptive_node,summary_node)
from graph.router import route_request

workflow = StateGraph(StudyAssistantState)
workflow.add_node("qa", qa_node)

workflow.add_node("summary", summary_node)

workflow.add_node("mcq", mcq_node)

workflow.add_node("descriptive", descriptive_node)

#flow
workflow.add_conditional_edges(
    START,
    route_request, {
    "qa": "qa",
        "summary": "summary",
        "mcq": "mcq",
        "descriptive": "descriptive"
})
# Connect every node to END
workflow.add_edge("qa", END)
workflow.add_edge("summary", END)
workflow.add_edge("mcq", END)
workflow.add_edge("descriptive", END)

#compile
study_assistant_graph = workflow.compile()
