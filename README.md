# AI 安全论文追踪器 - 自动化部署

> 🤖 每日自动追踪 AI 安全相关论文，生成可视化看板并推送到 GitHub

## ✨ 功能特性

- 🔍 **自动追踪**: 每日自动搜索 arXiv 最新 AI 安全论文
- 📊 **智能分类**: 自动将论文分类到 6 大领域（LLM/Agent/IoT/渗透测试/供应链/基础研究）
- 📈 **可视化看板**: Chart.js 驱动的交互式 dashboard（`board.html`）
- 📝 **每日简报**: Markdown 格式的每日总结
- 🚀 **GitHub 集成**: 自动提交推送到 GitHub + GitHub Actions 定时任务
- 🌐 **GitHub Pages**: 看板可在线访问

## 📁 目录结构

```
ai-security-tracker/
├── scripts/
│   └── auto_track.py          # 核心追踪脚本
├── data/
│   └── papers.json            # 论文数据存储
├── daily/
│   └── 2026-03-03.md          # 每日简报
├── board.html                 # 可视化看板
├── .github/workflows/
│   └── daily-track.yml        # GitHub Actions 配置
└── README.md
```

## 🚀 快速开始

### 1. 本地部署

```bash
# 克隆/初始化仓库
git init
git remote add origin <your-repo-url>

# 运行追踪脚本
python3 scripts/auto_track.py
```

### 2. 推送到 GitHub

```bash
git add .
git commit -m "Initialize AI security tracker"
git branch -M main
git push -u origin main
```

### 3. 启用 GitHub Actions

仓库推送到 GitHub 后，Actions 会自动激活。每天 UTC 00:00（北京时间 08:00）自动运行。

手动触发：GitHub 仓库 → Actions → "AI Security Daily Tracker" → Run workflow

### 4. 启用 GitHub Pages（看板托管）

1. 仓库 Settings → Pages
2. Source 选择 "Deploy from a branch"
3. Branch 选择 "main"，文件夹 "/ (root)"
4. 访问 `https://<username>.github.io/<repo>/board.html`

## 📊 看板功能

- **实时统计**: 总论文数、覆盖领域、追踪天数
- **领域分布**: 饼图展示 6 大领域占比
- **时间趋势**: 最近 7 天论文数量趋势
- **最新收录**: 最近 10 篇论文列表

## 🔧 配置选项

编辑 `scripts/auto_track.py` 中的参数：

```python
# 搜索关键词（前 5 个用于 API 查询）
keywords = [
    'LLM security', 'prompt injection', 'adversarial machine learning',
    ...
]

# 分类规则
def classify_paper(self, paper):
    # 自定义分类逻辑
```

## 📅 定时任务

GitHub Actions 默认：每天 UTC 00:00 运行

修改定时：编辑 `.github/workflows/daily-track.yml` 中的 cron 表达式

```yaml
schedule:
  - cron: '0 0 * * *'  # 每天 00:00
  # 其他示例:
  # - cron: '0 */6 * * *'  # 每 6 小时
  # - cron: '0 9 * * 1-5'  # 工作日早上 9 点
```

## 🛠️ 本地调试

```bash
# 手动运行
cd /root/.openclaw/workspace-research/ai-security-tracker
python3 scripts/auto_track.py

# 预览看板
python3 -m http.server 8000
# 访问 http://localhost:8000/board.html
```

## 📦 数据格式

`data/papers.json`:

```json
{
  "2026-03-03": [
    {
      "id": "2603.01564",
      "title": "论文标题",
      "url": "https://arxiv.org/abs/2603.01564",
      "published": "2026-03-03",
      "summary": "摘要...",
      "source": "arXiv",
      "category": "LLM Security"
    }
  ],
  "processed_ids": ["2603.01564", ...]
}
```

---

*🤖 自动维护 by AI Security Tracker*  
*最后更新: 2026-03-03*
