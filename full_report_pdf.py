from generate_report_text import generate_report_text
from chart1 import draw_trend_chart
from table1 import draw_stock_data_table
from table2 import draw_rating_details_table
from add_content_to_pdf import add_content_to_pdf
from create_picture_dir import create_picture_dir
from table3 import draw_prediction_table

def generate_total_report(symbol, name):
    create_picture_dir()
    dict_report_content = generate_report_text(symbol, name)
    if dict_report_content:
        draw_trend_chart(symbol, name)
        draw_stock_data_table(symbol, name)
        draw_rating_details_table(symbol, name)
        draw_prediction_table(dict_report_content, symbol, name)

        add_content_to_pdf(symbol, name, "template.pdf", dict_report_content)    # 生成只有一页不带免责声明的研报
        # add_content_to_pdf(symbol, name, "template_with_statement.pdf", dict_report_content)    # 生成两页带免责声明的研报
        return "Success"
    else:
        return "Insufficient Info"


# generate_total_report('300750.SZ', "宁德时代")
# generate_total_report('002230.SZ', "科大讯飞")
# generate_total_report('000858.SZ', "五粮液")
# generate_total_report('002415.SZ', "海康威视")
# generate_total_report('600519.SH', "贵州茅台")
# generate_total_report('002594.SZ', "比亚迪")
# generate_total_report('601899.SH', "紫金矿业")



