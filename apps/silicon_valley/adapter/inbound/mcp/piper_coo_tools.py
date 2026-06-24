from mcp.server.fastmcp import FastMCP

mcp = FastMCP("coo")

@mcp.tool("/introduce_piper_coo")
async def introduce_piper_coo() -> str:
    return "안녕하세요, 파이퍼 COO 입니다."
