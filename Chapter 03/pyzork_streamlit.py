import streamlit as st

# Function to manage chat history
def manage_chat_history(state, user_input):
    state.chat_history.append({"user": user_input})
    bot_reply = f"Echoing: {user_input}"
    state.chat_history.append({"bot": bot_reply})

# Initialize state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize a "version" counter
if 'input_version' not in st.session_state:
    st.session_state.input_version = 0

# Display an image at the top of the main page
st.image("generated_image.png", caption="Your Caption",
         use_column_width=True)

# User message prompt in the main page
with st.form(key='chat_form'):
    user_input = st.text_input("Type your message:",
                               key=f'input_key_{st.session_state.input_version}')
    send_button = st.form_submit_button(label='Send')

    if send_button and user_input:
        manage_chat_history(st.session_state, user_input)
        
        # Increment the version counter to trigger a rerender of the text input
        st.session_state.input_version += 1
        st.experimental_rerun()

# Display chat history in sidebar
st.sidebar.header("Chat History")
for chat in st.session_state.chat_history:
    for role, message in chat.items():
        st.sidebar.write(f"{role.capitalize()}: {message}")
