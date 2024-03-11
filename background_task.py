import boto3
import os
from pdf2image import convert_from_path
import sqlite3
from full_report_pdf import generate_total_report

#####################################################
path_to_db = "records.sqlite3"
#####################################################



def conn_s3(file_path):
    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv('aws_access_key_id'),
                      aws_secret_access_key=os.getenv('aws_secret_access_key'),
                      region_name='ap-southeast-1')
    bucket_name = 'stockresearchreport'

    # upload pdf to s3
    file_path_pdf = file_path 
    s3_key_pdf = f'stock_research_report_pdf/{file_path_pdf[5:]}'
    s3.upload_file(file_path_pdf, bucket_name, s3_key_pdf)

    # convert pdf to jpg and upload jpg to s3
    base_name = os.path.splitext(os.path.basename(file_path_pdf))[0]
    pages = convert_from_path(file_path_pdf, 400)  # 300 DPI是一个比较好的折中选择
    for i, page in enumerate(pages):
        file_path_jpg = f'temp/{base_name}_{i+1}.jpg'
        page.save(file_path_jpg, 'JPEG')
        s3_key_jpg = f'stock_research_report_jpg/{file_path_jpg[5:]}'
        s3.upload_file(file_path_jpg, bucket_name, s3_key_jpg)


def background_task(symbol, company_name, sent_time):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()

    # update the label to 0(processing)
    update_processing_sql = "UPDATE Ashares_data SET label = 0 WHERE symbol_market = ?"
    cursor.execute(update_processing_sql, (symbol,))
    conn.commit()

    # tasks for long time
    result = generate_total_report(symbol, company_name, sent_time)

    # update the label to 1 or 2(completed)
    if result == "Insufficient Info":
        update_completed_sql = "UPDATE Ashares_data SET label = 2 WHERE symbol_market = ?"
        cursor.execute(update_completed_sql, (symbol,))
    else:
        conn_s3(result)
        update_completed_sql = "UPDATE Ashares_data SET label = 1 WHERE symbol_market = ?"
        cursor.execute(update_completed_sql, (symbol,))
    conn.commit()

    conn.close()


