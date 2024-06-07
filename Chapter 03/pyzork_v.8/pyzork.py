import streamlit as st
from game import GameEngine

@st.cache_resource
def get_game_engine():
    return GameEngine()

# Function to manage chat history
def manage_chat_history(state, user_input, response):
    state.chat_history.append({"Player": user_input})
    response = f"Response: {response}"
    state.chat_history.append({"bot": response})

# Initialize state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize a "version" counter
if 'input_version' not in st.session_state:
    st.session_state.input_version = 0

ge = get_game_engine()
observation = ge.observe()

# Display an image at the top of the main page
if observation["image"]:
    st.image(observation["image"],
             caption=observation["description"],
             use_column_width=True,
             )
else:
    st.image("images/splash.png",
             caption=observation["description"],
             use_column_width=True,
             )
    
if observation["items"]:
    st.write(f"Items: {observation['items']}")
if observation["npcs"]:
    st.write(f"NPCs: {observation['npcs']}")


# User message prompt in the main page
with st.form(key='chat_form'):
    user_input = st.text_input("Type your message:", 
                               key=f'input_key_{st.session_state.input_version}')
    send_button = st.form_submit_button(label='Send')

    if send_button and user_input:
        response = ge.parse_command(user_input)
        manage_chat_history(st.session_state, user_input, response)
        
        # Increment the version counter to trigger a rerender of the text input
        st.session_state.input_version += 1
        st.experimental_rerun()

# Display chat history in sidebar
st.sidebar.header("Command History")
for chat in st.session_state.chat_history:
    for role, message in chat.items():
        st.sidebar.write(f"{role.capitalize()}: {message}")
