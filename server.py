import subprocess
import sys

# ========== 第一步：先定义安装函数并执行，再导入依赖 ==========
def install_dependencies():
    # 要安装的依赖列表
    dependencies = [
        "flask==2.3.3",
        "flask-cors==4.0.0",
        "requests==2.31.0"
    ]
    try:
        print("="*30)
        print("正在自动安装依赖（阿里云镜像）...")
        # 使用阿里云镜像加速安装，解决国内下载慢的问题
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-i", "https://mirrors.aliyun.com/pypi/simple/"] + dependencies,
            # 隐藏pip的冗余输出，只显示关键信息
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ 依赖安装完成！")
        print("="*30)
    except subprocess.CalledProcessError as e:
        print("❌ 依赖安装失败！错误信息：", e)
        print("建议手动执行以下命令安装：")
        print(f"{sys.executable} -m pip install flask==2.3.3 flask-cors==4.0.0 requests==2.31.0 -i https://mirrors.aliyun.com/pypi/simple/")
        sys.exit(1)  # 安装失败则退出程序

# 先执行依赖安装（关键！安装完成后再导入库）
install_dependencies()

# ========== 第二步：依赖安装完成后，再导入需要的库 ==========
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import requests
except ImportError as e:
    print(f"❌ 导入库失败：{e}")
    print("请手动安装依赖后重试！")
    sys.exit(1)

# ========== 第三步：初始化Flask应用 ==========
app = Flask(__name__)
CORS(app)  # 允许所有跨域请求，新手无需修改

# ========== DeepSeek API 配置 ==========
DEEPSEEK_CONFIG = {
    "api_key": "sk-16094f6def0b4900a780a08f3828e52e",  # 你的API Key
    "base_url": "https://api.deepseek.com/v1/chat/completions",
    "model": "deepseek-chat"
}

# ========== 后端接口（前端调用地址：http://127.0.0.1:5000/api/chat） ==========
@app.route('/api/chat', methods=['POST'])
def chat_with_deepseek():
    try:
        # 1. 获取前端传递的用户问题
        if not request.is_json:
            return jsonify({"error": "请求格式错误！请使用JSON格式"}), 400
        
        user_data = request.get_json()
        user_question = user_data.get("question", "").strip()
        if not user_question:
            return jsonify({"error": "请输入要提问的内容！"}), 400

        # 2. 构造DeepSeek API请求参数
        request_body = {
            "model": DEEPSEEK_CONFIG["model"],
            "messages": [
                {"role": "system", "content": "你是中国海洋大学文旅专属AI助手，回答简洁、专业，贴合研学场景，避免无关内容"},
                {"role": "user", "content": user_question}
            ],
            "temperature": 0.7,
            "stream": False
        }

        # 3. 调用DeepSeek API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_CONFIG['api_key']}"
        }
        
        # 发送请求并设置超时
        response = requests.post(
            DEEPSEEK_CONFIG["base_url"],
            headers=headers,
            json=request_body,
            timeout=30
        )
        response.raise_for_status()  # 捕获HTTP错误（如401/403/500）

        # 4. 解析并返回AI回复
        ai_result = response.json()
        ai_reply = ai_result["choices"][0]["message"]["content"]
        return jsonify({"reply": ai_reply})

    except requests.exceptions.Timeout:
        return jsonify({"error": "请求超时！请检查网络或稍后重试"}), 500
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return jsonify({"error": "API Key无效或已过期！请检查Key是否正确"}), 401
        else:
            return jsonify({"error": f"DeepSeek API错误：{e}"}), 500
    except Exception as e:
        # 通用错误捕获，避免程序崩溃
        return jsonify({"error": f"服务异常：{str(e)}"}), 500

# ========== 启动后端服务 ==========
if __name__ == '__main__':
    print("🚀 后端服务启动中...")
    print("🌐 后端访问地址：http://127.0.0.1:5000")
    print("💡 前端请调用：http://127.0.0.1:5000/api/chat")
    print("="*30)
    # 启动服务（host=0.0.0.0 允许局域网访问，debug=True方便调试）
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        # 关闭Flask的冗余日志
        use_reloader=False
    )