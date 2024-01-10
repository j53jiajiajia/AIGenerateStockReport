import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import re
from get_keys import get_openai
import sys

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def get_raw_content_from_url(url):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.find('div', class_= "newsContent").get_text().strip()
        title = soup.find('div', class_="detail-header").get_text().split()[0].strip()
        clean_text = '\n'.join(text.split())
        # print(title, clean_text)
        return title, clean_text
    except Exception as e:
        print(f"Error downloading data for {url}: {str(e)}")
        pass

# url = 'https://data.eastmoney.com/report/info/AP202310231602720302.html'

# get_raw_content_from_url(url)

def get_target_text(url):
    title, clean_text = get_raw_content_from_url(url)
    # 让openai提取target_text(***核心观点：***事件点评分析：***风险提示：***投资建议：)
    client = OpenAI(
        api_key=get_openai(),
    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
          {"role": "user", "content": f"{clean_text}\n在这段话中，有0或1段内容为核心观点（事件总结），有2或3段内容为事件点评分析，有1段内容为风险提示，有一段内容为投资建议，请分别把他们提取出来。\n请注意提取出来的内容应是整个原文段落，然后，你返回的内容格式应为：\n***核心观点：\n***事件点评分析：\n***风险提示：\n***投资建议："}
        ]
    )
    content = response.choices[0].message.content.strip()
    # print(content)

    dict_target_text = {}
    # keywords = ["***核心观点：", "***事件点评分析：", "***风险提示：", "***投资建议："]
    index1 = content.find("***核心观点：")
    index2 = content.find("***事件点评分析：")
    index3 = content.find("***风险提示：")
    index4 = content.find("***投资建议：")

    main_idea_text = content[index1+len("***核心观点："):index2].strip()
    comment_idea_text = content[index2+len("***事件点评分析："):index3].strip()
    risk_warning_text = content[index3+len("***风险提示："):index4].strip()
    investment_advice_text = content[index4+len("***投资建议："):].strip()

    dict_target_text["title"] = title
    dict_target_text["main_idea"] = main_idea_text
    dict_target_text["comment_idea"] = comment_idea_text
    dict_target_text["risk_warning"] = risk_warning_text
    dict_target_text["investment_advice"] = investment_advice_text

    # print(dict_target_text)
    return dict_target_text

# get_target_text(url)

def get_two_reports(symbol):
    # 根据url对symbol的格式进行调整
    symbol = symbol.split(".")[0]
    url = f'https://data.eastmoney.com/report/{symbol}.html'
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)
        all_source_code = soup.find_all('script')
        # print(all_source_code)
        valid_matches_found = False
        for source_code in all_source_code:
            matches = re.findall("\"infoCode\":\"[A-Z0-9]+\"", source_code.get_text())
            # print(matches)
            if len(matches) > 1:
                valid_matches_found = True
                infoCode1 = matches[0][12:-1]
                infoCode2 = matches[1][12:-1]
                # print(infoCode1, infoCode2)
                url1 = f'https://data.eastmoney.com/report/info/{infoCode1}.html'
                url2 = f'https://data.eastmoney.com/report/info/{infoCode2}.html'
                dict_target_text1 = get_target_text(url1)
                dict_target_text2 = get_target_text(url2)

                # print(dict_target_text1)
                # print(dict_target_text2)
                return dict_target_text1, dict_target_text2
        if not valid_matches_found:
            raise Exception(f"不好意思，股票({symbol})可获取到的信息较少，无法为您生成研报...")
    except Exception as e:
        print(f"不好意思，股票({symbol})可获取到的信息较少，无法为您生成研报...")
        return None, None

# get_two_reports('603719.SH')




