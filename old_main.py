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
# from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from IPython.display import Image, display
import pprint
from langchain_core.messages import BaseMessage

from langgraph.graph.message import add_messages
from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage

from langgraph.graph.message import add_messages
from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict

from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field

from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# def build_vector_db():

#     def _set_env():
#         load_dotenv()
#         if "GOOGLE_API_KEY" not in os.environ:
#             os.environ["GOOGLE_API_KEY"] = getpass.getpass(
#                 "Enter your Google AI API key: "
#             )

#     _set_env()

#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-pro",
#         temperature=0,
#         max_tokens=None,
#         timeout=None,
#         max_retries=2,
#         # other params...
#     )

#     urls = [
#         os.environ["moneycontrol"],
#         os.environ["economic_times"],
#         os.environ["yahoo_fin"],
#     ]

#     docs = [WebBaseLoader(url).load() for url in urls]
#     docs_list = [item for sublist in docs for item in sublist]

#     text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=100, chunk_overlap=20
#     )
#     doc_splits = text_splitter.split_documents(docs_list)

#     # Add to vectorDB
#     vectorstore = Chroma.from_documents(
#         documents=doc_splits,
#         collection_name="rag-chroma",
#         embedding=embeddings,
#     )
#     retriever = vectorstore.as_retriever()

#     retriever_tool = create_retriever_tool(
#         retriever,
#         "retriver_stock_market_updates",
#         "Search and return information about stocks in news whether they are good news or bad news , , bullish and bearnish newses as well",
#     )

#     tools = [retriever_tool]

#     return retriever_tool, retriever, tools, vectorstore





def process_user_input(input_text):
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
        # other params...
    )

    urls = [os.environ["moneycontrol"], os.environ["economic_times"], os.environ["yahoo_fin"]]



    urls = [os.environ["moneycontrol"], os.environ["economic_times"], os.environ["yahoo_fin"]]

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

    # results = vectorstore.similarity_search(
    #     "jio finance",
    #     k=2,
    #     # filter={"source": "tweet"},
    # )
    # for res in results:
    #     print(f"* {res.page_content} [{res.metadata}]")



    retriever_tool = create_retriever_tool(
        retriever,
        "retriver_stock_market_updates",
        "Search and return information about stocks in news whether they are good news or bad news , , bullish and bearnish newses as well",
    )

    tools = [retriever_tool]



    class AgentState(TypedDict):
        # The add_messages function defines how an update should be processed
        # Default is to replace. add_messages says "append"
        messages: Annotated[Sequence[BaseMessage], add_messages]




    class AgentState(TypedDict):
        # The add_messages function defines how an update should be processed
        # Default is to replace. add_messages says "append"
        messages: Annotated[Sequence[BaseMessage], add_messages]


    ### Edges


    def grade_documents(state) -> Literal["generate", "rewrite"]:
        """
        Determines whether the retrieved documents are relevant to the question.

        Args:
            state (messages): The current state

        Returns:
            str: A decision for whether the documents are relevant or not
        """

        #print("---CHECK RELEVANCE---")

        # Data model
        class grade(BaseModel):
            """Binary score for relevance check."""

            binary_score: str = Field(description="Relevance score 'yes' or 'no'")

        # LLM
        # model = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=True)
        model =  ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
        )

        # LLM with tool and validation
        llm_with_tool = model.with_structured_output(grade)

        # Prompt
        prompt = PromptTemplate(
            template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
            Here is the retrieved document: \n\n {context} \n\n
            Here is the user question: {question} \n
            If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
            input_variables=["context", "question"],
        )

        # Chain
        chain = prompt | llm_with_tool

        messages = state["messages"]
        last_message = messages[-1]

        question = messages[0].content
        docs = last_message.content

        scored_result = chain.invoke({"question": question, "context": docs})

        score = scored_result.binary_score

        if score == "yes":
            #print("---DECISION: DOCS RELEVANT---")
            return "generate"

        else:
            #print("---DECISION: DOCS NOT RELEVANT---")
            #print(score)
            return "rewrite"


    ### Nodes


    def agent(state):
        """
        Invokes the agent model to generate a response based on the current state. Given
        the question, it will decide to retrieve using the retriever tool, or simply end.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the agent response appended to messages
        """
        #print("---CALL AGENT---")
        messages = state["messages"]
        # model = ChatOpenAI(temperature=0, streaming=True, model="gpt-4-turbo")
        model =  ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )

        model = model.bind_tools(tools)
        response = model.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}


    def rewrite(state):
        """
        Transform the query to produce a better question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """

        #print("---TRANSFORM QUERY---")
        messages = state["messages"]
        question = messages[0].content

        msg = [
            HumanMessage(
                content=f""" \n 
        Look at the input and try to reason about the underlying semantic intent / meaning. \n 
        Here is the initial question:
        \n ------- \n
        {question} 
        \n ------- \n
        Formulate an improved question: """,
            )
        ]

        # Grader
        # model = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=True)
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )

        response = model.invoke(msg)
        return {"messages": [response]}


    def generate(state):
        """
        Generate answer

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """
        #print("---GENERATE---")
        messages = state["messages"]
        question = messages[0].content
        last_message = messages[-1]

        docs = last_message.content

        # Prompt
        prompt = hub.pull("rlm/rag-prompt")

        # LLM
        # llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )

        # Post-processing
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Chain
        rag_chain = prompt | llm | StrOutputParser()

        # Run
        response = rag_chain.invoke({"context": docs, "question": question})
        return {"messages": [response]}


    #print("*" * 20 + "Prompt[rlm/rag-prompt]" + "*" * 20)
    prompt = hub.pull("rlm/rag-prompt").pretty_print()  # Show what the prompt looks like




    # Define a new graph
    workflow = StateGraph(AgentState)

    # Define the nodes we will cycle between
    workflow.add_node("agent", agent)  # agent
    retrieve = ToolNode([retriever_tool])
    workflow.add_node("retrieve", retrieve)  # retrieval
    workflow.add_node("rewrite", rewrite)  # Re-writing the question
    workflow.add_node(
        "generate", generate
    )  # Generating a response after we know the documents are relevant
    # Call agent node to decide to retrieve or not
    workflow.add_edge(START, "agent")

    # Decide whether to retrieve
    workflow.add_conditional_edges(
        "agent",
        # Assess agent decision
        tools_condition,
        {
            # Translate the condition outputs to nodes in our graph
            "tools": "retrieve",
            END: END,
        },
    )

    # Edges taken after the `action` node is called.
    workflow.add_conditional_edges(
        "retrieve",
        # Assess agent decision
        grade_documents,
    )
    workflow.add_edge("generate", END)
    workflow.add_edge("rewrite", "agent")

    # Compile
    graph = workflow.compile()


    try:
        display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        pass



    inputs = {
        "messages": [
            ("user", input_text),
        ]
    }
    # for output in graph.stream(inputs):
    #     for key, value in output.items():
    #         pprint.pprint(f"Output from node '{key}':")
    #         pprint.pprint("---")
    #         pprint.pprint(value, indent=2, width=80, depth=None)
    #     pprint.pprint("\n---\n")

    #original output 
    # output_data = ""
    # for output in graph.stream(inputs):
    #     for key, value in output.items():
    #         output_data += f"\n**Output from node '{key}':**\n---\n"
    #         output_data += f"{pprint.pformat(value, indent=2, width=80, depth=None)}\n"
    #         output_data += "\n---\n"
    
    # return output_data

    import pprint
    import ast
    # Initialize final_output as an empty dictionary string
    final_output = ""

    for output in graph.stream(inputs):
        for key, value in output.items():
            # Only store the latest dictionary in final_output, without extra text
            final_output = pprint.pformat(value, indent=2, width=80, depth=None)

    # Now final_output will only contain the dictionary as a formatted string
    # print('original final output')
    # Return only the final output after the loop completes
    # Convert the string to a dictionary
    # print(type(final_output))
    print(final_output)
    output_dict = ast.literal_eval(final_output)

    # print("converted coutput")
    # Extract the message and print it
    final_message = output_dict['messages'][0]
    # print(type(final_message))
    print(final_message)
    
    return final_message

process_user_input('is bajaj auto a good stock')
   

    # for output in graph.stream(inputs):
    #     for key, value in output.items():
    #         # Assuming value is a dictionary, extract its values
    #         if isinstance(value, dict):
    #             final_output += "\n".join(str(v) for v in value.values())
    #         else:
    #             final_output += str(value)  # Handle non-dictionary values
                
    #         final_output += "\n---\n"  # Separator for readability

    # return final_output
