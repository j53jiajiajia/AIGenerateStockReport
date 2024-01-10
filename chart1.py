import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator

def draw_trend_chart(symbol, name):

    plt.rcParams["font.sans-serif"] = ["KaiTi"] #设置字体
    plt.rcParams["axes.unicode_minus"] = False #该语句解决图像中的“-”负号的乱码问题

    # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
    if symbol[-3:] == '.SH':
        symbol = symbol.replace('.SH', '.SS')

    # 定义沪深300指数代码
    ticker_hs300 = "000300.SS"   # 沪深300指数股票代码

    # 下载过去一年的数据
    symbol_data = yf.download(symbol, period="1y")
    hs300_data = yf.download(ticker_hs300, period="1y")
    # symbol_data = yf.download(ticker_ningde, start="2022-10-24", end="2023-10-24")
    # hs300_data = yf.download(ticker_hs300, start="2022-10-24", end="2023-10-24")


    # 计算每日收盘价的百分比变化
    symbol_pct_change = symbol_data['Close']/symbol_data['Close'].iloc[0] - 1
    # print(symbol_pct_change)
    hs300_pct_change = hs300_data['Close']/hs300_data['Close'].iloc[0] - 1

    # Close all open figures
    plt.close('all')
    # 绘图
    plt.figure(figsize=(2.5, 1.5))
    plt.plot(symbol_pct_change, label=symbol, color='blue')
    plt.plot(hs300_pct_change, label='沪深300', color='red')

    # 添加x轴 (y=0)
    plt.axhline(y=0, color='black', linewidth=1)

    # 移除上边框和右边框
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # 标题
    # plt.title('走势对比', fontsize=10, fontweight='bold')

    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    diff_pct_change = max(symbol_pct_change) - min(symbol_pct_change)
    plt.gca().yaxis.set_major_locator(MultipleLocator((diff_pct_change//0.6+1) * 0.05))  # 例如，每0.05（5%）一个刻度

    # 将y轴的标签格式化为百分比
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

    plt.legend(fontsize=6)
    plt.grid(False)

    image_path = f"图片/chart1图片/chart1_{name}({symbol}).jpg"
    plt.savefig(image_path, dpi=300, bbox_inches='tight')  # 保存图表为图像文件，设置dpi和边界以控制图像的清晰度和边距
    # plt.show()

# draw_trend_chart("300750.SZ", "宁德时代")
# draw_trend_chart("000858.SZ", "五粮液")
# draw_trend_chart("002230.SZ", "科大讯飞")