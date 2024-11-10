
# # Title of the app
# st.title("User Input Application 📄")

# # Step 1: Take user input
# st.subheader("Please enter the information:")
# user_input = st.text_input("Enter your question or text:")

# # Step 2: Display the result
# if st.button("Submit"):
#     if user_input:
#         # Call the function from main.py to process the input
#         result = process_user_input(user_input)
        
#         # Display the output
#         st.subheader("Result:")
#         st.markdown(result, unsafe_allow_html=True)  # Render markdown format
        
#         # Feedback or additional confirmation
#         st.success("Your input has been successfully processed!")
#     else:
#         st.warning("Please enter some text before submitting.")

################################################################################################################################################
# import streamlit as st
# from main import create_vector_db, get_qa_chain

# st.title("QA 🤔")
# st.title("are u system administrator🖥️")
# system_admin = st.button("🖥")
# system_admin_no = st.button("🚫")
# if system_admin:
#     btn = st.button("create knowledgeBase")
#     if btn:
#         create_vector_db()
# st.title("choose ur gender ")
# male = st.button("🙋‍♂")
# female = st.button("🙋‍♀️")


# if male:
#     question = st.text_input("Question: 🙋‍♂️")
# else:
#     question = st.text_input("Question: 🙋‍♀️")

# if question:
#     chain = get_qa_chain()
#     response = chain(question)
#     print(response)
#     st.header("Answer: ")
#     st.write(response["result"])

# st.title("source doucments ")
# src_doc = st.button("📄")
# if src_doc:
#     st.write(response["source_documents"])
############################################################################################################################################################

###################################################################################################################################################
# for looping till user hit exit  ------- throwing error, check to fix it 
import streamlit as st
from main_test import process_user_input, build_vector_db

# Initialize session state to keep track of whether the vector DB has been created
if "vector_db_created" not in st.session_state:
    st.session_state.vector_db_created = False

st.title("Ask your query")

# system_admin = st.button("🖥")
# system_admin_no = st.button("🚫")
# if system_admin:
btn = st.button("create knowledgeBase")
if btn:
    retriever_tool, retriever, tools, vectorstore = build_vector_db()
    # Store the variables in session state
    st.session_state.retriever_tool = retriever_tool
    st.session_state.retriever = retriever
    st.session_state.tools = tools
    st.session_state.vectorstore = vectorstore
    st.session_state.vector_db_created = True  # Mark that the vector DB is created
    st.write("VectorDB is created, please proceed with your questions.")

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


# # Step 1: Take user input
# user_input = st.text_input("Enter your question or text:", key="question_input")
# st.write("Type your question below. Type 'exit' to stop asking questions.")

# if st.button("Submit"):
#     # Check if the user wants to exit
#     if user_input.strip().lower() == "exit":
#         st.write("Thank you! Exiting the question loop.")
#         st.session_state.continue_asking = False  # Stop asking questions
#     else:
#         # Process the input if it's not "exit"
#         if user_input:
#             result = process_user_input(user_input, retriever_tool, retriever, tools, vectorstore)
#             st.subheader("Result:")
#             st.markdown(result, unsafe_allow_html=True)  # Display the formatted result
#             st.success("Question processed! You can ask another or type 'exit' to stop.")
#         else:
#             st.warning("Please enter a question before submitting.")
