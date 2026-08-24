# 国内大模型 API 注册指南

三个平台都要注册，但今天至少跑通一个就算过关。推荐顺序：智谱（有免费模型）> DeepSeek（便宜）> 通义（免费额度）。

## 1. 智谱 GLM（推荐先注册）

1. 打开 https://open.bigmodel.cn
2. 手机号注册登录，进入「API 密钥」页面
3. 点「创建 API Key」，复制保存（只显示一次）
4. 用免费模型 `glm-4-flash`，不需要充值

设置环境变量（PowerShell）：
```powershell
$env:ZHIPU_API_KEY = "粘贴你的key"
```

测试：
```powershell
python api_hello.py --provider glm --question "你好"
```

## 2. DeepSeek

1. 打开 https://platform.deepseek.com
2. 注册登录后进入「API Keys」创建 Key
3. 新账号默认余额很少，需要充值（几十块够用很久）

设置环境变量：
```powershell
$env:DEEPSEEK_API_KEY = "sk-粘贴你的key"
```

测试：
```powershell
python api_hello.py --provider deepseek --question "你好"
```

## 3. 通义千问（阿里云百炼）

1. 打开 https://bailian.console.aliyun.com
2. 阿里云账号登录，开通百炼大模型服务
3. 在「API-KEY 管理」创建 Key
4. 用 `qwen-turbo`，新用户有免费额度

设置环境变量：
```powershell
$env:DASHSCOPE_API_KEY = "sk-粘贴你的key"
```

测试：
```powershell
python api_hello.py --provider qwen --question "你好"
```

## 安全规则（重要）

- API Key 是钱，**永远不要提交到 Git，不要发给别人，不要写进代码里**。
- 本仓库已经配置 `.gitignore` 忽略 `.env` 和 `__pycache__`。
- 如果怀疑 Key 泄露，回平台立刻删除重建。
