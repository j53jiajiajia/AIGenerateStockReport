from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from input_processing import input_processing
import threading
from background_task import background_task
from presigned_url import presigned_url
from datetime import datetime, timedelta

#####################################################
path_to_db = "records.sqlite3"
#####################################################


app = Flask(__name__)
cors = CORS(app, resources={r"/submit": {"origins": "https://bangbangday.com"}})
cors = CORS(app, resources={r"/check": {"origins": "https://bangbangday.com"}})


@app.route('/submit', methods=['POST'])
def generate_report():
    data = request.get_json()
    user_id = data.get("user_id")
    service_id = data.get("service_id")
    timestamp = data.get("sent_time")
    utc_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    sent_time = (utc_time + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")[:10]
    # print(sent_time)
    user_input = data.get("user_input")
    stock = user_input.get("stock")
    print(f"Received the stock: {stock} on {sent_time} by {user_id} on {service_id}")

    # give response the front end first
    bucket_name = 'stockresearchreport'
    symbol = input_processing(stock)[0]
    company_name = input_processing(stock)[1]
    # s3_pdf = f'stock_research_report_pdf/{company_name}({symbol})研究报告({sent_time}).pdf'
    # s3_jpg1 = f'stock_research_report_jpg/{company_name}({symbol})研究报告({sent_time})_1.jpg'
    # s3_jpg2 = f'stock_research_report_jpg/{company_name}({symbol})研究报告({sent_time})_2.jpg'
    # url1 = f'https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}?region=ap-southeast-1&bucketType=general&prefix={s3_pdf}'
    # url2 = f'https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}?region=ap-southeast-1&bucketType=general&prefix={s3_jpg1}'
    # url3 = f'https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}?region=ap-southeast-1&bucketType=general&prefix={s3_jpg2}'
    
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    select_sql = "SELECT label FROM Ashares_data WHERE symbol_market = ?"
    cursor.execute(select_sql, (symbol,))
    label = cursor.fetchone()[0]
    conn.close()
    if label == 1:
        url1 = presigned_url(company_name, symbol, sent_time, 'pdf')
        url2 = presigned_url(company_name, symbol, sent_time, 'jpg', '_1')
        url3 = presigned_url(company_name, symbol, sent_time, 'jpg', '_2')
    else:
        url1, url2, url3 = '', '', ''
    response = {"user_id": user_id, "service_id": service_id, "label": label, "url1": url1, "url2": url2, "url3": url3}
    print(f"We will respond: {response}")

    # start thread in background to finish the task according to the label
    if label == -1:
        thread = threading.Thread(target=background_task, args=(symbol, company_name, sent_time))
        thread.start()

    return jsonify(response)
    


@app.route('/check', methods=['POST'])
def is_stock():
    data = request.get_json()
    user_input = data.get("user_input")
    stock = user_input.get("stock")

    result = input_processing(stock)
    if result:
        response = True
    else:
        response = False
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')