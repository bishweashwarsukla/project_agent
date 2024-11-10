import streamlit as st
from main import process_user_input, build_vector_db

# Initialize session state to keep track of whether the vector DB has been created
if "vector_db_created" not in st.session_state:
    st.session_state.vector_db_created = False

st.title("Ask your query")


# Button to create knowledge base (vector DB)
btn = st.button("Create knowledgeBase")
if btn:
    # Call the build_vector_db function to create the vector DB
    retriever_tool, retriever, tools, vectorstore = build_vector_db()

    # Store the variables in session state
    st.session_state.retriever_tool = retriever_tool
    st.session_state.retriever = retriever
    st.session_state.tools = tools
    st.session_state.vectorstore = vectorstore
    st.session_state.vector_db_created = True  # Mark that the vector DB is created
    st.write("VectorDB is created, please proceed with your questions.")
    # st.write("Retriever Tool:", retriever_tool)
    # st.write("Retriever:", retriever)
    # st.write("Tools:", tools)
    # st.write("Vectorstore:", vectorstore)

# Step 1: Take user input only if the vector DB is created
if st.session_state.vector_db_created:
    st.write("Type your question below. Type 'exit' to stop asking questions.")
    user_input = st.text_input("Enter your question or text:", key="question_input")

    if st.button("Submit"):
        # Check if the user wants to exit
        if user_input.strip().lower() == "exit":
            st.write("Thank you! Exiting the question loop.")
            st.session_state.vector_db_created = False  # Reset to allow the user to restart
        else:
            # Process the input if it's not "exit"
            if user_input:
                # Retrieve the stored session state values
                retriever_tool = st.session_state.retriever_tool
                retriever = st.session_state.retriever
                tools = st.session_state.tools
                vectorstore = st.session_state.vectorstore

                # Call the process_user_input function
                result = process_user_input(user_input, retriever_tool, retriever, tools, vectorstore)
                
                # Display the result
                st.subheader("Result:")
                st.markdown(result, unsafe_allow_html=True)  # Display the formatted result
                st.success("Question processed! You can ask another or type 'exit' to stop.")
            else:
                st.warning("Please enter a question before submitting.")
else:
    st.write("Please create the knowledge base first by clicking the 'Create knowledgeBase' button.")
