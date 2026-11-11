from graph.nodes import summary_node

test_state = {
    "request_type": "summary",
    "subject": "Machine Learning",
    "note_path": "machine_learning/linear_regression.pdf"
}
result = summary_node(test_state)
print(result["response"])