from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


def generate_comment_idea(symbol, name, dict_target_text1, dict_target_text2):
    comment_idea1 = dict_target_text1["comment_idea"]
    comment_idea2 = dict_target_text2["comment_idea"]

    # make openai to generate comment idea for our report
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
          {"role": "user", "content": f"{comment_idea1}\n{comment_idea2}\n以上是证券公司的研究报告对于{name}({symbol})股票的多个点评分析。请仔细阅读，综合点评分析，然后生成对{name}股票的3个点评分析。\n注意：你将仅返回3个点评分析；语言风格应当正式官方，每个点评为一段，首句为总结（以句号结尾）（不要带有特殊标注，如*），后面为分析解释；尽可能多的提供具体的数据支持，定量分析；生成的文本风格及格式应就像提供的研究报告一样。"}
        ]
    )
    content = response.choices[0].message.content.strip()
    content = content.replace("\n\n", "\n")
    # print(content)
    return content


def generate_risk_warning(symbol, name, dict_target_text1, dict_target_text2):
    risk_warning1 = dict_target_text1["risk_warning"]
    risk_warning2 = dict_target_text2["risk_warning"]

    # make openai to generate comment idea for our report
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
          {"role": "user", "content": f"{risk_warning1}\n{risk_warning2}\n以上是证券公司的研究报告对于{name}({symbol})股票的多个风险提示。请仔细阅读，综合这些风险提示，然后生成对{name}股票的3个风险提示。\n注意：你将仅返回3个风险提示（不需要任何提示语，比如：面临的三个主要风险提示为：）；语言风格应当正式官方，生成的3个风险提示应为短句，之间以、分隔, 最后以。结尾；比如，你返回的内容为：{risk_warning1}"}
        ]
    )
    content = response.choices[0].message.content.strip()
    # print(content)
    return content


def generate_main_idea(symbol, name, dict_target_text1, dict_target_text2):
    main_idea1 = dict_target_text1["main_idea"]
    main_idea2 = dict_target_text2["main_idea"]

    # make openai to generate comment idea for our report
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
          {"role": "user", "content": f"{main_idea1}\n{main_idea2}\n以上是证券公司的研究报告对于{name}({symbol})股票的多个核心观点。请仔细阅读，综合这些风险提示，然后生成对{name}股票的核心观点。\n注意：你将仅返回一段话的核心观点（不需要任何提示语，比如：核心观点为：）；语言风格应当正式官方，生成的核心观点应为一个段落，且字数不得超过150字；比如，你返回的内容为：\n{main_idea1}"}
        ]
    )
    content = response.choices[0].message.content.strip()
    # print(content)
    return content


# def generate_report_content(symbol, name):
#     dict_target_text1, dict_target_text2 = get_two_reports(symbol)
#     generate_main_idea(symbol, name, dict_target_text1, dict_target_text2)
#     generate_comment_idea(symbol, name, dict_target_text1, dict_target_text2)
#     generate_risk_warning(symbol, name, dict_target_text1, dict_target_text2)

# generate_report_content('300750.SZ')