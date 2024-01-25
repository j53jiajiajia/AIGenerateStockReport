from openai import OpenAI
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from dotenv import load_dotenv
load_dotenv()

plt.rcParams["font.sans-serif"] = ["STKaiTi"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

def generate_prediction(dict_report_content, name):
    all_content_text = dict_report_content["全部文本"]
    
    # make openai to generate rating and target price
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
    )
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
          {"role": "user", "content": f"{all_content_text}\n以上是股票{name}的研报的主要内容，请仔细阅读，然后以一个金融分析师的角度，给出股票{name}的评级(买入/增持/持有/减持/卖出)和目标价格，请注意你给出的目标价格不能是平均目标股价，你应只返回你给出的股票评级和目标价格，且返回内容的格式为: ****股票评级：？\n****目标价格：？。"}
        ]
    )
    content = response.choices[0].message.content.strip()
    # print(content)

    # Extract the rating and target price
    rating_match = re.search(r"股票评级：(\w+)", content)
    target_price_match = re.search(r"目标价格：(\d+)", content)

    dict_prediction = {}
    dict_prediction['股票评级'] = rating_match.group(1) if rating_match else "暂无"
    dict_prediction['目标价格'] = target_price_match.group(1) if target_price_match else "暂无"
    
    # print(dict_prediction)
    return  dict_prediction

def draw_prediction_table(dict_report_content, symbol, name):
    dict_prediction = generate_prediction(dict_report_content, name)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(3.0, 1.5))
    ax.axis('off')  # 关闭坐标轴
    # Create a Rectangle patch
    rect = patches.Rectangle((0.01, 0.01), 0.98, 0.9, linewidth=2, edgecolor='w', facecolor='w')

    # Add text inside the rectangle
    for i, (key, value) in enumerate(dict_prediction.items()):
        text = f"{key}: {value}"
        ax.text(0.05, 0.7 - i * 0.4, text, color='black', fontsize=14, weight='bold')


    # Add the patch to the Axes
    ax.add_patch(rect)

    # plt.show()
    image_path = f"图片/table3图片/table3_{name}({symbol}).jpg"
    fig.savefig(image_path, dpi=400, bbox_inches='tight', pad_inches=0.05)


# draw_prediction_table(dict_report_content, 600519.SH', "贵州茅台")