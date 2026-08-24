$ErrorActionPreference = "Stop"

Write-Host "请在下面粘贴你的智谱 API Key，然后按回车。"
$key = Read-Host "API Key"
if (-not $key) {
    Write-Host "没有输入 Key，已退出。"
    exit 1
}

$env:PYTHONIOENCODING = "utf-8"
$env:ZHIPU_API_KEY = $key

python "D:\codex\11-AI学习\day01\api_hello.py" --provider glm --question "你好，用一句话介绍你自己"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n成功！第一次 AI 对话跑通了。"
} else {
    Write-Host "`n出错了，把上面的报错内容发给 Codex。"
}

Read-Host "按回车关闭窗口"
