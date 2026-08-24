"""中药材 AI 助手 v0.1。

用法：
  python chat.py --question "五味子什么时候收"
  或直接运行 python chat.py 进入交互模式，输入 q 退出。

需要环境变量 ZHIPU_API_KEY（智谱 API Key）。
"""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


BASE_DIR = Path(__file__).resolve().parent
HERBS_FILE = BASE_DIR / "data" / "herbs.json"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4-flash"


def load_herbs():
    with HERBS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)["品种"]


def find_matches(question, herbs):
    """按药材名称/别名做关键词匹配，返回命中药材的资料片段。"""
    matched = []
    for herb in herbs:
        keywords = [herb["名称"]] + herb.get("别名", [])
        if any(kw in question for kw in keywords):
            lines = [f"【{herb['名称']}】"]
            for key, label in [
                ("科属", "科属"),
                ("主产区", "主产区"),
                ("采收时间", "采收时间"),
                ("加工", "加工"),
                ("用途", "用途"),
                ("规格", "规格"),
                ("行情", "行情"),
                ("备注", "备注"),
            ]:
                if herb.get(key) and herb[key] != "待补充":
                    lines.append(f"{label}：{herb[key]}")
            matched.append("\n".join(lines))
    return "\n\n".join(matched)


def ask_glm(question, material):
    api_key = os.environ.get("ZHIPU_API_KEY")
    if not api_key:
        raise SystemExit("没有找到 ZHIPU_API_KEY，请先设置环境变量或使用 run_herba.bat。")

    system_prompt = (
        "你是一名中药材行业助手。回答必须优先基于提供的资料，"
        "如果资料没有相关信息，就明确说“资料里没有，需要补充”，不要编造。"
    )
    user_content = f"资料：\n{material}\n\n问题：{question}"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def run(question):
    herbs = load_herbs()
    material = find_matches(question, herbs)
    if not material:
        print("知识库里没有匹配到药材，我可以先回答常识，但更准确的资料要等补充。\n")
        material = "知识库暂无该品种资料"
    answer = ask_glm(question, material)
    print(f"\n回答：{answer}")


def main():
    parser = argparse.ArgumentParser(description="中药材 AI 助手")
    parser.add_argument("--question", help="要问的问题")
    args = parser.parse_args()

    if args.question:
        run(args.question)
        return

    print("中药材 AI 助手 v0.1（输入 q 退出）")
    while True:
        question = input("\n你的问题：").strip()
        if question.lower() in ("q", "quit", "exit"):
            break
        if question:
            run(question)


if __name__ == "__main__":
    main()
