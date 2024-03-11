import akshare as ak
import sqlite3
from datetime import datetime

#####################################################
path_to_db = "Ashares.sqlite3"
#####################################################
def create_Ashares_table(path_to_db):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS Ashares_data (
                id INTEGER PRIMARY KEY,
                symbol TEXT,
                company_name TEXT,
                symbol_market TEXT
            )
    ''')
    
    conn.commit()
    conn.close()


def insert_Ashares_data(path_to_db):
    try:
        stock_info_sh_df = ak.stock_info_sh_name_code()
        stock_info_sz_df = ak.stock_info_sz_name_code()
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return

    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    insert_sql = '''
        INSERT OR IGNORE INTO Ashares_data (symbol, company_name, symbol_market) 
        VALUES (?, ?, ?)
    '''

    # 遍历DataFrame并插入数据
    for index, row in stock_info_sz_df.iterrows():
        symbol = row['A股代码']
        company_name = row['A股简称'].replace(" ", "")
        symbol_market = f"{symbol}.SZ"
        # 插入数据到数据库
        cursor.execute(insert_sql, (symbol, company_name, symbol_market))

    for index, row in stock_info_sh_df.iterrows():
        symbol = row['证券代码']
        company_name = row['证券简称'].replace(" ", "")
        symbol_market = f"{symbol}.SH"
        # 插入数据到数据库
        cursor.execute(insert_sql, (symbol, company_name, symbol_market))
    
    conn.commit()
    conn.close()

# def update_daily_table(path_to_db):
#     conn = sqlite3.connect(path_to_db)
#     cursor = conn.cursor()

#     cursor.execute("PRAGMA table_info(Ashares_data)")
#     columns_info = cursor.fetchall()
#     columns_names = [info[1] for info in columns_info]  # extract the column names
    
#     if 'label' not in columns_names:
#         cursor.execute("ALTER TABLE Ashares_data ADD COLUMN label INTEGER DEFAULT -1")
#     if 'date' not in columns_names:
#         cursor.execute("ALTER TABLE Ashares_data ADD COLUMN date TEXT")

#     # update the table
#     today = datetime.now().strftime('%Y-%m-%d')
#     update_sql = "UPDATE Ashares_data SET label = -1, date = ?"
#     cursor.execute(update_sql, (today,))

#     conn.commit()
#     conn.close()
    

# create_Ashares_table(path_to_db)
# insert_Ashares_data(path_to_db)
# update_daily_table(path_to_db)

