import os
from PIL import Image, ImageOps

def autocrop(image):
    """Helper function to crop whitespace and transparent areas"""
    bbox = image.getbbox()
    if bbox:
        return image.crop(bbox)
    return image

def slice_spritesheet(image_path, rows, cols, output_folder, fixed_width, padding=32):
    """... [Same docstring as before with added parameter description for fixed_width] ..."""
    
    img = Image.open(image_path)
    
    SPRITE_WIDTH = img.width // cols
    SPRITE_HEIGHT = img.height // rows 
    slices = []

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for row in range(rows):
        for col in range(cols):
            left = col * SPRITE_WIDTH
            upper = row * SPRITE_HEIGHT 
            right = (col + 1) * SPRITE_WIDTH
            lower = (row + 1) * SPRITE_HEIGHT 
            slice_img = img.crop((left, upper, right, lower))
            cropped_img = autocrop(slice_img)

            # Resize the cropped content to the sprite width, maintaining aspect ratio
            aspect_ratio = cropped_img.width / cropped_img.height
            new_height = int(SPRITE_WIDTH / aspect_ratio)
            resized_img = cropped_img.resize((SPRITE_WIDTH, new_height), Image.ANTIALIAS)
            
            background = Image.new('RGBA', (SPRITE_WIDTH, new_height), (255, 255, 255, 0))
            
            # Calculate the vertical offset to center the content
            y_offset = (SPRITE_HEIGHT - new_height) // 2
            y_offset = 0
            background.paste(resized_img, (0, y_offset), resized_img)
            
            # Resize to the fixed width while maintaining the aspect ratio
            final_aspect_ratio = background.width / background.height
            final_height = int(fixed_width / final_aspect_ratio)
            final_img = background.resize((fixed_width, final_height), Image.ANTIALIAS)
            
            slices.append(final_img)
            
            # Save the sprite image to the output folder
            sprite_name = f"sprite_row{row}_col{col}.png"
            final_img.save(os.path.join(output_folder, sprite_name))

    return slices

# Example usage
fixed_width = 128  # Replace with the desired width
# Example usage
sprites = slice_spritesheet("generated_tiles2.png",
                            4, 3, 
                            "generated_tiles2", 
                            fixed_width)
