import fitz  # PyMuPDF
import pandas as pd
from helper import color, instances_positions, fontName, split_address, get_color_test_description
import os

current_directory = os.path.dirname(os.path.abspath(__file__))


def extract_patient_info(file_path):
    """Extracts patient information from an Excel sheet and combines test results."""

    # Load the Excel sheet
    dtype = {'Patient ID': str}
    df = pd.read_excel(file_path, dtype=dtype)
    df['DOB'] = df['DOB'].dt.strftime('%m/%d/%Y')

    # Extract relevant columns
    patient_info = df[['Date of Service', 'Patient Name', 'DOB', 'ADDRESS', 'SEX', 'Patient ID', 'SAMPLE ID', 'Cov-2', 'Flu', 'RSV']]

    return patient_info

def fill_reports(page, row, name, result):
    # Patient info
    x0, y0, x1, y1 = instances_positions["patient_name"]
    page.insert_text((x0, y0+10), row['Patient Name'], fontsize=11, color=color("black"), fontname=fontName)
    
    x0, y0, x1, y1 = instances_positions["dob"]
    page.insert_text((x0-2, y0+9), row['DOB'], fontsize=11, color=color("black"), fontname=fontName)
    
    x0, y0, x1, y1 = instances_positions["sex"]
    page.insert_text((x0-2, y0+8.5), row['SEX'], fontsize=11, color=color("black"), fontname=fontName)
    
    x0, y0, x1, y1 = instances_positions["patient_id"]
    page.insert_text((x0-2, y0+9.5), row['Patient ID'], fontsize=11, color=color("black"), fontname=fontName)
    
    street_address, city_state_zip = split_address(row['ADDRESS'])
    x0, y0, x1, y1 = instances_positions["add1"]
    page.insert_text((x0-2, y0+8), street_address, fontsize=10, color=color("black"), fontname=fontName)
    x0, y0, x1, y1 = instances_positions["add2"]
    page.insert_text((x0, y0+8), city_state_zip, fontsize=10, color=color("black"), fontname=fontName)
    
    x0, y0, x1, y1 = instances_positions["speciment_id"]
    page.insert_text((x0-1, y0+9), row['SAMPLE ID'], fontsize=11, color=color("black"), fontname=fontName)
    
    x0, y0, x1, y1 = instances_positions["speciment_colletion_date"]
    page.insert_text((x0-2, y0+9), row['Date of Service'], fontsize=11, color=color("black"), fontname=fontName)
    
    x0, y0, x1, y1 = instances_positions["date_of_service"]
    page.insert_text((x0-2, y0+10), row['Date of Service'], fontsize=11, color=color("black"), fontname=fontName)
    
    # test result
    test_name, result_color, result_text, result_mean, result_sign, description = get_color_test_description(name, result)
    
    colar_bar_instance = instances_positions["color_bar"]
    page.draw_rect(colar_bar_instance, color=result_color, fill=result_color)
    x0, y0, x1, y1 = instances_positions["color_bar"]
    page.insert_text((x0+20, y0+15), result_text, fontsize=12, color=color("white"), fontname=fontName)
    page.insert_text((x0+350, y0+15), test_name, fontsize=12, color=color("white"), fontname=fontName)
    
    x0, y0, x1, y1 = instances_positions["mean"]
    page.insert_text((x0-2, y0+10), result_mean, fontsize=11, color=result_color, fontname=fontName)
    result_sign_path = os.path.join(current_directory, 'static', result_sign)
    page.insert_image(instances_positions["circle"], filename=result_sign_path)
    
    x0, y0, x1, y1 = instances_positions["description"]
    # page.insert_text((x0-2, y0+10), description, fontsize=11, color=color("black"), fontname=fontName, lineheight=0.6)
    page.insert_textbox((x0, y0, x1-5, y1+110), description, fontsize=10, color=color("black"), fontname=fontName, lineheight=1.3)
    
def export_file(test_name, res, row, export_path):
    pdf_template_path = os.path.join(current_directory, 'static', 'template.pdf')
    pdf_document = fitz.open(pdf_template_path)
    page = pdf_document.load_page(0)
    
    fill_reports(page, row, test_name, res)
    
    path = os.path.abspath(export_path)
    new_name = f"{row['Patient Name']}{'_'}{test_name}{'.pdf'}"
    output_pdf_path = os.path.join(path, new_name)
    pdf_document.save(output_pdf_path)
    pdf_document.close()
    return output_pdf_path

def generate_reports(file_path, export_directory):    
    patient_info = extract_patient_info(file_path)
    
    for index, row in patient_info.iterrows():
        print("Processing patient " + str(index+1))
        # create new folder for each patient in the expected directory
        export_path = os.path.join(export_directory, row['Patient Name'])
        if not os.path.exists(export_path):
            os.makedirs(export_path)
            
        if (row['Cov-2'] == 'N'):
            export_file('Cov-2', "neg", row, export_path)
        elif (row['Cov-2'] == 'P'):
            export_file('Cov-2', "pos", row, export_path)
            
        if (row['RSV'] == 'N'):
            export_file("RSV", "neg", row, export_path)
        elif (row['RSV'] == 'P'):
            export_file("RSV", "pos", row, export_path)

        if (row['Flu'] == 'N'):
            export_file("Flu", "neg", row, export_path)
        elif (row['Flu'] == 'P'):
            export_file("Flu", "pos", row, export_path)
    

# Example usage
file_path = '/Users/daivuong/Desktop/test/overlayPDF/resource/reporttemplates/DATA SAMPLE.xlsx'
export_path = '/Users/daivuong/Desktop/test/overlayPDF/resource/reporttemplates'
generate_reports(file_path, export_path)


