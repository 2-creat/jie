# 中药材 AI 助手（v0.1 骨架）

用智谱 GLM 做的第一版命令行问答助手，先跑通“资料 + AI 回答”的完整链路。

## 现在能做什么

双击 `run_herba.bat`，输入智谱 API Key 后，问它：

```text
五味子什么时候收？
淫羊藿主产哪里？
柴胡有什么用途？
```

它会先按关键词从 `data/herbs.json` 找资料，再把资料交给 GLM 生成回答。资料里没有的它会如实说不知道，不会瞎编。

## 目录

```text
herba_ai/
├── README.md
├── chat.py              # 问答主程序
├── run_herba.bat        # 双击运行
├── run_herba.ps1        # 底层脚本
└── data/herbs.json      # 药材知识库（重点维护这个文件）
```

## 下一步升级计划

1. 把家里真实资料补进 `herbs.json`：规格、产地、采收标准、历史收购价。
2. 升级成 RAG：用 Chroma 向量库 + 文档切分，支持大段资料。
3. 做成网页版：输入框提问，浏览器里直接聊。
4. 加上行情：把近 3 年价格数据放进去，让它能回答“今年行情怎么样”。

## 跑法（命令行方式）

```powershell
cd D:\codex\11-AI学习\day02\herba_ai
$env:ZHIPU_API_KEY = "你的key"
python chat.py --question "五味子什么时候收"
```
