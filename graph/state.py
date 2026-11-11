from typing import TypedDict , Optional ,Any

#create the state
class StudyAssistantState(TypedDict, total=False):

    request_type: str
    subject: str
    question: str
    # for explaination
    level: str
    # study material
    note_path: str
    # quiz 
    difficulty: str
    num_questions: int
    marks_per_question: int
    #output flow
    response: Any
    # error information
    error: Optional[str]