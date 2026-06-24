from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sys")

@mcp.tool("/introduce_piper_sys")
async def introduce_piper_sys() -> str:
    return "안녕하세요, 파이퍼 SYS 입니다."
