import os
import boto3
from dotenv import load_dotenv
load_dotenv()

def presigned_url(company_name, symbol, sent_time, kind, suffix=''):
    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv('aws_access_key_id'),
                      aws_secret_access_key=os.getenv('aws_secret_access_key'),
                      region_name='ap-southeast-1')
    bucket_name = 'stockresearchreport'

    # 根据文件路径生成S3键名
    s3_key = f'stock_research_report_{kind}/{company_name}({symbol})研究报告({sent_time}){suffix}.{kind}'

    # 生成预签名上传URL
    presigned_url = s3.generate_presigned_url('get_object',
                                              Params={'Bucket': bucket_name, 'Key': s3_key, 'ResponseContentDisposition': 'inline'},
                                              ExpiresIn=3600,  # URL有效期为3600秒
                                              HttpMethod='GET')
    # print(presigned_url)
    return presigned_url

import requests

# # # 你的预签名URL
# presigned_url = presigned_url('宁德时代', '300750.SZ', '2024-03-10', 'pdf')







