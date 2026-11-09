from langchain_core.output_parsers import StrOutputParser

from llm.model import get_chat_model
from llm.prompts import study_question_prompt


def create_qa_chain():

    model = get_chat_model()

    output_parser = StrOutputParser()

    qa_chain = (
        study_question_prompt| model| output_parser
    )

    return qa_chain