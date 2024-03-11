import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from full_report_pdf import generate_total_report

#####################################################
path_to_db = "Ashares.sqlite3"
#####################################################
def get_heat_list():
    url = "https://www.moomoo.com/quote/cn/most-active-stocks?from=futunn"

    # 发送GET请求获取页面内容
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=HEADERS)
    # 使用Beautiful Soup解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize lists to store data
    rank_list = []
    symbol_list = []
    company_name_list = []

    head_list = soup.find("div", class_="content-main")
    table = head_list.find_all("a", class_="list-item")
    for row in table:
        left_item = row.find('div', class_="fix-left")
        rank = left_item.find('span', class_="order").get_text()
        symbol = left_item.find('span', class_="code ellipsis").get_text()
        company_name = left_item.find('span', class_="name ellipsis").get_text()

        rank_list.append(rank)
        symbol_list.append(symbol)
        company_name_list.append(company_name)

    df = pd.DataFrame({
        'rank': rank_list,
        'symbol': symbol_list,
        'company_name': company_name_list
    })
    # print(df)
    return df

def generate_heat_list_stock_reports():
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()

    df = get_heat_list()
    df_head = df.head(10)
    for index, row in df_head.iterrows():
        rank = row['rank']
        symbol = row['symbol']
        cursor.execute("SELECT symbol_market, company_name FROM Ashares_data WHERE symbol = ?", (symbol,))
        result = cursor.fetchone()
        if result:
            symbol, company_name = result
            print(f"我们正在生成股票热榜第{rank}名: 股票{company_name}({symbol})的研报...")
            info = generate_total_report(symbol, company_name)
            print(info)
        else:
            print("找不到您输入的股票，请检查A股的股票代码或股票名称...")


# # Example
# generate_heat_list_stock_reports()




