from langchain.tools import tool

@tool(parse_docstring=True)
def calculator(a: int|float, b: int|float) -> int|float:
    """加法计算器

    Args:
        a: 待加参数
        b: 待加参数
    """
    print("成功调用工具")
    return a + b