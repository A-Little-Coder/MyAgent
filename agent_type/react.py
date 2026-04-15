import os
import platform
import re
import json

from langchain.messages import SystemMessage, HumanMessage

from agent_type.prompt_template import react_prompt_template
from tools import tool_executor
from llm import LLMClient



class ReActAgent:
    def __init__(self):
        self.model = LLMClient(model="qwen3-vl-plus")
        self.system_prompt = self.render_system_prompt(react_prompt_template)
        self.messages = [SystemMessage(self.system_prompt)]

    def render_system_prompt(self, system_prompt_template: str) -> str:
        """渲染系统提示模板，替换变量"""
        tool_desc = tool_executor.tool_descriptions()
        system_name = platform.system()
        cwd = os.getcwd()
        system_prompt = system_prompt_template.format(tool_desc=tool_desc, operating_system=system_name, dir=cwd)
        return system_prompt

    def run_react_client(self, user_input: str):
        self.messages.append(HumanMessage(user_input))
        n = 1
        while n < 20:
            res = self.model.stream(self.messages)
            if "<final_answer>" in res:
                final_answer = re.search(r"<final_answer>(.*?)</final_answer>", res, re.DOTALL)
                print(final_answer.group(1))
                break
            else:
                if "<action>" in res:
                    actions = re.search(r"<action>(.*?)</action>", res, re.DOTALL)
                    actions = json.loads(actions.group(1))
                    for action in actions:
                        func_name = list(action.keys())[0]
                        func = tool_executor.use_tool(func_name)
                        params = action[func_name]
                        try:
                            tool_res = func(**params)
                        except Exception as e:
                            tool_res = f"工具执行错误：{str(e)}"
                        obs_msg = f"<observation>{tool_res}</observation>"
                        print("\n"+obs_msg)
                        self.messages.append(HumanMessage(obs_msg))
            n += 1
            print("⸻")
        else:
            print("询问次数过多，程序终止！")


if __name__ == "__main__":
    agent = ReActAgent()
    agent.run_react_client("请帮我在工作目录下新建并写入一个num.txt文件，然后在里面写下20个数字，数字用逗号隔开，之后再读取这个文件中的数字并计算求和的结果")
