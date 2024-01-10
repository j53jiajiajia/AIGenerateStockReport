import yfinance as yf

def get_valuation(symbol, name):
    # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
    if symbol[-3:] == '.SH':
        symbol = symbol.replace('.SH', '.SS')

    info = yf.Ticker(symbol).info
    current_pe = float(info.get('trailingPE', 'N/A')) if info.get('trailingPE') is not None else 'N/A'
    estimated_pe = float(info.get('forwardPE', 'N/A')) if info.get('forwardPE') is not None else 'N/A'
    current_pb = float(info.get('priceToBook', 'N/A')) if info.get('priceToBook') is not None else 'N/A'
    ev = float(info.get('enterpriseValue', 'N/A')) if info.get('enterpriseValue') is not None else 'N/A'
    ebitda = float(info.get('ebitda', 'N/A')) if info.get('ebitda') is not None else 'N/A'
    # Calculate EV/EBITDA
    if ev != 'N/A' and ebitda != 'N/A' and ebitda != 0:  # Ensure values are valid and avoid division by zero
        ev_ebitda = ev / ebitda
    else:
        ev_ebitda = 'N/A'  # If data is not available or invalid
    if current_pe != 'N/A' and estimated_pe != 'N/A' and current_pb != 'N/A' and ev != 'N/A' and ebitda != 'N/A':
        message = f"股票{name}({symbol})当前市盈率(PE)为：{current_pe:.2f}，预计该公司市盈率为：{estimated_pe:.2f}，当前市盈率高于预计市盈率；当前市净率(PB)为：{current_pb:.2f}；企业价值对息税折旧摊销前利润的比率(EV/EBITDA)为：{ev_ebitda:.2f}。"
    elif estimated_pe == 'N/A':
        message = f"股票{name}({symbol})当前市盈率(PE)为：{current_pe:.2f}；当前市净率(PB)为：{current_pb:.2f}；企业价值对息税折旧摊销前利润的比率(EV/EBITDA)为：{ev_ebitda:.2f}。"
    else:
        message = ""
    return message

# # Example usage:
# symbol = "002415.SZ"  # Stock symbol
# name = "海康威视"  # Stock name
# get_valuation(symbol, name)