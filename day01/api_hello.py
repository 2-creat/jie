"""Day 01: 第一个大模型对话脚本。

用法：
  python api_hello.py --provider deepseek --question "你好，介绍一下你自己"
  python api_hello.py --provider qwen --question "用一句话解释什么是 RAG"
  python api_hello.py --provider glm --question "帮我起三个中药材店铺的名字"

API Key 从环境变量读取，不要在代码里写死：
  DeepSeek -> DEEPSEEK_API_KEY
  通义     -> DASHSCOPE_API_KEY
  智谱     -> ZHIPU_API_KEY

Windows 设置环境变量示例（PowerShell）：
  $env:DEEPSEEK_API_KEY = "sk-你的key"
"""

import argparse
import os
import urllib.request
import json


PROVIDERS = {
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "key_env": "DEEPSEEK_API_KEY",
        "model": "deepseek-chat",
    },
    "qwen": {
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "key_env": "DASHSCOPE_API_KEY",
        "model": "qwen-turbo",
    },
    "glm": {
        "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "key_env": "ZHIPU_API_KEY",
        "model": "glm-4-flash",
    },
}


def chat(provider: str, question: str) -> dict:
    cfg = PROVIDERS[provider]
    api_key = os.environ.get(cfg["key_env"])
    if not api_key:
        raise SystemExit(
            f"没有找到环境变量 {cfg['key_env']}。\n"
            "请先在平台注册拿到 Key，再设置环境变量后重试。"
        )

    payload = {
        "model": cfg["model"],
        "messages": [{"role": "user", "content": question}],
    }
    req = urllib.request.Request(
        cfg["url"],
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data


def main():
    parser = argparse.ArgumentParser(description="调用国内大模型 API")
    parser.add_argument("--provider", choices=PROVIDERS.keys(), default="deepseek")
    parser.add_argument("--question", default="你好，用一句话介绍你自己")
    args = parser.parse_args()

    print(f"提问（{args.provider}）：{args.question}")
    data = chat(args.provider, args.question)
    answer = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    print(f"回答：{answer}")
    print(f"用量：prompt={usage.get('prompt_tokens')} tokens, "
          f"completion={usage.get('completion_tokens')} tokens")


if __name__ == "__main__":
    main()
