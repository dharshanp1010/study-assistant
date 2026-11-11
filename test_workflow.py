
from graph.workflow import study_assistant_graph

# Input state test 
test_state = {
    "request_type": "summary",
    "subject": "Machine Learning",
    "note_path": "machine_learning/linear_regression.pdf"
}

# Execute graph
result = study_assistant_graph.invoke(test_state)


print(result["response"])
