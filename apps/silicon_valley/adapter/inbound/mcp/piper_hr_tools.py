from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hr")

@mcp.tool("/introduce_piper_hr")
async def introduce_piper_hr() -> str:
    return "안녕하세요, 파이퍼 HR 입니다."
