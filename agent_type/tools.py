from typing import List
import subprocess
from pathlib import Path
WORKDIR = Path.cwd()


class ToolExecutor:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name: str, description: dict, tool_func):
        self.tools[name] = {"description": description, "tool_func": tool_func}

    def use_tool(self, name: str):
        return self.tools[name]["tool_func"]

    def tool_descriptions(self):
        desc_str = "\n".join([f"- {name}: {info["description"]}" for name, info in self.tools.items()])
        return desc_str

def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path

def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=WORKDIR,
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"

def sum_num(nums: List[int]) -> int:
    return sum(nums)

def run_read(
        path: str, limit: int = None) -> str:
    try:
        text = safe_path(path).read_text()
        lines = text.splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more lines)"]
        return "\n".join(lines)[:50000]
    except Exception as e:
        return f"Error: {e}"


def run_write(path: str, content: str) -> str:
    try:
        fp = safe_path(path)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        fp = safe_path(path)
        content = fp.read_text()
        if old_text not in content:
            return f"Error: Text not found in {path}"
        fp.write_text(content.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"


tool_executor = ToolExecutor()
tool_executor.register_tool(name="sum_num",
                            description={"description": "对数据进行求和", "input_parm": {"nums": "List[int]"}},
                            tool_func=sum_num)
tool_executor.register_tool(name="bash",
                            description={"description": "Run a shell command.", "input_parm": {"command": "string"}},
                            tool_func=run_bash)
tool_executor.register_tool(name="read_file",
                            description={"description": "Read file contents.", "input_parm": {"path": "string", "limit": "int"}},
                            tool_func=run_read)
tool_executor.register_tool(name="write_file",
                            description={"description": "Write content to file.", "input_parm": {"path": "string", "content": "str"}},
                            tool_func=run_write)
tool_executor.register_tool(name="edit_file",
                            description={"description": "Replace exact text in file.", "input_parm": {"path": "string", "old_text": "str", "new_text": "str"}},
                            tool_func=run_edit)

if __name__ == "__main__":
    tool_desc = tool_executor.tool_descriptions()
    print(tool_desc)