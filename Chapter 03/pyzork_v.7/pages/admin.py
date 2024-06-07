import streamlit as st
from game import GameEngine

@st.cache_resource
def get_game_engine():
    return GameEngine()

ge = get_game_engine()
# Define the main function for adding game objects
def add_game_object():
    object_type = st.selectbox("Object Type", 
                               ["ROOM", "ITEM", "NPC"])
    object_name = st.text_input("Object Name")
    object_description = st.text_area("Object Description")
    object_image = st.file_uploader("Object Image", 
                                    type=["jpg", "jpeg", "png"])
    object_special = None

    room_list = [room for room in ge.world.rooms.keys()]
    if object_type == "ROOM":
        object_rooms = st.multiselect("Exits to other rooms", room_list)
        object_special = st.multiselect("Select room exit directions",
                                        ["North", "South", "East", "West"])
    elif object_type == "ITEM":
        object_rooms = st.multiselect("Is found in rooms", room_list)
        object_special = st.text_input("Item context")
    elif object_type == "NPC":
        object_rooms = st.multiselect("Is found in rooms", room_list)
        object_special = st.text_input("NPC background")

    if st.button("Add Object"):
        try:
            ge.add_object(object_type,
                          object_name,
                          object_description,
                          object_image,
                          object_rooms,
                          object_special
                          )
            st.success("Object added successfully!")
        except Exception as ex:
            st.error(ex)

# Streamlit UI
st.title("Game Object Editor")
add_game_object()
