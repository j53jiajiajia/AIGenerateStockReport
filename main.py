import sqlite3
from full_report_pdf import generate_total_report

#####################################################
path_to_db = "Ashares.sqlite3"
#####################################################

def process_user_input(s):
    s = s.replace(" ", "")
    s = s.replace("\t", "")

    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()

    first_six = s[:6]
    if len(s) >= 6 and first_six.isdigit():
        cursor.execute("SELECT symbol_market, company_name FROM Ashares_data WHERE symbol = ?", (s[:6],))
    else:
        cursor.execute("SELECT symbol_market, company_name FROM Ashares_data WHERE company_name = ?", (s,))
    result = cursor.fetchone()
    # print(result)
    if result:
        symbol, company_name = result
        print(f"我们正在生成股票{company_name}({symbol})的研报...")
        generate_total_report(symbol, company_name)
    else:
        print("找不到您输入的股票，请重新输入A股的股票代码或股票名称...")

    conn.close()

# Examples
process_user_input('比亚迪')
# process_user_input('长白山')
# process_user_input('贵州茅台')
# process_user_input('万科Ａ')
# process_user_input('五芳斋')
# process_user_input('000078.SZ')    #找不到相关信息的股票
# process_user_input('阳光电源')
# process_user_input('老板电器')
# process_user_input('000338.SZ')
# process_user_input('600223.SH')
# process_user_input('山西汾酒')



