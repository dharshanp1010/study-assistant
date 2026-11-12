
from graph.state import StudyAssistantState


# Create a sample MCQ request
state: StudyAssistantState = {
    "request_type": "mcq",
    "subject": "Machine Learning",
    "note_path": "linear_regression.pdf",
    "difficulty": "Intermediate",
    "num_questions": 5
}


for key, value in state.items():
    print(f"{key}: {value}")

