from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY


def get_chat_model():

    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=GOOGLE_API_KEY
    )

    return model