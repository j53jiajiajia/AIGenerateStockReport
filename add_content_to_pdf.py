import os
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('KaiTi', 'KaiTi.ttf'))
pdfmetrics.registerFont(TTFont('KaiTi-Bold', 'KaiTi-Bold.ttf'))
pdfmetrics.registerFont(TTFont('HeiTi', 'SimHei.ttf'))

def apply_inline_style(text):
    # 将第一个句子放在加粗样式标签内
    try:
        new_text = ''
        for para in text.split('<br/>'):
            # print(para)
            first_sentence_end = para.find('。') + 1
            # first_sentence = text[:first_sentence_end]
            # other_sentence = text[first_sentence_end:]

            if first_sentence_end > 0:
                new_para = f"<font name='KaiTi-Bold'>{para[:first_sentence_end]}</font><font name='KaiTi'>{para[first_sentence_end:]}</font><br/>"
                # new_para = f"{para[:first_sentence_end]}{para[first_sentence_end:]}"
                new_text = new_text + new_para
                # text = text.replace(para, new_para)
            # print(para)
        # print(new_text)
        return new_text
    except Exception as e:
        raise ValueError("apply_inline_style ERROR")


def add_content_to_pdf(symbol, name, input_file_path, content):
    # 创建一个PDF读取对象和一个PDF写入对象
    pdf_reader = PdfReader(input_file_path)
    pdf_writer = PdfWriter()

    # 获取第一页
    page = pdf_reader.pages[0]

    # 创建一个临时PDF来存储文字
    packet = BytesIO()
    pdf_canvas = canvas.Canvas(packet, pagesize=letter)

    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']
    style.firstLineIndent = 21
    style.wordWrap = 'CJK'
    # style.alignment = 4

    # 插入图像1
    # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
    if symbol[-3:] == '.SH':
        adjusted_symbol = symbol.replace('.SH', '.SS')
        image1_path = f"图片/chart1图片/chart1_{name}({adjusted_symbol}).jpg"
    else:
        image1_path = f"图片/chart1图片/chart1_{name}({symbol}).jpg"

    pdf_canvas.drawImage(image1_path, 65, 530, width=170, height=100)  # Adjust the coordinates and dimensions as needed

    # 插入图像2
    # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
    if symbol[-3:] == '.SH':
        adjusted_symbol = symbol.replace('.SH', '.SS')
        image2_path = f"图片/table1图片/table1_{name}({adjusted_symbol}).jpg"
    else:
        image2_path = f"图片/table1图片/table1_{name}({symbol}).jpg"

    pdf_canvas.drawImage(image2_path, 65, 390, width=170, height=100)  # Adjust the coordinates and dimensions as needed

    # 插入图像3
    image3_path = f"图片/table2图片/table2_{name}({symbol}).jpg"

    pdf_canvas.drawImage(image3_path, 65, 280, width=170, height=80)  # Adjust the coordinates and dimensions as needed

    # 插入图像4
    # 根据yahoo api对沪板块的股票symbol的格式进行调整(在yahoo api中，沪板块的股票代码为：xxxxxx.SS)
    if symbol[-3:] == '.SH':
        adjusted_symbol = symbol.replace('.SH', '.SS')
        image3_path = f"图片/table3图片/table3_{name}({adjusted_symbol}).jpg"
    else:
        image3_path = f"图片/table3图片/table3_{name}({symbol}).jpg"

    pdf_canvas.drawImage(image3_path, 65, 145, width=170, height=85)  # Adjust the coordinates and dimensions as needed

    # Set initial coordinates
    x = 255
    y = 650

    for key, value in content.items():
        if key == "报告标题":
            pdf_canvas.setFont('KaiTi-Bold', 18)
            pdf_canvas.setFillColor(colors.black)
            pdf_canvas.drawString(65, 680, value)
        elif key == "名字代码":
            pdf_canvas.setFont('HeiTi', 12)
            pdf_canvas.setFillColor(colors.black)
            name_width = 12*len(value.split("(")[0])
            pdf_canvas.drawString(490-name_width, 730, value)
        elif key == "出版时期":
            pdf_canvas.setFont('HeiTi', 10.6)
            pdf_canvas.setFillColor(colors.grey)
            pdf_canvas.drawString(500, 760, value)
        elif key == "昨收盘: ":
            pdf_canvas.setFont('KaiTi', 9)
            pdf_canvas.setFillColor(colors.black)
            pdf_canvas.drawString(530, 718, value)

        elif key == "核心要点" or key == "点评分析" or key == "估值预测" or key == "风险提示":
            # Set bold and blue for subtitle
            pdf_canvas.setFont('KaiTi-Bold', 10.5)
            pdf_canvas.setFillColor(colors.darkblue)
            pdf_canvas.drawString(x, y, key)
            y -= 2

            # 处理package中无视'\n'等问题
            value = value.replace(' ', '&nbsp;')
            value = value.replace('\n', '<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            value = value.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')

            # Set content with appropriate style
            if key == "核心要点":
                style.fontName = 'KaiTi-Bold'
                style.fontSize = 10.5

            elif key == "点评分析":
                value = apply_inline_style(value)
                style.fontName = 'KaiTi'
                style.fontSize = 10.5

            else:
                style.fontName = 'KaiTi'
                style.fontSize = 10.5


            P = Paragraph(value, style)
            aW = 310  # Available width
            aH = y - 12  # Available height

            # Wrap the text and check if it fits in the available space
            w, h = P.wrap(aW, aH)
            # print(w,h,aW,aH)
            if w <= aW and h <= aH:
                P.drawOn(pdf_canvas, x, y - h)
                y -= h + 12
            else:
                raise ValueError("Text does not fit in the specified area")

    # Save the PDF file
    pdf_canvas.save()

    # 将临时PDF移动到packet的开头
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # 将文字合并到原来的页面上
    page.merge_page(new_pdf.pages[0])

    # 将合并后的页面添加到PDF写入对象
    pdf_writer.add_page(page)

    # 将剩余的页面添加到PDF写入对象
    for i in range(1, len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[i])

    # 将新的PDF写入到文件
    output_file_path = f"{name}({symbol})研究报告.pdf"
    with open(output_file_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"PDF created successfully at: {output_file_path}")

# # Text content for the PDF
# dict_report_content = {
#     "名字代码": "宁德时代(300750.SZ)",
#     "出版时期": "2023-12-10",
#     "昨收盘: ": "167.99",
#     "报告标题": "财报稳健展商智，市场占有显领骥",
#     "核心要点": "宁德时代在2023年第三季度维持了稳健的财务业绩，增长势头保持良好，其中第三季度实现营业收入1054亿元，同比增长8%，环比增长5%，表明公司保持了逐季增长的态势。尽管如此，归母净利润出现较上季度4%的小幅下降，降至104亿元，但与去年同期相比也实现了11%的增长。这一结果显示出宁德时代即便在市场竞争加剧和成本压力可能增大的外部环境下，依然能够保持利润增长，并巩固其在动力电池行业中的领先地位。",
#     "点评分析": "宁德时代的第三季度业绩稳健，显示其盈利能力和市场份额的持续增长。第三季度实现归母净利润104.3亿元，同比增长10.7%，与公司在全球动力电池装机量达158.3GWh，市占率提升到36.9%的强劲表现相协调。毛利率也从上半年的21.6%提升到Q3的22.4%，体现出公司对成本控制的优秀管控能力。公司的这一系列财务指标集中体现了它作为电池制造行业领导者的地位。\n产品创新和研发投入是宁德时代业绩增长的关键驱动因素。前三季度研发投入增长40.7%，达到148.8亿元，这促进了如神行超充电池等新技术的研发和推广。神行超充电池支持10分钟内充电至80%SOC，体现了公司在快充技术方面的领先地位，此举有望成为新产品销售的强大推动力，提升公司的盈利能力和市场竞争力。\n宁德时代的全球业务扩展为其市场份额提升奠定了坚实基础。该公司在中美欧以外地区的动力电池市场占率达27.2%，同比大幅提升9.8%，并且在欧洲市场占有率也有持续大幅提升，目前已达34.9%。得益于与大众、Stellantis等欧系本土车企的密切合作以及矿产资源业务的开展，预计公司在全球市场的份额和盈利能力将继续保持上升趋势。",
#     "估值预测": "股票宁德时代300750.SZ当前市盈率(PE)为：16.18，预计该公司市盈率为：13.30，当前市盈率高于预计市盈率；当前市净率(PE)为：3.99；息税折旧摊销前利润(EBITDA)为：10.06。\n截至2023年12月10日，根据近三个月内48位分析师对宁德时代股票的评级判断，普遍给予强烈买入的建议。其中，有87.50%的分析师认定强烈买入，12.50%的分析师建议买入，没有分析师给出持有、未达标或卖出的建议。宁德时代的平均目标股价预计为330.10元，最高可能达到712.00元，而最低目标价设定在239.02元。考虑到当前股价为163.59元，市场对该公司股票的增值潜力保持高度信心，呈现出强烈的买入信号。",
#     "风险提示": "原材料成本上涨风险、电动汽车市场需求疲软、储能产品销售不达标"
# }
#
# # Example
# add_content_to_pdf('300750.SZ', '宁德时代', "template.pdf", dict_report_content)
