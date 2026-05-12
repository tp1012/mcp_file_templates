from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
# FastMCPアプリケーションのインスタンスを作成
# アプリケーション名はuv initで指定したものと同じにします
mcp = FastMCP("mcp_file_templates")

@mcp.prompt(description="テンプレートリソースを活用してユーザーの表示を実行します。")
async def prosecc_with_resources(ctx: Context, instruction: str) -> str:

    """
    MCPサーバーが保持するテンプレートリソースを活用して、ユーザーの指示を実行するためのプロンプトを生成します。
    """

    await ctx.info(f"Prompt機能が呼び出されました:'{instruction}'")
    #この時点では実際の処理は行いません。
    return f"mcp_file_templates MCP サーバー上のリソースを利用して、以下の指示を実行してください。 ¥n {instruction}"

@mcp.prompt()
async def suggest_template(ctx: Context, theme: str) -> str:
    """
    指定されたテーマに適したテンプレートを調査・提案し、選択後に作成・保存するワークフローを案内します。
    """
    await ctx.info(f"２つ目のprompt機能が呼び出されました：'{theme}'")

    #このプロンプトも、現時点では指示を受け付けたことの確認を返すのみ
    return f"""以下の順で処理を行ってください。
    {theme}のファイルについて、必要な項目を洗い出し、推奨されるテンプレートやフォーマットをwebで検索してください。
    調査した内容を整理し、３つのパターンを提示してください。
    提示されたパターンから選ばれたら、そのテンプレートファイルを作成してください。
    このMCPサーバーの登録ツールを作成して、作成したファイルの保存をしてください。"""

if __name__ == "__main__":
    # サーバーを起動
    mcp.run()