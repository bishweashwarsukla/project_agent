import streamlit as st
from main import process_user_input, build_vector_db, load_vector_db

# Initialize session state to keep track of whether the vector DB has been created
if "vector_db_created" not in st.session_state:
    st.session_state.vector_db_created = False

st.title("Stock & Finance Query Assistant")


try:
    retriever_tool, retriever, tools, vectorstore = load_vector_db()
    st.session_state.retriever_tool = retriever_tool
    st.session_state.retriever = retriever
    st.session_state.tools = tools
    st.session_state.vectorstore = vectorstore
    st.session_state.vector_db_created = True
    st.success(
        """
        knowledge base loaded succesfully
        \n
        You can now ask questions now. 
        \n
        or 
        \n
        you can update knowledge data base using below button 👇
        \n
        """
    )
except Exception as e:
    st.error(f"Please create a Knowledge base before you start: {e}")

# Button to create knowledge base (vector DB)
btn = st.button("Update Knowledge Base")
if btn:
    try:
        retriever_tool, retriever, tools, vectorstore = build_vector_db()
        st.session_state.retriever_tool = retriever_tool
        st.session_state.retriever = retriever
        st.session_state.tools = tools
        st.session_state.vectorstore = vectorstore
        st.session_state.vector_db_created = True
        st.success("Knowledge Base created successfully! You can now ask questions.")
    except Exception as e:
        st.error(f"Error creating knowledge base: {e}")

if st.session_state.vector_db_created:
    user_input = st.text_input(
        "Enter your question about stocks, finance, or cryptocurrency:",
        key="question_input",
    )
    if st.button("Submit"):
        if user_input.strip():
            retriever_tool = st.session_state.retriever_tool
            retriever = st.session_state.retriever
            tools = st.session_state.tools
            vectorstore = st.session_state.vectorstore

            result = process_user_input(
                user_input, retriever_tool, retriever, tools, vectorstore
            )
            st.subheader("Answer:")
            st.write(result)
        else:
            st.warning("Please enter a question before submitting.")
else:
    st.write(
        "Please create the knowledge base first by clicking 'Create Knowledge Base'."
    )
