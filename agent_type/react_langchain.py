from langchain.agents import create_agent
from langchain.messages import HumanMessage
from tools_langchain import calculator
from llm import LLMClient

tools = [calculator]
model = LLMClient(model="qwen3-vl-plus").init_client()
system_prompt = """你是一个有能力调用外部工具的智能助手，请基于用户问题调用合适的工具进行解答"""

agent = create_agent(model=model,
                     tools=tools,
                     system_prompt=system_prompt)
HumanMessage(content="1+1等于多少")
result = agent.invoke(input={"messages": [{"role": "user", "content": "1+1等于多少"}]})