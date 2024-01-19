import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import matplotlib.pyplot as plt

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def get_rating_details(symbol):
    symbol = symbol.split(".")[0]
    url = f'https://data.eastmoney.com/report/{symbol}.html'
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        script = soup.find(lambda tag: tag.name == "script" and "var initdata =" in tag.text)
        # print(script)
        if script:
            json_text = re.search(r'var initdata =(.*?)};', script.text).group(1)
            json_text += '}'
            # print(json_text)
            data = json.loads(json_text)['data']
            df = pd.DataFrame(data)
            # Selecting specific columns for making rating table
            df = df[['orgSName', 'emRatingName', 'publishDate']]
            # Rename the columns
            df = df.rename(columns={'orgSName': '机构名称', 'emRatingName': '评级', 'publishDate': '发布日期'})
            # Format the '发布日期' column to year-month-day format
            df['发布日期'] = pd.to_datetime(df['发布日期']).dt.strftime('%Y-%m-%d')

            return df
        else:
            print("无机构评级信息")
    except Exception as e:
        print(f"Error: {e}")
        return None


def draw_rating_details_table(symbol, name):
    plt.rcParams["font.sans-serif"] = ["STKaiTi"]  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

    df = get_rating_details(symbol)
    # print(df)
    df_head = df.head(5)
    # print(df_head)
    # Creating the figure and axis.
    fig, ax = plt.subplots(figsize=(3, 1.5), dpi=400)
    ax.axis('off')  # Do not display axis

    cell_text = df_head.values.tolist()
    table = ax.table(cellText=cell_text, colLabels=df_head.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)

    # Make the table lines invisible
    for key, cell in table.get_celld().items():
        cell.set_linewidth(0)

    for col in range(len(df_head.columns)):
        cell = table[(0, col)]
        cell.set_edgecolor('black')
        cell.set_linestyle('-')
        cell.set_linewidth(1.5)
        cell.visible_edges = 'B'

    image_path = f"图片/table2图片/table2_{name}({symbol}).jpg"
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0.05)

# get_rating_details('000338.SZ')