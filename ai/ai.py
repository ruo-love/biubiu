from openai import AsyncOpenAI, OpenAI
import os
import datetime
import logging
import pytz
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
DOUBAO_API_BASE_URL = os.getenv("DOUBAO_API_BASE_URL")
# 配置日志
logging.basicConfig(
    filename='schedule.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

class UseAI:
    @staticmethod
    def use_doubao_ai():
        if not DOUBAO_API_KEY or not DOUBAO_API_BASE_URL:
            logging.error("环境变量 DOUBAO_API_KEY 或 DOUBAO_API_BASE_URL 缺失")
        return OpenAI(
            api_key=DOUBAO_API_KEY,
            base_url=DOUBAO_API_BASE_URL,
        )

example = """
**标题：全球人工智能大会今日在杭州开幕，聚焦“AI协同治理与创新发展”**

*   **关键信息：**
    *   **时间：** 今日（2025年6月20日）开幕。
    *   **地点：** 中国杭州。
    *   **事件：** 备受瞩目的全球人工智能大会正式开幕。
    *   **主题：** “AI协同治理与创新发展”。
*   **核心看点：**
    *   会议聚集了全球顶尖AI科学家、头部企业领袖（包括中外科技巨头CEO）、政策制定者。
    *   与会者分享了最新的AI技术、应用场景，探讨合作与整合的重要性。
    *   与会者还分享了他们在AI领域的创新实践和成功案例。
*   **详情**
    ...
"""
def query_ai():
    try:
        client = UseAI.use_doubao_ai()
        beijing_tz = pytz.timezone('Asia/Shanghai')
        now = datetime.datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
        response = client.chat.completions.create(
            model="deepseek-r1-250528",
            messages=[
                {"role": "system","content": "你是新闻检索助手，你需要根据当前时间来检索新闻,直接给我新闻内容，格式如下：\n"+example},
                {"role": "user", "content": f"现在是{now}，请检索今天国内外的1条热点新闻给我"}
            ],
            max_tokens=1000
        )
        content = response.choices[0].message.content
        print("content",content)
        return content
    except Exception as e:
        print(e)
        logging.error(f"[query_ai] AI 请求失败：{e}")
        return "⚠️ AI 请求失败，未能获取内容。"
