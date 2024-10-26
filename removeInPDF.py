from PIL import Image
import fitz  # PyMuPDF
import os

def replace_pdf(pdf_path, new_text):
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
    current_directory = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_directory, 'static', 'header.jpg')
    with Image.open(image_path) as img:

        # Iterate over each page in the PDF
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            
            replace_text_in_pdf(page, new_text)
        
        # Save the updated PDF
        head, tail = os.path.split(pdf_path)
        name, ext = os.path.splitext(tail)
        new_name = f"replaced_{name}{ext}"
        output_pdf_path = os.path.join(head, new_name)
        pdf_document.save(output_pdf_path)
        pdf_document.close()
        return output_pdf_path


def replace_text_in_pdf(page, new_text):
    """
    Replace specified text on a PDF page with new text.
    Searches for `old_text` on the `page`, covers it with a white rectangle, and inserts `new_text` at the same location.

    :param page: fitz.Page The page to modify (from a fitz.Document).
    :param new_text: str The text to insert.
    :return: None Modifies the page in place.
    """
    # Position of Refferring Physician Name
    instance = fitz.Rect(287.6343078613281, 183.04403686523438, 353.5799865722656, 194.76817321777344)
    
    # Cover the text with a white with slight yellowish tint
    rgba_color = (255, 251, 239, 255)  # White with slight yellowish tint
    rgb_color = (rgba_color[0] / 255.0, rgba_color[1] / 255.0, rgba_color[2] / 255.0)
    instance1 = fitz.Rect(410.2229919433594, 185.62503051757812, 550.4169921875, 197.8490447998047)
    page.draw_rect(instance1, color=(1,1,1), fill=(1,1,1))
    
    # Calculate the position and size for the new text
    x0, y0, x1, y1 = instance
    # Insert the new text at the adjusted position
    page.insert_text((x0-2, y0+10), new_text, fontsize=11, color=(0, 0, 0), fontname='Courier')
    
# Example usage
# Position is (x, y) for the top-left corner of the image
# replace_pdf('static/template.pdf', new_text=' ')