import os
import fitz  # PyMuPDF
import re

instances_positions = {
    "patient_name" : fitz.Rect(51.70998764038086, 182.1260467529297, 165.96998596191406, 192.76605834960938),
    "dob" : fitz.Rect(125.36599731445312, 191.9959930419922, 180.906005859375, 204.43600463867188),
    "sex" : fitz.Rect(74.23100280761719, 201.93697204589844, 104.3810043334961, 213.37698364257812),
    "patient_id" : fitz.Rect(106.12229919433594, 212.1191864013672, 155.12229919433594, 223.25919799804688),
    "add1" : fitz.Rect(95.69329833984375, 222.3822021484375, 153.95030212402344, 232.1382110595703),
    "add2" : fitz.Rect(51.710304260253906, 231.3341796875, 190.02030944824219, 241.9901885986328),
    "lab_report_date" : fitz.Rect(287.6343078613281, 183.04403686523438, 353.5799865722656, 194.76817321777344),
    "speciment_id" : fitz.Rect(266.60101318359375, 193.90701599121094, 340.9209899902344, 204.74702758789062),
    "speciment_colletion_date" : fitz.Rect(346.21600341796875, 213.9750213623047, 397.0760498046875, 224.81503295898438),
    "date_of_service" : fitz.Rect(299.2229919433594, 226.62503051757812, 380.4169921875, 240.8490447998047),
    "color_bar" : fitz.Rect(42.77000045776367, 301.890380859375, 552.22305297851562, 324.813232421875),
    "mean" : fitz.Rect(94.2699966430664, 330.59039306640625, 552.22305297851562, 368.51324462890625),
    "circle" : fitz.Rect(42.77000045776367, 330.59039306640625, 85.22305297851562, 368.51324462890625),
    "description" : fitz.Rect(42.52000045776367, 382.3380126953125, 567.3809814453125, 640.177001953125)
}

def remove(pdf_path, instances, instances_positions):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)
    
    for inst in instances:
        # print(inst)
        # print(instances_positions[inst])
        # print()
        
        page.draw_rect(instances_positions[inst], color=color("white"), fill=color("white"))
        
    head, tail = os.path.split(pdf_path)
    name, ext = os.path.splitext(tail)
    new_name = f"replaced_{name}{ext}"
    output_pdf_path = os.path.join(head, new_name)
    pdf_document.save(output_pdf_path)
    pdf_document.close()
    return output_pdf_path

# remove_items = ["patient_name", "dob", "sex", "patient_id", "add1", "add2", "lab_report_date", "speciment_id", 
#                 "speciment_colletion_date", "date_of_service", "color_bar", "mean", "circle", "description"]
# remove('/Users/daivuong/Desktop/test/overlayPDF/resource/reporttemplates/template.pdf', remove_items, instances_positions)

def color(input):
    if input == "red":
        return (1,0,0)
    elif input == "black":
        return (0,0,0)
    elif input == "white":
        return (1,1,1)
    elif input == "green":
        rgba_color = (8, 132, 4, 0)
        return (rgba_color[0] / 255.0, rgba_color[1] / 255.0, rgba_color[2] / 255.0)

fontName='Courier'

import re

def split_address(address):
    """Splits an address into street address and city, state, ZIP code."""

    street_types = ["ave", "st", "dr", "blvd", "ln", "ct", "ter", "rd", "sq", "pl", "pkwy", "cir", "crt", "way"]
    address_lower = address.lower()
    for street_type in street_types:
        if street_type in address_lower:
            index = address_lower.index(street_type)
            street_address = address[:index + len(street_type)]
            city_state_zip = address[index + len(street_type) + 1:]
            return street_address, city_state_zip

    # If no street type is found, split based on the first space
    index = address.find(" ")
    if index != -1:
        street_address = address[:index]
        city_state_zip = address[index + 1:]
        return street_address, city_state_zip

    # Handle cases where the address doesn't have a clear split
    return None, None

