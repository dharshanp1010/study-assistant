
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


sys.path.insert(0, str(PROJECT_ROOT))

# Import MCP and existing services
from mcp.server.fastmcp import FastMCP
from services.qa_service import create_qa_chain
from services.summary_service import ( summarize_note,summarize_pdf_note)
from services.quiz_service import (generate_mcq_quiz, generate_descriptive_quiz)

# Create MCP server
mcp = FastMCP("Personal Study Assistant")


# Tool 1: question and answer
@mcp.tool()
def ask_question(subject: str,question: str,level: str = "Intermediate") -> str:
    """
    Answer a study-related question.
    """
    qa_chain = create_qa_chain()

    answer = qa_chain.invoke({
        "level": level,
        "topic": subject,
        "question": question
    })

    return str(answer)


# Tool 2: Summarize 
@mcp.tool()
def summarize_notes(subject: str,note_path: str) -> str:
    """
    Summarize study notes from PDF, TXT or Markdown files.
    """

    # Get file extension
    file_extension = Path(note_path).suffix.lower()

    # Validate file format
    if file_extension not in [".pdf", ".txt", ".md"]:
        raise ValueError(
            "Unsupported file format. Use PDF, TXT or Markdown."
        )

    # Resolve file path
    file_path = (PROJECT_ROOT / note_path).resolve()

    # Prevent access outside project directory
    if not file_path.is_relative_to(PROJECT_ROOT.resolve()):
        raise ValueError("File path is outside the project directory.")

    # Check whether file exists
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Study material not found: {note_path}"
        )

    # Select the summarization service
    if file_extension in [".txt", ".md"]:
        summary = summarize_note(
            relative_path=str(file_path),
            subject=subject
        )
    else:
        summary = summarize_pdf_note(
            relative_path=str(file_path),
            subject=subject
        )

    return str(summary)

# Tool 3: Generate MCQ quiz
@mcp.tool()
def generate_mcq(subject: str,note_path: str,num_questions: int = 5,difficulty: str = "Intermediate") -> str:
    """
    Generate multiple-choice questions from study notes.
    """

    # Validate file extension
    file_extension = Path(note_path).suffix.lower()

    if file_extension not in [".pdf", ".txt", ".md"]:
        raise ValueError(
            "Unsupported file format. Use PDF, TXT or Markdown."
        )

    # Resolve and validate file path
    file_path = (PROJECT_ROOT / note_path).resolve()

    if not file_path.is_relative_to(PROJECT_ROOT.resolve()):
        raise ValueError(
            "File path is outside the project directory."
        )

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Study material not found: {note_path}"
        )

    # Call existing MCQ service
    quiz = generate_mcq_quiz(
        relative_path=str(file_path),
        subject=subject,
        num_questions=num_questions,
        difficulty=difficulty
    )

    return str(quiz)


# Tool 4: Generate descriptive quiz
@mcp.tool()
def generate_descriptive_quiz_tool(subject: str,note_path: str,num_questions: int = 5,difficulty: str = "Intermediate",
    marks_per_question: int = 5
) -> str:
    """
    Generate descriptive questions and answers from study notes.
    """

    # Validate file format
    file_extension = Path(note_path).suffix.lower()

    if file_extension not in [".pdf", ".txt", ".md"]:
        raise ValueError(
            "Unsupported file format. Use PDF, TXT or Markdown."
        )

    # Resolve file path
    file_path = (PROJECT_ROOT / note_path).resolve()

    # Prevent access outside project directory
    if not file_path.is_relative_to(PROJECT_ROOT.resolve()):
        raise ValueError(
            "File path is outside the project directory."
        )

    # Check file existence
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Study material not found: {note_path}"
        )

    # Call existing descriptive quiz service
    quiz = generate_descriptive_quiz(
        relative_path=str(file_path),
        subject=subject,
        num_questions=num_questions,
        difficulty=difficulty,
        marks_per_question=marks_per_question
    )

    return str(quiz)

# Start MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")