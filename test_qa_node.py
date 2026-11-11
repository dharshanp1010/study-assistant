
from graph.nodes import qa_node


test_state = {
    "request_type": "qa",
    "subject": "Machine Learning",
    "question": "What is Linear Regression?",
    "level": "Intermediate"
}


result = qa_node(test_state)


print(result["response"])
