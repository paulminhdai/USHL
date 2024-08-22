import fitz  # PyMuPDF
import pandas as pd
from helper import color, instances_positions, fontName, split_address
import os
import datetime


def extract_patient_info(file_path):
    """Extracts patient information from an Excel sheet and combines test results."""

    # Load the Excel sheet
    dtype = {'Patient ID': str}
    df = pd.read_excel(file_path, dtype=dtype)
    df['DOB'] = df['DOB'].dt.strftime('%m/%d/%Y')

    # Extract relevant columns
    patient_info = df[['Date of Service', 'Patient Name', 'DOB', 'ADDRESS', 'SEX', 'Patient ID', 'SAMPLE ID', 'Cov-2', 'Flu', 'RSV']]

    return patient_info

def fill_reports(page, row, result):
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
    
    x0, y0, x1, y1 = instances_positions["circle"]
    page.insert_text((x0-2, y0+10), result, fontsize=18, color=color("red"), fontname=fontName)

def generate_reports(file_path):
    pdf_template_path  = '/Users/daivuong/Desktop/test/overlayPDF/resource/reporttemplates/template.pdf'
    pdf_document = fitz.open(pdf_template_path)
    page = pdf_document.load_page(0)
    patient_info = extract_patient_info(file_path)
    # for index, row in patient_info.iterrows():
    row = patient_info.iloc[0]
    if (row['Cov-2'] == 'N'):
        fill_reports(page, row, "NEGATIVE")

    
    head, tail = os.path.split('/Users/daivuong/Desktop/test/overlayPDF/resource/reporttemplates/results')
    new_name = f"{row['Patient Name']}{'.pdf'}"
    output_pdf_path = os.path.join(head, new_name)
    pdf_document.save(output_pdf_path)
    pdf_document.close()
    return output_pdf_path
    

# Example usage
file_path = '/Users/daivuong/Desktop/test/overlayPDF/resource/reporttemplates/DATA SAMPLE.xlsx'
generate_reports(file_path)


