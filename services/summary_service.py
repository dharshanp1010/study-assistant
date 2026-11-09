from langchain_core.output_parsers import StrOutputParser

from llm.model import get_chat_model
from llm.prompts import note_summary_prompt
from services.notes_service import (read_note,read_pdf_note)


def summarize_note(relative_path: str, subject: str):

    #  Read the note
    note_content = read_note(relative_path)
    model = get_chat_model()
    output_parser = StrOutputParser()

    #  Create the  chain and invoke
    summary_chain = (note_summary_prompt| model | output_parser )
    summary = summary_chain.invoke({
        "subject": subject,
        "note_content": note_content
    })

    return summary

def summarize_pdf_note(relative_path: str, subject: str):

    note_content = read_pdf_note(relative_path)
    model = get_chat_model()
    output_parser = StrOutputParser()

    summary_chain = (note_summary_prompt | model | output_parser)
    summary = summary_chain.invoke({
        "subject": subject,
        "note_content": note_content
    })

    return summary