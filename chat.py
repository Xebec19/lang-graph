from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model("google_genai:gemini-2.5-flash-lite")


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[str]


def chatbot(state: State):
    response = llm.invoke(state.get("user_query"))

    state["llm_output"] = response.content

    return {"messages": [response]}


def evaluate_response(state: State):
    if True:
        return ""

    return ""


graph_builder = StateGraph(State)
