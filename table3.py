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
    
    i = 0
    while i < 3:
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
        print(content)

        # Extract the rating and target price
        rating_match = re.search(r"股票评级：(\w+)", content)
        target_price_match = re.search(r"目标价格：(\d+)", content)

        if rating_match and target_price_match:
            break
        i += 1

    dict_prediction = {}
    dict_prediction['股票评级'] = rating_match.group(1) if rating_match else "暂无"
    dict_prediction['目标价格'] = target_price_match.group(1) if target_price_match else "暂无"
    
    # print(dict_prediction)
    return dict_prediction

def draw_prediction_table(dict_report_content, symbol, name):
    dict_prediction = generate_prediction(dict_report_content, name)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(3.0, 0.5))
    ax.axis('off')  # 关闭坐标轴
    # Create a Rectangle patch
    rect = patches.Rectangle((0.01, 0.01), 0.98, 0.9, linewidth=2, edgecolor='w', facecolor='w')

    # Add text inside the rectangle
    for i, (key, value) in enumerate(dict_prediction.items()):
        text = f"{key}: {value}"
        ax.text(0.05, 0.9 - i * 0.8, text, color='black', fontsize=14, weight='bold')


    # Add the patch to the Axes
    ax.add_patch(rect)

    # plt.show()
    image_path = f"图片/table3图片/table3_{name}({symbol}).jpg"
    fig.savefig(image_path, dpi=400, bbox_inches='tight', pad_inches=0.05)

    
# # Text content for the PDF
# dict_report_content = {
#     "名字代码": "宁德时代(300750.SZ)",
#     "出版时期": "2023-12-10",
#     "昨收盘: ": "167.99",
#     "报告标题": "财报稳健展商智，市场占有显领骥",
#     "核心要点": "宁德时代在2023年第三季度维持了稳健的财务业绩，增长势头保持良好，其中第三季度实现营业收入1054亿元，同比增长8%，环比增长5%，表明公司保持了逐季增长的态势。尽管如此，归母净利润出现较上季度4%的小幅下降，降至104亿元，但与去年同期相比也实现了11%的增长。这一结果显示出宁德时代即便在市场竞争加剧和成本压力可能增大的外部环境下，依然能够保持利润增长，并巩固其在动力电池行业中的领先地位。",
#     "点评分析": "宁德时代的第三季度业绩稳健，显示其盈利能力和市场份额的持续增长。第三季度实现归母净利润104.3亿元，同比增长10.7%，与公司在全球动力电池装机量达158.3GWh，市占率提升到36.9%的强劲表现相协调。毛利率也从上半年的21.6%提升到Q3的22.4%，体现出公司对成本控制的优秀管控能力。公司的这一系列财务指标集中体现了它作为电池制造行业领导者的地位。\n产品创新和研发投入是宁德时代业绩增长的关键驱动因素。前三季度研发投入增长40.7%，达到148.8亿元，这促进了如神行超充电池等新技术的研发和推广。神行超充电池支持10分钟内充电至80%SOC，体现了公司在快充技术方面的领先地位，此举有望成为新产品销售的强大推动力，提升公司的盈利能力和市场竞争力。\n宁德时代的全球业务扩展为其市场份额提升奠定了坚实基础。该公司在中美欧以外地区的动力电池市场占率达27.2%，同比大幅提升9.8%，并且在欧洲市场占有率也有持续大幅提升，目前已达34.9%。得益于与大众、Stellantis等欧系本土车企的密切合作以及矿产资源业务的开展，预计公司在全球市场的份额和盈利能力将继续保持上升趋势。",
#     "估值预测": "股票宁德时代300750.SZ当前市盈率(PE)为：16.18，预计该公司市盈率为：13.30，当前市盈率高于预计市盈率；当前市净率(PE)为：3.99；息税折旧摊销前利润(EBITDA)为：10.06。\n截至2023年12月10日，根据近三个月内48位分析师对宁德时代股票的评级判断，普遍给予强烈买入的建议。其中，有87.50%的分析师认定强烈买入，12.50%的分析师建议买入，没有分析师给出持有、未达标或卖出的建议。宁德时代的平均目标股价预计为330.10元，最高可能达到712.00元，而最低目标价设定在239.02元。考虑到当前股价为163.59元，市场对该公司股票的增值潜力保持高度信心，呈现出强烈的买入信号。",
#     "风险提示": "原材料成本上涨风险、电动汽车市场需求疲软、储能产品销售不达标",
#     "全部文本": "股票宁德时代300750.SZ当前市盈率(PE)为：16.18，预计该公司市盈率为：13.30，当前市盈率高于预计市盈率；当前市净率(PE)为：3.99；息税折旧摊销前利润(EBITDA)为：10.06。\n截至2023年12月10日，根据近三个月内48位分析师对宁德时代股票的评级判断，普遍给予强烈买入的建议。其中，有87.50%的分析师认定强烈买入，12.50%的分析师建议买入，没有分析师给出持有、未达标或卖出的建议。宁德时代的平均目标股价预计为330.10元，最高可能达到712.00元，而最低目标价设定在239.02元。考虑到当前股价为163.59元，市场对该公司股票的增值潜力保持高度信心，呈现出强烈的买入信号。"
# }

# draw_prediction_table(dict_report_content, '300750.SZ', "宁德时代")