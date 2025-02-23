import sys
import os

CURRENT_DIR = os.path.split(os.path.realpath(__file__))[0]
OE_EXCEL_TEMPLATE_DIR = os.path.join(CURRENT_DIR, "import_excel_template_27772.xlsx")

print(f'sys.argv{sys.argv}')
print(f'OE_EXCEL_TEMPLATE_DIR:{OE_EXCEL_TEMPLATE_DIR}')
file_path = os.path.dirname(__file__)
excel_path = file_path + '/data'
print(file_path)
print(f'excel_path{excel_path}')