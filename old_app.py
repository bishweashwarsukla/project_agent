import streamlit as st
from old_main import process_user_input


st.title("Ask your query")

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

            result = process_user_input(user_input)
            # Display the result
            st.subheader("Result:")
            st.markdown(result, unsafe_allow_html=True)  # Display the formatted result
            st.success(
                "Question processed! You can ask another or type 'exit' to stop."
            )
        else:
            st.warning("Please enter a question before submitting.")
