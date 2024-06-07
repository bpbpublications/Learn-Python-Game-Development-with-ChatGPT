import streamlit as st
import sqlite3
from PIL import Image
import io

# Connect to SQLite database
conn = sqlite3.connect('images.db')
c = conn.cursor()

# Create table if it doesn't exist yet
c.execute('''CREATE TABLE IF NOT EXISTS images (image BLOB);''')
conn.commit()

def insert_image(image):
    # Convert the image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_byte = buffered.getvalue()
    
    # Insert the image into the database
    c.execute("INSERT INTO images (image) VALUES (?)", (sqlite3.Binary(img_byte),))
    conn.commit()

def get_all_images():
    c.execute("SELECT * FROM images")
    return c.fetchall()

st.title("Streamlit Image Upload and SQLite Example")

uploaded_image = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if uploaded_image is not None:
    st.image(uploaded_image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    image = Image.open(uploaded_image)
    
    if st.button("Save to Database"):
        insert_image(image)
        st.success("Saved to Database")

st.write("---")

st.header("Images in Database")
all_images = get_all_images()

for idx, img_data in enumerate(all_images):
    st.write(f"Image ID: {idx}")
    image = Image.open(io.BytesIO(img_data[0]))
    st.image(image, use_column_width=True)
