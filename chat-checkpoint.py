from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model("google_genai:gemini-2.5-flash-lite")


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[str]


def chatbot(state: State):

    print("Chatbot Node")

    response = llm.invoke(state.get("user_query"))

    state["llm_output"] = response.content

    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, What is 2+2"}))
print(updated_state)
