from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dash")

@mcp.tool("/introduce_piper_dash")
async def introduce_piper_dash() -> str:
    return "안녕하세요, 파이퍼 DASH 입니다."
