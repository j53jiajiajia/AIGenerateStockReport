# AIGenerateStockReport

## Introduction
This tool uses GPT to generate the stock research report automatically given by stock symbol or company name. It will take about 5 minutes to generate one stock research report. 
## Generation Method 
### main.py: 
If you want to give one stock symbol or company name and generate the stock research report, please use main.py.(Examples: process_user_input('600223.SH') or process_user_input('山西汾酒'))
### main_heat_list.py: 
If you want to generate the stock research reports for the top 10 hottest stocks, please use main_heat_list.py.(Example: generate_heat_list_stock_reports())
## Notice
### Packages: 
Please make sure that you have already pip install relative packages and put 华文楷体.ttf, 华文楷体-Bold.ttf, 华文黑体.ttf in the Lib\site-packages\reportlab\fonts file directory before you run the code.
### OpenAI Key:
You should have one OpenAI Key and replace the get_openai() in the code with your key because our get_keys.py was not uploaded.
