from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ceo")

@mcp.tool("/introduce_piper_ceo")
async def introduce_piper_ceo() -> str:
    return "안녕하세요, 파이퍼 CEO 입니다."