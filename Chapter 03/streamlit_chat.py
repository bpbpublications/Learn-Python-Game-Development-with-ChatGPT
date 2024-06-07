import streamlit as st

# Function to initialize the chat history
@st.cache_resource()
def init_chat_history():
    return []

# Function to add a new message to the chat history
def add_message(chat_history, username, message):
    chat_history.append(f"{username}: {message}")

# Main function to run the chat application
def main():
    st.title("Multi-User Chat Application")

    username = st.text_input("Enter your username:")
    message = st.text_input("Enter your message:")

    chat_history = init_chat_history()

    if st.button("Send"):
        if username and message:
            add_message(chat_history, username, message)
            st.experimental_rerun()

    st.write("Chat History:")
    for chat_message in chat_history:
        st.write(chat_message)

if __name__ == "__main__":
    main()
