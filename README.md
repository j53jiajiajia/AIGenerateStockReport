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
Please make sure that you have run  
pip install -r requirements.txt  
and put KaiTi.ttf, KaiTi-Bold.ttf, and SimHei.ttf in the Lib\site-packages\reportlab\fonts file directory and (/usr/share/fonts/KaiTi if you use ubuntu) before you run the code.
### OpenAI Key:
You should have one OpenAI Key and have .env to store OPENAI_API_KEY(OPENAI_API_KEY=******************************).
## Details
Coverage: 90%+ A shares  
Time: about 5 minutes per report  
Cost: 0.066 US dollars (0.02 + 0.03 + 0.001 + 0.002 + 0.001 + 0.002 + + 0.01) = 0.5 RMB  
## Chinese Promotion Introduction
🌟【新上功能|AI自动生成股票研报】🌟  
🔍【深度分析，洞察市场脉动】AI研报，汇聚大数据分析，洞悉行业趋势，为您提供全面而深入的市场分析。每一份研报，都是对过往数据的精准梳理，对未来走势的合理预测。  
💡【实时更新，把握第一手资讯】股市变幻莫测，AI研报实时更新，让您随时掌握最新的市场动态，及时做出明智的投资决策。  
📈【AI助力，客观大数据分析】在这个信息爆炸的时代，让AI研报成为您的智慧助手，用客观大数据分析，助您投资路上更加稳健前行！  
🚀【个性化定制，贴合合作方需求】可根据合作方需要，为您个性化生成股票研报。数据实时准确，分析客观可靠。欢迎私信合作！  
🔥每周免费分享3篇AI研报，加入群聊即可免费获得股票热榜前10只股票的AI研报
