import sqlite3

#####################################################
path_to_db = "Ashares.sqlite3"
#####################################################

def input_processing(stock):
    stock = stock.replace(" ", "")
    stock = stock.replace("\t", "")

    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()

    first_six = stock[:6]
    if len(stock) >= 6 and first_six.isdigit():
        cursor.execute("SELECT symbol_market, company_name FROM Ashares_data WHERE symbol = ?", (stock[:6],))
    else:
        cursor.execute("SELECT symbol_market, company_name FROM Ashares_data WHERE company_name = ?", (stock,))
    result = cursor.fetchone()
    
    conn.close()
    return result
