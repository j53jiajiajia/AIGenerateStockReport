import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams["font.sans-serif"] = ["STKaiTi"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题


def get_xtrafin_rating(symbol):
    # Define the URL for the API endpoint
    url = f'https://fin-gpt.org/analysis/{symbol}'
    # print(f"Requesting data from {url}...")
    # Make a GET request to the API
    response = requests.get(url)
    # Check the status of the response
    if response.status_code == 200:
        # The request was successful
        data = response.json()  # Parse JSON data from the response
        # print(f"Data received")
        # if 'error' in data:  # No data loaded for the symbol
        #     print(f"Error: {data['error']}")
        # else:  # Data is available
        #     print("get data successfully")

        # analysis = data['analysis']
        # client = OpenAI(
        #     api_key=get_openai(),
        # )
        #
        # response = client.chat.completions.create(
        #     model="gpt-4-1106-preview",
        #     messages=[
        #         {"role": "user",
        #          "content": f"{analysis}\n这是{symbol}股票的英文大模型分析，请把它翻译成中文。\n请注意，请直接返回中文翻译，不要有任何提示词，如：以下为翻译等"}
        #     ]
        # )
        dict_xtrafin = {}
        dict_xtrafin['技术评分'] = data['rating']
        dict_xtrafin['市场情绪'] = '积极' if data['sentiment'] == 'positive' else '中性' if data['sentiment'] == 'neutral' else '消极'
        dict_xtrafin['技术面分析'] = f'https://fin-gpt.org/symbol/{symbol}'

        # print(dict_xtrafin)
        return dict_xtrafin

# get_xtrafin_rating('300750.SZ')

def generate_xtrafin_rating(symbol, name):
    # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
    if symbol[-3:] == '.SH':
        symbol = symbol.replace('.SH', '.SS')

    dict_xtrafin = get_xtrafin_rating(symbol)
    # dict_xtrafin = {'技术评分': '50', '市场情绪': '消极', '详情分析': 'https://fin-gpt.org/symbol/300750.SZ'}

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(3.0, 1.5))
    ax.axis('off')  # 关闭坐标轴
    # Create a Rectangle patch
    rect = patches.Rectangle((0.01, 0.01), 0.98, 0.9, linewidth=2, edgecolor='w', facecolor='w')

    # Add text inside the rectangle
    for i, (key, value) in enumerate(dict_xtrafin.items()):
        text = f"{key}: {value}"
        if i == 0 or i == 1:
            ax.text(0.05, 0.7 - i * 0.3, text, color='black', fontsize=14, weight='bold')
        else:
            ax.text(0.05, 0.7 - i * 0.25, text, color='black', fontsize=6)


    # Add the patch to the Axes
    ax.add_patch(rect)

    # plt.show()
    image_path = f"图片/table3图片/table3_{name}({symbol}).jpg"
    fig.savefig(image_path, dpi=400, bbox_inches='tight', pad_inches=0.05)

# generate_xtrafin_rating('300750.SZ', "宁德时代")
