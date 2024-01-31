import yfinance as yf
import matplotlib.pyplot as plt
from pathlib import Path

def draw_stock_data_table(symbol, name):

    plt.rcParams["font.sans-serif"] = ['STKaiti']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

    # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
    if symbol[-3:] == '.SH':
        symbol = symbol.replace('.SH', '.SS')

    # 初始化 yfinance 对象
    stock = yf.Ticker(symbol)

    # 获取基本信息
    info = stock.info
    # print(info)

    # 总股本（单位：百万股）
    total_shares = int(info.get('sharesOutstanding', 0) // 1e6)

    # 总市值（单位：百万元）
    total_market_cap = int(info.get('marketCap', 0) // 1e6)

    hist = stock.history(period='1y')
    # print(hist)
    # 12个月最高价和最低价
    high_52_week = round(hist['High'].max(), 2)
    low_52_week = round(hist['Low'].min(), 2)


    close_price = round(yf.Ticker(symbol).history(period="2d")['Close'].iloc[0], 2)

    # # 打印数据
    # print(f"昨日收盘价（元）: {close_price}")
    # print(f"总股本（百万股）: {total_shares}")
    # print(f"总市值（百万元）: {total_market_cap}")
    # print(f"12个月最高价（元）: {high_52_week}")
    # print(f"12个月最低价（元）: {low_52_week}")


    # Sample data for the table
    data = {
        "昨日收盘价（元）": close_price,
        "总股本（百万股）": total_shares,
        "总市值（百万元）": total_market_cap,
        "12个月最高价（元）": high_52_week,
        "12个月最低价（元）": low_52_week,
    }

    # 创建一个无表头和无框线的表格
    fig, ax = plt.subplots(figsize=(2.5, 1))
    ax.axis('off')  # 关闭坐标轴

    # 计算表格内容的纵向位置
    y_positions = [0.9 - 0.2 * i for i in range(len(data))]

    # 绘制表格内容，左对齐且右对齐
    for key, value in data.items():
        key_text = ax.text(0.00, y_positions.pop(0), key, fontsize=8, ha="left")
        value_text = ax.text(1.00, key_text.get_position()[1], value, fontsize=8, ha="right")

    # 添加表名
    # ax.text(0.5, 0.9, "股票数据", fontsize=12, fontweight="bold", ha="center")

    image_path = f"图片/table1图片/table1_{name}({symbol}).jpg"
    fig.savefig(image_path, dpi=400, bbox_inches='tight', pad_inches=0.05)
    # # 显示图表
    # plt.show()

# draw_stock_data_table("300750.SZ", "宁德时代")