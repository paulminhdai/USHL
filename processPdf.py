from PIL import Image
import fitz  # PyMuPDF
import os

def replace_pdf(pdf_path, old_text, new_text):
    """
    Overlay an image on all pages of a PDF at a specified position.

    :param pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to the output PDF file.
    :param position: Tuple (x, y) representing the position of the top-left corner of the image.
    :param old_text: The text to be replaced.
    :param new_text: The text to insert.
    """
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Open the image file
    image_path = 'header.jpg'
    with Image.open(image_path) as img:

        # Iterate over each page in the PDF
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            
            position = (0,0)
            replace_header_in_pdf(page, img, image_path, position)
            
            replace_text_in_pdf(page, old_text, new_text)
        
        # Save the updated PDF
        head, tail = os.path.split(pdf_path)
        name, ext = os.path.splitext(tail)
        new_name = f"replaced_{name}{ext}"
        output_pdf_path = os.path.join(head, new_name)
        pdf_document.save(output_pdf_path)
        pdf_document.close()
        return output_pdf_path

def replace_header_in_pdf(page, img, image_path, position):
    """
    Overlay an image on the top of a PDF page.
    Resizes the image to match the page width and overlays it at the specified position.
    
    :param page: fitz.Page The PDF page where the image will be placed.
    :param img: PIL.Image The image to overlay.
    :param image_path: str Path to the image file.
    :param position: Tuple (x, y) representing the position of the top-left corner of the image.
    :return: None The image is inserted on the page.
    """
    # Calculate new image size
    img_width, img_height = img.size
    
    # Get the page width
    page_width = page.rect.width
    
    # Calculate new image size
    new_width = int(page_width)
    new_height = int((new_width / img_width) * img_height)
    
    # Determine the position rectangle
    x_pos, y_pos = position
    rect = fitz.Rect(x_pos, y_pos, x_pos + new_width, y_pos + new_height)
    
    # Overlay the image on the page
    page.insert_image(rect, filename=image_path)

def replace_text_in_pdf(page, old_text, new_text):
    """
    Replace specified text on a PDF page with new text.
    Searches for `old_text` on the `page`, covers it with a white rectangle, and inserts `new_text` at the same location.

    :param page: fitz.Page The page to modify (from a fitz.Document).
    :param old_text: str The text to be replaced.
    :param new_text: str The text to insert.
    :return: None Modifies the page in place.
    """
    # Search for the old text
    text_instances = page.search_for(old_text)
    print(text_instances)
    
    # Cover the old text with white rectangles
    for inst in text_instances:
        print(inst)
        # Cover the text with a white with slight yellowish tint
        rgba_color = (255, 251, 239, 255)  # White with slight yellowish tint
        rgb_color = (rgba_color[0] / 255.0, rgba_color[1] / 255.0, rgba_color[2] / 255.0)
        page.draw_rect(inst, color=rgb_color, fill=rgb_color)
        
        # Calculate the position and size for the new text
        x0, y0, x1, y1 = inst
        text_rect = fitz.Rect(x0, y0, x1, y1)
        
        # # Insert the new text
        # page.insert_textbox(text_rect, new_text, fontsize=48, color=(0, 0, 0))
        
        # Insert the new text at the adjusted position
        page.insert_text((x0-2, y0+10), new_text, fontsize=11, color=(0, 0, 0), fontname='Courier')
    

# Example usage
# Position is (x, y) for the top-left corner of the image
# replace_pdf('input.pdf', ', old_text='L Dellamaggiora', new_text='Roman Testing')
