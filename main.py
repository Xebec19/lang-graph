from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):

    return {"messages": ["Hi, This is a message from Chatbot Node"]}


def samplenode(state: State):
    return {"messages": ["Sample Message Appended"]}


graph_builder = StateGraph(State)  # created graph

graph_builder.add_node("chatbot", chatbot)  # added node to graph
graph_builder.add_node("samplenode", samplenode)  # add another node to graph


def main():
    print("Hello from lang-graph!")


if __name__ == "__main__":
    main()
