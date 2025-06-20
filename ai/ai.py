from openai import AsyncOpenAI, OpenAI
import os
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
DOUBAO_API_BASE_URL = os.getenv("DOUBAO_API_BASE_URL")
class UseAI:
    @staticmethod
    def use_doubao_ai():
        if not DOUBAO_API_KEY or not DOUBAO_API_BASE_URL:
            logging.error("环境变量 DOUBAO_API_KEY 或 DOUBAO_API_BASE_URL 缺失")
        return OpenAI(
            api_key=DOUBAO_API_KEY,
            base_url=DOUBAO_API_BASE_URL,
        )


def query_ai():
    try:
        client = UseAI.use_doubao_ai()
        response = client.chat.completions.create(
            model="doubao-1.5-vision-pro-32k-250115",
            messages=[
                {"role": "system", "content": "你是一个幽默的助手，请讲一个笑话"},
                {"role": "user", "content": "讲个笑话吧"}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"[query_ai] AI 请求失败：{e}")
        return "⚠️ AI 请求失败，未能获取内容。"
