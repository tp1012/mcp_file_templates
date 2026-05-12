from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
# FastMCPアプリケーションのインスタンスを作成
# アプリケーション名はuv initで指定したものと同じにします
mcp = FastMCP("mcp_file_templates")

@mcp.prompt()
async def prosecc_with_resources(ctx: Context, instruction: str) -> str:

    """
    MCPサーバーが保持するテンプレートリソースを活用して、ユーザーの指示を実行するためのプロンプトを生成します。
    """

    await ctx.info(f"Prompt機能が呼び出されました:'{instruction}'")
    #この時点では実際の処理は行いません。
    return f"mcp_file_templates MCP サーバー上のリソースを利用して、以下の指示を実行してください。 ¥n {instruction}"

if___name__ == "__main__":
    # サーバーを起動
    mcp.run()