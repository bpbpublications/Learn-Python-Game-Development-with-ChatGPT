import streamlit as st
from PIL import Image

# Title of the app
st.title("Image Upload Example")

# Upload image through streamlit
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Image successfully uploaded and displayed above.")
