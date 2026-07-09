from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm = init_chat_model("google_genai:gemini-2.5-flash-lite")


def chatbot(state: MessagesState):

    response = llm.invoke(state["messages"])

    return {"messages": [response]}


graph_builder = StateGraph(MessagesState)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


def compile_graph_with_checkpointer(checkpointer):

    return graph_builder.compile(checkpointer=checkpointer)


DB_URI = "mongodb://admin:admin@localhost:27017/lg?authSource=admin"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer)

    config = {"configurable": {"thread_id": "123"}}

    updated_state = graph_with_checkpointer.invoke(
        MessagesState({"messages": [{"role": "user", "content": "What is my name ?"}]}),
        config,
    )

    print(updated_state["messages"][-1].content)
