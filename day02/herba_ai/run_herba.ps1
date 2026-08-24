$ErrorActionPreference = "Stop"

Write-Host "请在下面粘贴你的智谱 API Key，然后按回车。"
$key = Read-Host "API Key"
if (-not $key) {
    Write-Host "没有输入 Key，已退出。"
    exit 1
}

$env:PYTHONIOENCODING = "utf-8"
$env:ZHIPU_API_KEY = $key

$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
python "$scriptDir\chat.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n运行结束。"
} else {
    Write-Host "`n出错了，把上面的报错内容发给 Codex。"
}

Read-Host "按回车关闭窗口"
