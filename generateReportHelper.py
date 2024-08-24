import os
import fitz  # PyMuPDF

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
    "circle" : fitz.Rect(42.77000045776367, 330.59039306640625, 85.22305297851562, 371.51324462890625),
    "description" : fitz.Rect(42.52000045776367, 382.3380126953125, 567.3809814453125, 640.177001953125)
}

descriptions = {
    "Cov-2_pos": """A positive test result for this test means that SARSCoV-2 RNA was present in the specimen above the limit of detection. For a sample to be considered positive for SARS-CoV-2, the patient sample must return target Ct values of <=35. However, a negative result does not rule out COVID-19 and should not be used as the sole basis for treatment orpatient management decisions. Negative results must be combined with clinical observations, patient history, and epidemiological information. All laboratory tests have limitations. Negative results do not preclude infection with RSV, Flu A & B virus. \n\nMolecular Testing performed via Thermo Fisher Quant Studio PCR utilizing PheonixDX SARS-CoV-2 test assay. The PheonixDX SARS-C0V-2 assay is an Emergency Use Authorization (EUA) test authorized by the U.S. FDA for use by authorized laboratories, using real-time (RT) polymerase chain reaction (PCR) technology for the qualitative detection of nucleic acids from the SARS-CoV-2 virus and diagnosis of SARS-CoV-2 virus infection from individuals meeting CDC clinical and/or epidemiological testing criteria. Testing is limited to laboratories certified under the Clinical Laboratory Improvement Amendments of 1988 (CLIA), 42 U.S.C. §263a, that meet requirements to perform high complexity tests. The test detects all current variants of concern as defined by the Center for Disease Control (CDC), including: \n\nB.1.1.7 (Alpha), B.1.351 (Beta), P.1 (Gamma), B.1.617.2 (Delta), B.1.1.529 (Omicron)\n\n\n[END OF REPORT]""",

    "Cov-2_neg": """A negative test result for this test means that SARSCoV-2, RSV, Flu A & B RNA was not present in the specimen above the limit of detection. For a sample to be considered positive for SARS-CoV-2, the patient sample must return target Ct values of <=35. However, a negative result does not rule out COVID-19 and should not be used as the sole basis for treatment or patient management decisions. Negative results must be combined with clinical observations, patient history, and epidemiological information. All laboratory tests have limitations. Negative results do not preclude infection with SARS-CoV-2, RSV, Flu A & B virus. \n\nMolecular Testing performed via Thermo Fisher Quant Studio PCR utilizing PheonixDX SARS-CoV-2 test assay. The PheonixDX SARS-C0V-2 assay is an Emergency Use Authorization (EUA) test authorized by the U.S. FDA for use by authorized laboratories, using real-time (RT) polymerase chain reaction (PCR) technology for the qualitative detection of nucleic acids from the SARS-CoV-2 virus and diagnosis of SARS-CoV-2 virus infection from individuals meeting CDC clinical and/or epidemiological testing criteria. Testing is limited to laboratories certified under the Clinical Laboratory Improvement Amendments of 1988 (CLIA), 42 U.S.C. §263a, that meet requirements to perform high complexity tests. The test detects all current variants of concern as defined by the Center for Disease Control (CDC), including:\n\nB.1.1.7 (Alpha), B.1.351 (Beta), P.1 (Gamma), B.1.617.2 (Delta), B.1.1.529 (Omicron)\n\n\n[END OF REPORT]""",

    "RSV_pos": """A positive result from a polymerase chain reaction (PCR) test for Respiratory Syncytial Virus (RSV) indicates that the patient is likely infected with the virus. However, the test doesn't show the stage of the infection. A final diagnosis should consider the results in the context of clinical observations and other data.\n\n\n[END OF REPORT]""",

    "RSV_neg": """A negative result means that no signs of the RSV virus were found in your sample. They may mean that another illness is causing your symptoms. But a negative test result does not rule out RSV. It's possible that there was not enough of the virus in the sample for the test to find it.\n\n\n[END OF REPORT]""",

    "Flu_pos": """A positive test result for influenza A virus or influenza B virus indicates that RNA from one or both of these viruses was detected, the patient is infected with the virus(es) and is presumed to be contagious. Laboratory test results should always be considered in the context of clinical findings and observations and epidemiological data in making a final diagnosis. Patient management decisions should be made by a healthcare provider and follow current CDC guidelines. Results (positive and negative) for influenza should be interpreted with caution. If a result is inconsistent with clinical presentation and/or other clinical and epidemiological information, FDA-cleared influenza NAATs are available for confirmation if clinically indicated.\n\n\n[END OF REPORT]""",

    "Flu_neg": """A negative result means that there is no evidence of influenza viral RNA or nucleic acids in the respiratory specimen tested. For hospitalized patients, especially for patients with lower respiratory tract disease, if no other etiology is identified and influenza is still clinically suspected, additional specimens should be collected and tested, and antiviral treatment should be initiated or continued.\n\n\n[END OF REPORT]"""
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

def get_color_test_description(name, result):
    # set color
    result_color = color("black")
    result_text = ""
    result_mean = ""
    if(result == "pos"):
        result_color = color("red")
        result_text = "MOLECULAR TESTING POSITIVE RESULTS"
        result_mean = "A POSITIVE RESULT MEANS THAT THE VIRUS WAS DETECTED IN \nTHE SAMPLE YOU PROVIDED. THE RESULTS SUGGEST YOU WERE POSITIVE \nAT THE TIME OF TESTING."
        result_sign = "pos.png"
    elif(result == "neg"):
        result_color = color("green")
        result_text = "MOLECULAR TESTING NEGATIVE RESULTS"
        result_mean = "A NEGATIVE RESULT MEANS THAT THE VIRUS WAS NOT DETECTED IN \nTHE SAMPLE YOU PROVIDED. THE RESULTS SUGGEST YOU WERE NEGATIVE \nAT THE TIME OF TESTING."
        result_sign = "neg.png"
        
    test_name = ""
    if(name == "Cov-2"):
        test_name = "SARS-Cov-2/Covid-19"
    elif(name == "Flu"):
        test_name = "Flu A & B"
    elif(name == "RSV"):
        test_name = "Respiratory Syncytial Virus (RSV)" 
    
    description = name + "_" + result
    
    return (test_name, result_color, result_text, result_mean, result_sign, descriptions[description])
    
