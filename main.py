from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model("google_genai:gemini-2.5-flash-lite")

class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}


def samplenode(state: State):
    return {"messages": ["Sample Message Appended"]}


graph_builder = StateGraph(State)  # created graph

graph_builder.add_node("chatbot", chatbot)  # added node to graph
graph_builder.add_node("samplenode", samplenode)  # add another node to graph

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi, my name is Rohan Thakur"]}))
print("updated_state", updated_state)


def main():
    print("Hello from lang-graph!")


if __name__ == "__main__":
    main()
