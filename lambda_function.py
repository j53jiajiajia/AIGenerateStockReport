from delete_files import delete_pdf, delete_jpg
from main_heat_list import generate_heat_list_stock_reports
from pdftoimage import convert_pdf_to_images

def lambda_handler():
    delete_pdf()
    delete_jpg('图片/chart1图片')
    delete_jpg('图片/chart2图片')
    delete_jpg('图片/table1图片')
    delete_jpg('图片/table2图片')
    delete_jpg('图片/table3图片')
    delete_jpg('研报图片')
    try:
        generate_heat_list_stock_reports()
    except Exception as e:
        print(f"There are some errors about stock report generation today.")
    convert_pdf_to_images()


lambda_handler()
