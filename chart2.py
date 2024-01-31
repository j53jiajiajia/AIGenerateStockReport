import yfinance as yf
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Polygon, FancyBboxPatch
import numpy as np


# Function to calculate SMA
def sma(data):
    sma_10 = data['Close'].rolling(window=10).mean()
    sma_20 = data['Close'].rolling(window=20).mean()
    
    data['SMA_10_signal'] = 0
    data['SMA_10_signal'] = np.where(data['Close'] > sma_10, 1, data['SMA_10_signal'])  
    data['SMA_10_signal'] = np.where(data['Close'] < sma_10, -1, data['SMA_10_signal']) 
    data['SMA_20_signal'] = 0
    data['SMA_20_signal'] = np.where(data['Close'] > sma_20, 1, data['SMA_20_signal'])  
    data['SMA_20_signal'] = np.where(data['Close'] < sma_20, -1, data['SMA_20_signal']) 

# Function to calculate RSI
def rsi(data):
    rsi_6 = ta.momentum.RSIIndicator(data['Close'], window=6).rsi()
    rsi_12 = ta.momentum.RSIIndicator(data['Close'], window=12).rsi()
    rsi_24 = ta.momentum.RSIIndicator(data['Close'], window=24).rsi()
    
    data['RSI_6_signal'] = 0
    data['RSI_6_signal'] = np.where(rsi_6 < 30, 1, data['RSI_6_signal'])  
    data['RSI_6_signal'] = np.where(rsi_6 > 70, -1, data['RSI_6_signal']) 
    data['RSI_12_signal'] = 0
    data['RSI_12_signal'] = np.where(rsi_12 < 30, 1, data['RSI_12_signal'])  
    data['RSI_12_signal'] = np.where(rsi_12 > 70, -1, data['RSI_12_signal']) 
    data['RSI_24_signal'] = 0
    data['RSI_24_signal'] = np.where(rsi_24 < 30, 1, data['RSI_24_signal'])  
    data['RSI_24_signal'] = np.where(rsi_24 > 70, -1, data['RSI_24_signal']) 

# Function to calculate MACD
def macd(data):
    macd = ta.trend.MACD(data['Close'], window_slow=26, window_fast=12, window_sign=9)
    MACD_diff = macd.macd_diff()
    
    data['MACD_signal'] = 0
    data['MACD_signal'] = np.where(MACD_diff > 0, 1, data['MACD_signal'])  
    data['MACD_signal'] = np.where(MACD_diff < 0, -1, data['MACD_signal']) 

# Function to calculate BOLL    
def bollinger(data):
    indicator_bollinger = ta.volatility.BollingerBands(close=data['Close'], window=20, window_dev=2)
    Bollinger_hband = indicator_bollinger.bollinger_hband() # Upper Band
    Bollinger_lband = indicator_bollinger.bollinger_lband() # Lower Band
    
    data['BOLL_signal'] = 0
    data['BOLL_signal'] = np.where(data['Close'] < Bollinger_lband, 1, data['BOLL_signal'])  
    data['BOLL_signal'] = np.where(data['Close'] > Bollinger_hband, -1, data['BOLL_signal']) 

# Function to calculate SAR
def sar(data):
    sar_indicator = ta.trend.PSARIndicator(data['High'], data['Low'], data['Close'], step=0.02, max_step=0.2)
    sar = sar_indicator.psar()
    
    data['SAR_signal'] = 0
    data['SAR_signal'] = np.where(data['Close'] > sar, 1, data['SAR_signal'])  # 价格在SAR之上，买入信号
    data['SAR_signal'] = np.where(data['Close'] < sar, -1, data['SAR_signal']) # 价格在SAR之下，卖出信号

# Function to calculate KDJ
def kdj(data):
    stochastic = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'], window=14, smooth_window=3)
    stoch_D = stochastic.stoch_signal()
    
    data['KDJ_signal'] = 0
    data['KDJ_signal'] = np.where(stoch_D < 20, 1, data['KDJ_signal'])  
    data['KDJ_signal'] = np.where(stoch_D > 80, -1, data['KDJ_signal']) 

# Function to calculate PSY
def psy(data):
    up_price = pd.Series(np.where(data['Close'] > data['Close'].shift(1), 1, 0), index=data.index)
    psy = up_price.rolling(window=14).sum() / 14 * 100
    
    data['PSY_signal'] = 0
    data['PSY_signal'] = np.where(psy < 25, 1, data['PSY_signal'])  # PSY above threshold, buy signal
    data['PSY_signal'] = np.where(psy > 75, -1, data['PSY_signal']) # PSY below threshold, sell signal
    

def draw_dashboard_and_matrix(lastest_signal, lastest_details, symbol, name):
    # Create the figure and axis
    fig = plt.figure(figsize=(3, 3))
    ax = fig.add_subplot(1, 1, 1)

    # draw the dashboard
    # Draw the wedges
    # wedges = [
    #     (0, 60, 'lightgreen'),    
    #     (60, 120, 'grey'),
    #     (120, 180, '#ff9999')   
    # ]
    wedges = [
        (0, 60, 'red'),    
        (60, 120, 'grey'),
        (120, 180, 'green')   
    ]
    for min_angle, max_angle, color in wedges:
        ax.add_patch(Wedge(center=(0.5, 0.5), r=0.5, theta1=min_angle, theta2=max_angle, color=color))

    # Draw the center circle
    center_circle = plt.Circle((0.5, 0.5), 0.42, color='white')
    ax.add_artist(center_circle)

    total_signal = lastest_signal['total_signal']
    pointer_angle = 180 - ((total_signal + 10) * (180 / 20))
    # Draw the pointer
    angle_rad = np.deg2rad(pointer_angle)
    x = 0.5 + 0.4 * np.cos(angle_rad)
    y = 0.5 + 0.4 * np.sin(angle_rad)
    pointer = Polygon([(0.5, 0.5), (x, y), (0.5, 0.5 - 0.01)], closed=True, color='black')
    ax.add_patch(pointer)

    sentiment = "中性" if -3 <= total_signal <= 3 else ("看跌" if total_signal < -3 else "看涨")
    # Draw the text
    plt.text(0.05, 0.45, '看跌', horizontalalignment='center', verticalalignment='center', fontsize=10)
    plt.text(0.95, 0.45, '看涨', horizontalalignment='center', verticalalignment='center', fontsize=10)
    plt.text(0.5, 0.35, f'市场情绪: {sentiment}', horizontalalignment='center', verticalalignment='center', fontsize=18, weight='bold')

    # draw the matrix
    i = 0
    for column, value in lastest_details.items():
        if i < 5:
            if value == -1:
                rectangle = FancyBboxPatch((0.04 + i*0.2, 0.18), 0.09, 0.04, boxstyle="round,pad=0.04", color='green', ec="none")
            elif value == 0:
                rectangle = FancyBboxPatch((0.04 + i*0.2, 0.18), 0.09, 0.04, boxstyle="round,pad=0.04", color='grey', ec="none")
            else:
                rectangle = FancyBboxPatch((0.04 + i*0.2, 0.18), 0.09, 0.04, boxstyle="round,pad=0.04", color='red', ec="none")
            print(f"The value in column '{column}' is {value}.")
            ax.add_patch(rectangle)
            plt.text(0.08+ i*0.2, 0.19, column, horizontalalignment='center', verticalalignment='center', fontsize=8, weight='bold')
        else:
            if value == -1:
                rectangle = FancyBboxPatch((0.04 + (i-5)*0.2, 0.04), 0.09, 0.04, boxstyle="round,pad=0.04", color='green', ec="none")
            elif value == 0:
                rectangle = FancyBboxPatch((0.04 + (i-5)*0.2, 0.04), 0.09, 0.04, boxstyle="round,pad=0.04", color='grey', ec="none")
            else:
                rectangle = FancyBboxPatch((0.04 + (i-5)*0.2, 0.04), 0.09, 0.04, boxstyle="round,pad=0.04", color='red', ec="none")
            print(f"The value in column '{column}' is {value}.")
            ax.add_patch(rectangle)
            plt.text(0.08+ (i-5)*0.2, 0.048, column, horizontalalignment='center', verticalalignment='center', fontsize=8, weight='bold')
        i += 1

    ax.set_aspect('equal')
    ax.axis('off')

    file_path = f"图片/chart2图片/chart2_{name}({symbol}).jpg"
    fig.savefig(file_path, dpi=400, bbox_inches='tight', pad_inches=0.05)

    plt.show()

def draw_technical_indicators(symbol, name):
    # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
    if symbol[-3:] == '.SH':
        symbol = symbol.replace('.SH', '.SS')
    data = yf.download(symbol, period='6mo', interval='1d')
    # print(data['Close'])
    
    sma(data)
    rsi(data)
    macd(data)
    bollinger(data)
    sar(data)
    kdj(data)
    psy(data)
    signal_data = data[['SMA_10_signal', 'SMA_20_signal', 'RSI_6_signal', 'RSI_12_signal', 'RSI_24_signal', 'MACD_signal', 'BOLL_signal', 'SAR_signal', 'KDJ_signal', 'PSY_signal']]
    signal_data = signal_data.copy()
    signal_data['total_signal'] = np.sum(signal_data.values, axis=1)
    lastest_signal = signal_data.iloc[-1]
    # print(lastest_signal)
    details = data[['SMA_10_signal', 'SMA_20_signal', 'RSI_6_signal', 'RSI_12_signal', 'RSI_24_signal', 'MACD_signal', 'BOLL_signal', 'SAR_signal', 'KDJ_signal', 'PSY_signal']].rename(columns={'SMA_10_signal': 'SMA(10)', 'SMA_20_signal': 'SMA(20)', 'RSI_6_signal': 'RSI(6)', 'RSI_12_signal': 'RSI(12)', 'RSI_24_signal': 'RSI(24)', 'MACD_signal': 'MACD', 'BOLL_signal': 'BOLL', 'SAR_signal': 'SAR', 'KDJ_signal': 'KDJ', 'PSY_signal': 'PSY'})
    lastest_details = details.iloc[-1]

    draw_dashboard_and_matrix(lastest_signal, lastest_details, symbol, name)

# draw_technical_indicators('300750.SZ', '宁德时代')