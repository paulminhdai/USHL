import fitz  # PyMuPDF
from processPdf import replace_text_in_pdf
import os

def remove(pdf_path, old_text):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)
    text_instances = page.search_for(old_text)
    # print(text_instances)
    
    # Cover the old text with white rectangles
    for inst in text_instances:
        print(inst)
        # Cover the text with a white with slight yellowish tint
        rgba_color = (255, 251, 239, 255)  # White with slight yellowish tint
        rgb_color = (rgba_color[0] / 255.0, rgba_color[1] / 255.0, rgba_color[2] / 255.0)
        border_color = (0,0,0)
        inst1 = fitz.Rect(42.52000045776367, 382.3380126953125, 567.3809814453125, 640.177001953125)
        page.draw_rect(inst1, color=border_color, fill=rgb_color)
        
        # Calculate the position and size for the new text
        x0, y0, x1, y1 = inst
        text_rect = fitz.Rect(x0, y0, x1, y1)
        
        # # Insert the new text
        # page.insert_textbox(text_rect, new_text, fontsize=48, color=(0, 0, 0))
        
        # Insert the new text at the adjusted position
        # page.insert_text((x0-2, y0+10), new_text, fontsize=11, color=(0, 0, 0), fontname='Courier')
    head, tail = os.path.split(pdf_path)
    name, ext = os.path.splitext(tail)
    new_name = f"replaced_{name}{ext}"
    output_pdf_path = os.path.join(head, new_name)
    pdf_document.save(output_pdf_path)
    pdf_document.close()
    return output_pdf_path
        
remove('/Users/daivuong/Desktop/test/overlayPDF/resource/reporttemplates/template.pdf', 'A positive test result for this test means that')

    
