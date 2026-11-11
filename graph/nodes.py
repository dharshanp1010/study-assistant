from graph.state import StudyAssistantState
from services.qa_service import create_qa_chain
from pathlib import Path

from services.summary_service import (summarize_note,summarize_pdf_note)
from services.quiz_service import (generate_mcq_quiz ,generate_descriptive_quiz)


def qa_node(state: StudyAssistantState):
# Check whether required inputs are available
    required_fields = ["subject", "question"]

    missing_fields = [
        field for field in required_fields
        if not state.get(field)
    ]

    if missing_fields:
        raise ValueError(f"Missing required inputs: {missing_fields}")

    # Create the existing QA chain
    qa_chain = create_qa_chain()

    # Execute the chain , use intermediate if not mentioned
    answer = qa_chain.invoke({
        "level": state.get("level", "Intermediate"),
        "topic": state["subject"],
        "question": state["question"]
    })

    # Return the result as a state update
    return {
        "response": answer
    }


#summary node for study material
def summary_node(state: StudyAssistantState):
    required_fields = ["subject", "note_path"]

    for field in required_fields:
        if not state.get(field):
            raise ValueError(f"Missing required input: {field}")
    # Get the file extension
    file_extension = Path(state["note_path"]).suffix.lower()

    # Select the correct summary service
    if file_extension in [".txt", ".md"]:

        summary = summarize_note(
            relative_path=state["note_path"],
            subject=state["subject"]
        )

    elif file_extension == ".pdf":

        summary = summarize_pdf_note(
            relative_path=state["note_path"],
            subject=state["subject"]
        )

    else:
        raise ValueError(
            "Unsupported file format. Use TXT, Markdown, or PDF."
        )

    # Return the summary as a state update
    return {
        "response": summary
    }

# mcq quiz node
def mcq_node(state: StudyAssistantState):
    # Generate the MCQ quiz
    quiz = generate_mcq_quiz(
        relative_path=state["note_path"],
        subject=state["subject"],
        num_questions=state["num_questions"],
        difficulty=state["difficulty"]
    )

    # Return the structured quiz as a state update
    return {
        "response": quiz
    }

def descriptive_node(state : StudyAssistantState):

    quiz = generate_descriptive_quiz(
        relative_path=state["note_path"],
        subject=state["subject"],
        num_questions=state["num_questions"],
        difficulty=state["difficulty"],
        marks_per_question=state["marks_per_question"]
    )
    return{
        "response":quiz
    }