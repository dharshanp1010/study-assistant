from pathlib import Path
from llm.model import get_chat_model
from llm.prompts import (mcq_quiz_prompt,mcq_parser,descriptive_quiz_prompt,descriptive_parser)
from services.notes_service import (read_note,read_pdf_note)



def generate_mcq_quiz(
    relative_path: str,
    subject: str,
    num_questions: int = 5,
    difficulty: str = "Intermediate"
):
    allowed_difficulties = ["Easy","Intermediate", "Advanced"]

    file_extension = Path(relative_path).suffix.lower()

    if file_extension == ".pdf":
        note_content = read_pdf_note(relative_path)

    elif file_extension in [".txt", ".md"]:
        note_content = read_note(relative_path)

    else:
        raise ValueError("Unsupported note format.")

    model = get_chat_model()

    quiz_chain = (
        mcq_quiz_prompt
        | model
        | mcq_parser
    )

    quiz = quiz_chain.invoke({
        "subject": subject,
        "difficulty": difficulty,
        "num_questions": num_questions,
        "note_content": note_content,
        "format_instructions": mcq_parser.get_format_instructions()
    })


    return quiz


def generate_descriptive_quiz(
    relative_path: str,
    subject: str,
    num_questions: int = 5,
    difficulty: str = "Intermediate",
    marks_per_question: int = 5
):

    if marks_per_question < 1 or marks_per_question > 20:
        raise ValueError(
            "Marks per question must be between 1 and 20."
        )

    file_extension = Path(relative_path).suffix.lower()

    if file_extension == ".pdf":
        note_content = read_pdf_note(relative_path)

    elif file_extension in [".txt", ".md"]:
        note_content = read_note(relative_path)

    else:
        raise ValueError("Unsupported note format.")

    model = get_chat_model()

    quiz_chain = (
        descriptive_quiz_prompt
        | model
        | descriptive_parser
    )

    quiz = quiz_chain.invoke({
        "subject": subject,
        "difficulty": difficulty,
        "num_questions": num_questions,
        "marks_per_question": marks_per_question,
        "note_content": note_content,
        "format_instructions":
            descriptive_parser.get_format_instructions()
    })


    for question in quiz.questions:
        if question.marks != marks_per_question:
            raise ValueError(
                "Generated question has an incorrect mark value."
            )

    return quiz