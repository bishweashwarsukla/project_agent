import os
from dotenv import load_dotenv
import google.generativeai as genai
import getpass
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import warnings
warnings.filterwarnings("ignore")
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from IPython.display import Image, display
import pprint
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Annotated, Literal
from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
import ast


def build_vector_db():

    def _set_env():
        load_dotenv()
        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass.getpass(
                "Enter your Google AI API key: "
            )

    _set_env()

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

    urls = [
        os.environ["moneycontrol"],
        os.environ["economic_times"],
        os.environ["yahoo_fin"],
    ]

    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=20
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Add to vectorDB
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embeddings,
    )
    retriever = vectorstore.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "retriver_stock_market_updates",
        "Search and return information about stocks in news whether they are good news or bad news , , bullish and bearnish newses as well",
    )

    tools = [retriever_tool]

    return retriever_tool, retriever, tools, vectorstore

def process_user_input(input_text, retriever_tool, retriever, tools, vectorstore):
    def _set_env():
        load_dotenv()
        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

    _set_env()

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # urls = [os.environ["moneycontrol"], os.environ["economic_times"], os.environ["yahoo_fin"]]
    # docs = [WebBaseLoader(url).load() for url in urls]
    # docs_list = [item for sublist in docs for item in sublist]

    # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=100, chunk_overlap=20)
    # doc_splits = text_splitter.split_documents(docs_list)

    # vectorstore = Chroma.from_documents(documents=doc_splits, collection_name="rag-chroma", embedding=embeddings)
    # retriever = vectorstore.as_retriever()

    # retriever_tool = create_retriever_tool(
    #     retriever,
    #     "retriver_stock_market_updates",
    #     "Search and return information about stocks in news, identifying positive or negative sentiment, and bullish or bearish indicators.",
    # )
    # tools = [retriever_tool]

    class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], add_messages]

    def grade_documents(state) -> Literal["generate", "rewrite"]:
        class Grade(BaseModel):
            binary_score: str = Field(description="Relevance score 'yes' or 'no'")

        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
        llm_with_tool = model.with_structured_output(Grade)

        prompt = PromptTemplate(
            template="Evaluate relevance of retrieved document to user question. Document:\n\n {context}\n\nUser question: {question}\nGive a binary score 'yes' or 'no' for relevance.",
            input_variables=["context", "question"],
        )

        chain = prompt | llm_with_tool
        question = state["messages"][0].content
        docs = state["messages"][-1].content

        scored_result = chain.invoke({"question": question, "context": docs})
        return "generate" if scored_result.binary_score == "yes" else "rewrite"

    def agent(state):
        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
        model = model.bind_tools(tools)
        return {"messages": [model.invoke(state["messages"])]}

    def rewrite(state):
        question = state["messages"][0].content
        prompt_msg = HumanMessage(
            content=f"Improve the question based on semantic intent:\n\n{question}\n\nReformulate as an improved question."
        )
        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
        return {"messages": [model.invoke([prompt_msg])]}

    def generate(state):
        docs = state["messages"][-1].content
        question = state["messages"][0].content
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
        rag_chain = prompt | llm | StrOutputParser()
        response = rag_chain.invoke({"context": docs, "question": question})
        return {"messages": [response]}

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent)
    workflow.add_node("retrieve", ToolNode([retriever_tool]))
    workflow.add_node("rewrite", rewrite)
    workflow.add_node("generate", generate)
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition, {"tools": "retrieve", END: END})
    workflow.add_conditional_edges("retrieve", grade_documents)
    workflow.add_edge("generate", END)
    workflow.add_edge("rewrite", "agent")
    graph = workflow.compile()

    inputs = {"messages": [("user", input_text)]}
    final_output = ""

    for output in graph.stream(inputs):
        for key, value in output.items():
            final_output = pprint.pformat(value, indent=2, width=80, depth=None)
    print(type(final_output))
    print(final_output)
    output_dict = ast.literal_eval(final_output)
    final_message = output_dict['messages'][0]
    print(type(final_message))
    print(final_message)
    return final_message

# Test the function
# print(process_user_input('Is Jio financial shares up today?'))
