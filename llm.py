import os

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()


class LLMClient(object):
    """自定义LLM服务类"""
    def __init__(self, model: str = None, model_provider: str = "openai",
                 api_key: str = "QWEN_API_KEY", base_url: str = "QWEN_BASE_URL"):
        self.model = model
        self.model_provider = model_provider
        self.api_key = os.getenv(api_key)
        self.base_url = os.getenv(base_url)
        self.client = init_chat_model(model=self.model,
                                      model_provider=self.model_provider,
                                      api_key=self.api_key,
                                      base_url=self.base_url)

    def invoke(self, message):
        return self.client.invoke(message).content

    def stream(self, message):
        for chunk in self.client.stream(message):
            print(chunk.content, end="", flush=True)  # flush实现实时输出

if __name__ == '__main__':
    llm = LLMClient(model="qwen3-vl-plus")
    # print(llm.invoke([HumanMessage("你好，请问你是谁？")]))
    llm.stream([HumanMessage("你好，请问你是谁？")])
