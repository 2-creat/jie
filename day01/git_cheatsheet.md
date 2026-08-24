# Git 每日提交速查

## 第一次（今天）

```powershell
cd D:\codex\11-AI学习
git init
git add .
git commit -m "Day 01: Python 自测 + API 脚本 + 学习日志"
```

## 每天收尾

```powershell
git status                       # 看改了什么
git add .                        # 把所有改动放进暂存区
git commit -m "Day 02: 完成 xxx" # 提交，-m 后面写今天做了什么
git log --oneline                # 看提交历史
```

## 等 GitHub 注册好之后

用已有的 `jie` 仓库（或新建一个空仓库，不要勾 README），然后：

```powershell
git remote add origin https://github.com/2-creat/jie.git
git branch -M main
git push -u origin main
```

之后每天 `git add .` + `git commit` + `git push` 就是完整打卡。

## 口诀

- `add` 是把改动装进篮子
- `commit` 是给这一篮改动拍照存档
- `push` 是把照片传到 GitHub
- commit 信息要写清楚今天干了什么，方便以后回看
