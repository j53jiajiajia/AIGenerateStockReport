import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def get_analyst_data(symbol):
    # 根据url对symbol的格式进行调整
    symbol = symbol.replace('.', '-')
    url = f"https://www.moomoo.com/stock/{symbol}/analysis"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # get the analyst rating of the given stock
    analyst_rating_text = ""
    analyst_rating_text += "Up to " + soup.find('p', class_='updated-time').get_text() + "，"
    analyst_rating_text += soup.find('p', class_='analyst-desc').get_text().strip() + "，"
    analyst_rating_text += "the overall rating is " + soup.find('div', class_='analyse-rating-score').get_text().strip() + ". "
    if len(soup.find_all('span', class_='rating-num')) == 3:
        analyst_rating_text += "To be specific, " + soup.find_all('span', class_='rating-num')[0].get_text() + " of analysts gave Buy, " + soup.find_all('span', class_='rating-num')[1].get_text() + " of analysts gave Hold, " + soup.find_all('span', class_='rating-num')[2].get_text() + " of analysts gave Sell. "
    if len(soup.find_all('span', class_='rating-num')) == 5:
        analyst_rating_text += "To be specific, " + soup.find_all('span', class_='rating-num')[0].get_text() + " of analysts gave Strong Buy, " + soup.find_all('span', class_='rating-num')[1].get_text() + " of analysts gave Buy, " + soup.find_all('span', class_='rating-num')[2].get_text() + " of analysts gave Hold, " + soup.find_all('span', class_='rating-num')[3].get_text() + " of analysts gave Underperform, " + soup.find_all('span', class_='rating-num')[4].get_text() + " of analysts gave Sell. "
    # print(analyst_rating_text)

    # get the analyst stock price target of the given stock
    analyst_price_text = ""
    analyst_price_text += "Up to " + soup.find('p', class_='updated-time').get_text() + ", "
    analyst_price_text += soup.find('p', class_='tarrget-desc').get_text() + ", " if soup.find('p', class_='tarrget-desc') else "None, "
    analyst_price_text += "Current price is " + soup.find('div', class_='price-normal').get_text().split()[0] + ". "
    # print(analyst_price_text)

    analyst_data = analyst_rating_text + "\n" + analyst_price_text
    # print(analyst_data)
    return analyst_data

def get_analyst_analysis(symbol, name):
    analyst_data = get_analyst_data(symbol)

    # make openai to make analysis of the analyst data
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
          {"role": "user", "content": f"{analyst_data}\n这是分析师们对{name}股票的评级和预测(日期为月/日/年），请仔细阅读，对这些信息进行总结和分析，为该股票的研究报告的生成一段100字左右估值分析。\n请注意，生成的文字应全为中文；语气应官方正式；你将仅直接返回一段话且你的回答不要包含提示语(比如：估值分析为：)。比如，你的返回的内容为：\n截至2023年12月10日，根据48位分析师在过去三个月对宁德时代股票的评级，整体评级为强烈买入。具体来说，87.50%的分析师给出强烈买入评级，12.50%的分析师给出买入评级，没有分析师给出持有、减持或卖出评级。此外，宁德时代的平均目标股价为330.10元，最高估值为712.00元，最低估值为239.02元，而当前股价为163.59元。这一数据表明市场对宁德时代的股票前景持乐观态度，分析师们普遍认为其股价具有显著上升空间，是投资者关注的重点。"}
        ]
    )
    content = response.choices[0].message.content.strip()
    # print(content)
    return content

# get_analyst_analysis('00700-HK')