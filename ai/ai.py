from openai import AsyncOpenAI, OpenAI
import os
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
DOUBAO_API_BASE_URL = os.getenv("DOUBAO_API_BASE_URL")
class UseAI:
    @staticmethod
    def use_doubao_ai():
        return OpenAI(
            api_key=DOUBAO_API_KEY,
            base_url=DOUBAO_API_BASE_URL,
        )


def query_ai():
    client = UseAI.use_doubao_ai()
    response = client.chat.completions.create(
    model="doubao-1.5-vision-pro-32k-250115",  # 或其他正确的模型
        messages=[{
                "role": "system",
                "content": ai_system_context
            },
            {
                    "role": "user",
                    "content": f"讲个笑话吧"
            }
            ],
            max_tokens=1000
        )
    res_content = response.choices[0].message.content
    return res_content