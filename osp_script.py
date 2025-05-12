import os
from docx import Document
from io import BytesIO
from PIL import Image

# Specify the paths
doc_path = r"C:\Users\DESKTOP.GE\Desktop\pyphoto\ChangePy.docx"  # Path to your Word document
folder_path = r"C:\Users\DESKTOP.GE\Desktop\pyphoto\photos_folder"  # Folder to save images

# Ensure the folder exists, create it if it doesn't
os.makedirs(folder_path, exist_ok=True)

# Function to extract and save images from a Word document
def extract_images_to_folder(doc_path, folder_path):
    doc = Document(doc_path)
    image_count = 0  # To keep track of image numbers

    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:  # Check if the part is an image
            image_count += 1
            image_data = rel.target_part.blob  # Get image data
            image = Image.open(BytesIO(image_data))  # Open image from bytes
            
            # Define the image path and save it
            image_path = os.path.join(folder_path, f"image_{image_count}.png")
            image.save(image_path, "PNG")  # Save as PNG
            
            print(f"Saved {image_path}")

    print(f"Total images extracted: {image_count}")

# Run the function
extract_images_to_folder(doc_path, folder_path)
