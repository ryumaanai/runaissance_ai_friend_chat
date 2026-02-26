import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

app = Flask(__name__)

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    """
    メインのチャット画面を描画
    （Chapter 7で、ここにファイルから履歴を読み込む処理を追加します）
    """
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    ユーザーからのメッセージを受け取り、AIの返答を返す
    """
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # 【不完全な状態】
    # 過去の履歴を含めず、今回のメッセージだけをAIに送信している
    # Chapter 1でシステムプロンプト（人格）を追加し、
    # Chapter 8, 9で過去の履歴も一緒に送るように改修します。
    messages_for_llm =[
        {"role": "user", "content": user_message}
    ]

    try:
        # OpenAI APIへリクエスト（ストリーミングなしの一括受信）
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_for_llm
        )
        
        # AIの返答テキストを抽出
        ai_reply = response.choices[0].message.content
        
        # JSON形式でフロントエンドへ返す
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "システムエラーが発生しました。"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)