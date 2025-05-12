# import PyPDF2
# from fpdf import FPDF
# from transformers import MarianMTModel, MarianTokenizer
# from tqdm import tqdm

# print("All libraries imported successfully!")


# def extract_text_from_pdf(pdf_path):
#     """
#     Extract text from PDF file.
#     """
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfFileReader(file)
#         text = ""
#         for page_num in range(reader.numPages):
#             text += reader.getPage(page_num).extractText()
#     return text

# def translate_text(text, source_language, target_language, max_length=512):
#     """
#     Translates text from source language to target language.
#     """
#     # change lng
#     model_name = f'Helsinki-NLP/opus-mt-{source_language}-{target_language}'
#     model = MarianMTModel.from_pretrained(model_name)
#     tokenizer = MarianTokenizer.from_pretrained(model_name)

#     text_segments = [text[i:i + max_length] for i in range(0, len(text), max_length)]

#     translated_segments = []
    
#     # Use tqdm for loading bar
#     for segment in tqdm(text_segments, desc="Translating", unit="segment"):
#         inputs = tokenizer(segment, return_tensors='pt', padding=True, max_length=max_length, truncation=True)
#         outputs = model.generate(**inputs)
#         translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         translated_segments.append(translated_text)

#     translated_text = " ".join(translated_segments)
#     return translated_text

# def create_pdf_from_text(text, output_path):
#     """
#     Creates a PDF file from text.
#     """
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 5, txt=text, align="L")
#     pdf.output(output_path)

# input_pdf_path = 'C:\\Users\\DESKTOP.GE\\Desktop\\civi\\civiko.pdf'
# output_pdf_path = 'C:\\Users\\DESKTOP.GE\\Desktop\\civi\\output_translated.pdf'
# source_language = 'en'  
# target_language = 'ka'  

# text = extract_text_from_pdf(input_pdf_path)
# translated_text = translate_text(text, source_language, target_language)
# create_pdf_from_text(translated_text, output_pdf_path)



import fitz  # PyMuPDF
import pytesseract
from pytesseract import Output
from PIL import Image
from deep_translator import GoogleTranslator
from fpdf import FPDF
import os

# Tesseract OCR path (if needed, specify full path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract images and text with positions
def extract_elements_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    elements = []
    
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        pix = page.get_pixmap()
        image_path = f"page_{page_number}.png"
        pix.save(image_path)

        # OCR text recognition
        with Image.open(image_path) as img:
            ocr_data = pytesseract.image_to_data(img, output_type=Output.DICT, lang='eng')
            for i in range(len(ocr_data['text'])):
                if ocr_data['text'][i].strip():
                    element = {
                        "type": "text",
                        "text": ocr_data['text'][i],
                        "x": ocr_data['left'][i],
                        "y": ocr_data['top'][i],
                        "width": ocr_data['width'][i],
                        "height": ocr_data['height'][i],
                        "page": page_number
                    }
                    elements.append(element)

        # Extract images separately
        for image_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_path = f"page_{page_number}_img_{image_index}.png"
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            elements.append({"type": "image", "path": image_path, "page": page_number})

    pdf_document.close()
    return elements

# Function to translate text
def translate_text(text, source_language="en", target_language="ka"):
    translator = GoogleTranslator(source=source_language, target=target_language)
    return translator.translate(text)

# Function to recreate PDF
def create_translated_pdf(elements, output_path, original_pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('NotoSans', '', 'NotoSansGeorgian_Condensed-Regular.ttf', uni=True)
    pdf.set_font('NotoSans', size=12)
    
    pdf_document = fitz.open(original_pdf_path)

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        pdf.add_page()
        for element in elements:
            if element['page'] == page_number:
                if element['type'] == 'text':
                    # Place translated text at the correct position
                    translated_text = translate_text(element['text'])
                    pdf.set_xy(element['x'] / 3, element['y'] / 3)
                    pdf.multi_cell(element['width'] / 3, 10, translated_text)
                elif element['type'] == 'image':
                    # Add images at the correct position
                    pdf.image(element['path'], x=element.get('x', 10), y=element.get('y', 10), w=element.get('width', 100))
    
    pdf.output(output_path)

# Paths and settings
input_pdf_path = 'C:\\Users\\DESKTOP.GE\\Desktop\\civi\\civiko.pdf'
output_pdf_path = 'C:\\Users\\DESKTOP.GE\\Desktop\\civi\\output_translated.pdf'

# Extract, translate, and recreate the PDF
elements = extract_elements_from_pdf(input_pdf_path)
create_translated_pdf(elements, output_pdf_path, input_pdf_path)

print(f"Translated PDF saved at {output_pdf_path}")
