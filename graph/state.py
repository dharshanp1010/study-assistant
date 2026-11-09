from typing import TypedDict , Optional ,Any

from typing import TypedDict, Optional, Any


class StudyAssistantState(TypedDict, total=False):

    request_type: str

    subject: str

    question: str

    level: str

    note_path: str

    difficulty: str

    num_questions: int

    marks_per_question: int

    response: Any

    error: Optional[str]