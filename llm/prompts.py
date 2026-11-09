from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field




study_question_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a personal AI study assistant.

        Your job is to help students understand technical concepts.

        Follow these instructions:
        1. Explain the concept clearly.
        2. Start with the fundamental idea.
        3. Include a practical example.
        4. Explain important technical terms.
        5. Mention real-world applications where relevant.
        6. End with a short summary.

        Adapt the explanation to the student's knowledge level:
        {level}
        """
    ),
    (
        "human",
        """
        Subject: {topic}

        Question: {question}
        """
    )
])

note_summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an academic study notes summarizer.

        Summarize the supplied study material accurately.

        Follow this structure:

        1. Overview
        2. Important Concepts
        3. Important Terms
        4. Examples and Applications
        5. Quick Revision

        Important rules:
        - Base your summary on the supplied notes.
        - Do not invent facts.
        - Preserve important equations and definitions.
        - Use clear language suitable for an intermediate student.
        """
    ),
    (
        "human",
        """
        Subject: {subject}

        Study Notes:

        {note_content}
        """
    )
])

#schema
class MCQQuestion(BaseModel):
    question: str = Field(description="The quiz question")
    options: list[str] = Field(description="Exactly four answer options"
    )
    correct_answer: str = Field(description="The exact correct option"
    )
    explanation: str = Field(description="Why the answer is correct"
    )


class MCQQuiz(BaseModel):
    title: str = Field(description="Quiz title")
    questions: list[MCQQuestion]


mcq_parser = PydanticOutputParser(pydantic_object=MCQQuiz)

#quiz prompt
mcq_quiz_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an academic quiz generator.

        Generate multiple-choice questions using only
        the supplied study notes.

        Rules:
        1. Generate exactly the requested number of questions.
        2. Every question must have exactly four options.
        3. Only one option must be correct.
        4. Avoid duplicate questions.
        5. Match the requested difficulty level.
        6. Provide a clear explanation for every answer.
        7. Do not introduce concepts absent from the notes.

        Return the output in the required format:
        {format_instructions}
        """
    ),
    (
        "human",
        """
        Subject: {subject}
        Difficulty: {difficulty}
        Number of questions: {num_questions}

        Study notes:
        {note_content}
        """
    )
])

#schema descriptive quiz
class DescriptiveQuestion(BaseModel):
    question: str = Field(
        description="The descriptive question"
    )

    marks: int = Field(
        description="Maximum marks for this question"
    )

    expected_answer: str = Field(
        description="A model answer for the question"
    )

    key_points: list[str] = Field(
        description="Important points expected in the answer"
    )


class DescriptiveQuiz(BaseModel):
    title: str = Field(
        description="Title of the descriptive quiz"
    )

    questions: list[DescriptiveQuestion]


descriptive_parser = PydanticOutputParser(
    pydantic_object=DescriptiveQuiz
)
# prompt descriptive quiz
descriptive_quiz_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an academic descriptive quiz generator.

        Generate descriptive questions using only the
        supplied study notes.

        Follow these rules:

        1. Generate exactly the requested number of questions.
        2. Match the requested difficulty.
        3. Assign the specified marks to every question.
        4. Provide a clear and accurate expected answer.
        5. Include important key points for evaluation.
        6. Avoid duplicate questions.
        7. Do not introduce concepts absent from the notes.
        8. Questions should test understanding, not only memory.

        Return the result in the required format:

        {format_instructions}
        """
    ),
    (
        "human",
        """
        Subject: {subject}
        Difficulty: {difficulty}
        Number of questions: {num_questions}
        Marks per question: {marks_per_question}

        Study notes:
        {note_content}
        """
    )
])