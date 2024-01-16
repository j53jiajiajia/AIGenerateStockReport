from generate_idea import generate_main_idea
from generate_idea import generate_comment_idea
from generate_idea import generate_risk_warning
from get_research_report import get_two_reports
from get_analyst_estimation import get_analyst_analysis
from get_valuation import get_valuation
from openai import OpenAI
import yfinance as yf
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def generate_report_title(symbol, name, dict_target_text1, dict_target_text2, all_content_text):
    title1 = dict_target_text1["title"]
    title2 = dict_target_text2["title"]

    # make openai to generate comment idea for our report
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
          {"role": "user", "content": f"{all_content_text}\n这是{name}{symbol}股票研究报告的内容，请为它起一个标题，标题应官方正式，由尽量押韵的短句组成，标题字数在10~20字左右，比如：{title1}，或者，{title2}\n请注意，你应只返回研究报告的标题，不需要含有任何提示词(比如，研究报告的标题为：；{name}{symbol}分析：)"}
        ]
    )
    content = response.choices[0].message.content.strip()
    # print(content)
    return content

def generate_report_text(symbol, name):
    dict_report_content = {}
    dict_target_text1, dict_target_text2 = get_two_reports(symbol)
    if dict_target_text1 and dict_target_text2:
        dict_report_content["核心要点"] = generate_main_idea(symbol, name, dict_target_text1, dict_target_text2)
        dict_report_content["点评分析"] = generate_comment_idea(symbol, name, dict_target_text1, dict_target_text2)
        dict_report_content["估值预测"] = get_valuation(symbol, name)
        dict_report_content["估值预测"] += "\n" + get_analyst_analysis(symbol, name) if get_valuation(symbol, name) != "" else get_analyst_analysis(symbol, name)
        dict_report_content["风险提示"] = generate_risk_warning(symbol, name, dict_target_text1, dict_target_text2)
        all_content_text = ""
        for subtitle, content in dict_report_content.items():
            all_content_text += subtitle + "\n"
            all_content_text += content + "\n"
        print(all_content_text)
        dict_report_content["报告标题"] = generate_report_title(symbol, name, dict_target_text1, dict_target_text2, all_content_text)
        dict_report_content["出版时期"] = datetime.now().strftime("%Y-%m-%d")
        dict_report_content["股票代码"] = symbol
        dict_report_content["股票名称"] = name
        dict_report_content["名字代码"] = f"{name}({symbol})"
        # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
        if symbol[-3:] == '.SH':
            symbol = symbol.replace('.SH', '.SS')
        dict_report_content["昨收盘: "] = str(round(yf.Ticker(symbol).history(period="2d")['Close'].iloc[0], 2))

        all_text = ""
        for subtitle, content in dict_report_content.items():
            all_text += subtitle + "\n"
            all_text += str(content) + "\n"
        # print(all_text)
        return dict_report_content
    else:
        return None


# generate_report_text('300750.SZ', "宁德时代“)






