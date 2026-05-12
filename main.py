from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
from mcp.server.fastmcp.exceptions import ResourceError
from typing import Tuple
import base64

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

@mcp.resource("mcp://template/{file_name}")
async def get_template_file(ctx: Context, file_name: str) -> str:
    """
    templatesディレクトリから、指定されたファイル名のテンプレートを読み込みます。
    """
    #安全のため、ファイル名からディレクトリトラバーサル（本来アクセスできないファイルにアクセスしようとすること）の試みを単純に除去
    safe_file_name = file_name.replace("..","")
    file_path = f"templates/{safe_file_name}"
    await ctx.info(f"リソースを読み込みます: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        await ctx.error(f"リソースファイルが見つかりません: {file_path}")
        raise ResourceError(f"テンプレートファイル「{file_name}」が見つかりません。")

@mcp.resource(
    uri="mcp://image/{image_name}",
    name="Get Image",
    description="imagesディレクトリから、指定された画像ファイルをバイナリデータとして読み込みます。",
    mime_type="image/png")
async def get_image(ctx: Context, image_name: str) -> str:
    """
    imagesディレクトリから、指定された画像ファイルをバイナリデータとして読み込みます。
    """
    # この例では簡単のため、PNG形式に限定します
    file_path = f"images/{image_name}.png"
    await ctx.info(f"画像リソースを読み込みます: {file_path}")

    try:
        with open(file_path, "rb") as f:
            content = f.read()
            base64_bytes = base64.b64encode(content)
            return base64_bytes.decode("utf-8")
    except FileNotFoundError:
        await ctx.error(f"画像ファイルが見つかりません: {file_path}")
        raise ResourceError(f"画像ファイル「{image_name}」は見つかりませんでした。")

if __name__ == "__main__":
    # サーバーを起動
    mcp.run()