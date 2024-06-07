import os
import shutil

def find_and_copy_images(root_folder, dest_folder):
    image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']
    os.makedirs(dest_folder, exist_ok=True)  # Create destination folder if it doesn't exist

    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                src_path = os.path.join(subdir, file)
                dest_path = os.path.join(dest_folder, file)
                shutil.copy2(src_path, dest_path)

root_folder = 'G:\\My Drive\\Books\\Learn_Python_Game_Development_with_ChatGPT\\chapters' 
dest_folder = 'C:\\bu2 - Copy\\LPGDwithChatGPT\\images' 

find_and_copy_images(root_folder, dest_folder)

print("Images have been copied.")
