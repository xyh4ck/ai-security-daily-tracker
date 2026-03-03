#!/usr/bin/env python3
"""
AI安全论文自动追踪系统
每日自动抓取、分析、生成报告并推送到GitHub
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import urllib.parse
import re
from typing import List, Dict, Any

class PaperTracker:
    def __init__(self, base_dir: Path = None):
        # 自动检测脚本所在目录作为项目根目录
        if base_dir is None:
            script_dir = Path(__file__).parent
            base_dir = script_dir.parent
        
        self.base_dir = Path(base_dir).resolve()
        self.reports_dir = self.base_dir / "Reports"
        self.daily_dir = self.base_dir / "daily"
        self.data_file = self.base_dir / "data" / "papers.json"
        
        # 确保目录存在
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 已处理论文ID集合
        self.processed_ids = set()
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.processed_ids = set(data.get('processed_ids', []))
    
    def search_arxiv(self, days_back: int = 1) -> List[Dict[str, Any]]:
        """搜索arXiv最新AI安全相关论文"""
        keywords = [
            'LLM security', 'prompt injection', 'adversarial machine learning',
            'AI safety', 'model poisoning', 'privacy machine learning',
            'Agent security', 'automated penetration testing', 'LLM vulnerability',
            'AI threat modeling', 'model extraction', 'membership inference'
        ]
        
        # 构建查询（最近N天）
        query = ' OR '.join([f'all:{kw}' for kw in keywords[:5]])
        url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending'
        
        papers = []
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read().decode('utf-8')
                
            # 简单解析arXiv API响应
            entries = re.findall(r'<entry>(.*?)</entry>', data, re.DOTALL)
            for entry in entries:
                paper = self._parse_arxiv_entry(entry, days_back)
                if paper and paper['id'] not in self.processed_ids:
                    papers.append(paper)
        except Exception as e:
            print(f"arXiv搜索失败: {e}")
        
        return papers
    
    def _parse_arxiv_entry(self, entry: str, days_back: int) -> Dict[str, Any] | None:
        """解析单篇arXiv论文条目"""
        id_match = re.search(r'<id>(https?://arxiv\.org/abs/\d+\.\d+)</id>', entry)
        title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
        date_match = re.search(r'<published>(\d{4}-\d{2}-\d{2})', entry)
        summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
        
        if not all([id_match, title_match, date_match]):
            return None
        
        paper_id = id_match.group(1).split('/')[-1]
        title = title_match.group(1).strip().replace('\n', ' ')
        pub_date = datetime.fromisoformat(date_match.group(1))
        summary = summary_match.group(1).strip().replace('\n', ' ') if summary_match else ""
        
        # 检查日期范围
        if (datetime.now() - pub_date).days > days_back:
            return None
        
        return {
            'id': paper_id,
            'title': title,
            'url': f"https://arxiv.org/abs/{paper_id}",
            'published': pub_date.strftime('%Y-%m-%d'),
            'summary': summary[:500],
            'source': 'arXiv'
        }
    
    def classify_paper(self, paper: Dict[str, Any]) -> str:
        """分类论文到6大领域"""
        title_lower = paper['title'].lower()
        summary_lower = paper['summary'].lower()
        combined = title_lower + ' ' + summary_lower
        
        if any(kw in combined for kw in ['agent', 'tool use', 'autonomous', 'openclaw']):
            return 'Agent Security'
        elif any(kw in combined for kw in ['prompt injection', 'jailbreak', 'llm', 'large language model']):
            return 'LLM Security'
        elif any(kw in combined for kw in ['iot', 'vehicle', 'embedded', 'edge']):
            return 'IoT Security'
        elif any(kw in combined for kw in ['penetration testing', 'vulnerability', 'exploit', 'fuzzing']):
            return 'Auto Pentest'
        elif any(kw in combined for kw in ['supply chain', 'model zoo', 'poisoning', 'backdoor']):
            return 'Supply Chain'
        else:
            return 'Foundations'
    
    def save_papers(self, papers: List[Dict[str, Any]]) -> None:
        """保存新论文到数据文件"""
        current_data = {}
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        
        # 按日期组织
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in current_data:
            current_data[today] = []
        
        for paper in papers:
            paper['category'] = self.classify_paper(paper)
            current_data[today].append(paper)
            self.processed_ids.add(paper['id'])
        
        current_data['processed_ids'] = list(self.processed_ids)
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=2)
    
    def generate_daily_report(self) -> str:
        """生成每日简报"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if not self.data_file.exists():
            return f"# {today} - 今日暂无新论文\n"
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if today not in data:
            return f"# {today} - 今日暂无新论文\n"
        
        papers = data[today]
        if not papers:
            return f"# {today} - 今日暂无新论文\n"
        
        # 按领域分组
        by_category = {}
        for p in papers:
            cat = p.get('category', 'Foundations')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(p)
        
        # 生成Markdown
        md = f"""# 🤖 AI安全每日简报 - {today}

> 📊 **今日收录**: {len(papers)}篇新论文 | 🔄 自动生成

## 🌟 今日亮点

"""
        # 取每个领域最值得关注的论文
        highlights = []
        for cat, cat_papers in sorted(by_category.items()):
            if cat_papers:
                p = cat_papers[0]
                highlights.append(f"- **[{p['title']}]({p['url']})** - {p['category']}")
        
        md += '\n'.join(highlights)
        md += "\n\n## 📚 详细列表\n\n"
        
        for cat, cat_papers in sorted(by_category.items()):
            md += f"### {cat}\n\n"
            for p in cat_papers:
                md += f"#### [{p['title']}]({p['url']})\n"
                md += f"**发布**: {p['published']} | **ID**: {p['id']}\n\n"
                md += f"{p['summary'][:300]}...\n\n"
                md += "---\n\n"
        
        return md
    
    def generate_dashboard_html(self) -> str:
        """生成可视化看板 HTML"""
        if not self.data_file.exists():
            return self._empty_dashboard()
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 聚合统计
        total_papers = sum(len(v) if isinstance(v, list) else 0 for v in data.values())
        category_stats = {}
        timeline_data = []
        
        for date, papers in data.items():
            if date == 'processed_ids' or not isinstance(papers, list):
                continue
            
            timeline_data.append({'date': date, 'count': len(papers)})
            
            for p in papers:
                cat = p.get('category', 'Foundations')
                category_stats[cat] = category_stats.get(cat, 0) + 1
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI安全追踪看板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0f172a; color: #e2e8f0; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
        .stat-card h3 {{ font-size: 0.9rem; color: #94a3b8; margin-bottom: 10px; }}
        .stat-card .value {{ font-size: 2.5rem; font-weight: bold; }}
        .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
        .chart-container {{ background: #1e293b; padding: 20px; border-radius: 16px; }}
        .recent {{ background: #1e293b; padding: 25px; border-radius: 16px; }}
        .recent h2 {{ margin-bottom: 20px; }}
        .paper-item {{ padding: 15px; margin: 10px 0; background: #334155; border-radius: 8px; border-left: 4px solid #667eea; }}
        .paper-item .title {{ font-weight: bold; margin-bottom: 5px; }}
        .paper-item .meta {{ font-size: 0.85rem; color: #94a3b8; }}
        @media (max-width: 768px) {{ .charts {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ AI安全追踪看板</h1>
            <p style="color: #94a3b8; margin-top: 10px;">最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>📚 总论文数</h3>
                <div class="value">{total_papers}</div>
            </div>
            <div class="stat-card">
                <h3>🎯 覆盖领域</h3>
                <div class="value">{len(category_stats)}</div>
            </div>
            <div class="stat-card">
                <h3>📅 追踪天数</h3>
                <div class="value">{len([d for d in data.keys() if d != 'processed_ids'])}</div>
            </div>
        </div>
        
        <div class="charts">
            <div class="chart-container">
                <canvas id="categoryChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="timelineChart"></canvas>
            </div>
        </div>
        
        <div class="recent">
            <h2>📚 最新收录</h2>
"""
        # 最新论文列表
        recent_papers = []
        for date in sorted(data.keys(), reverse=True):
            if date == 'processed_ids':
                continue
            if isinstance(data[date], list):
                recent_papers.extend(data[date][:3])
            if len(recent_papers) >= 10:
                break
        
        for p in recent_papers[:10]:
            html += f"""
            <div class="paper-item">
                <div class="title"><a href="{p['url']}" target="_blank" style="color: #e2e8f0; text-decoration: none;">{p['title'][:80]}...</a></div>
                <div class="meta">{p.get('category', 'Foundations')} | {p['published']}</div>
            </div>"""
        
        html += """
        </div>
    </div>
    
    <script>
        new Chart(document.getElementById('categoryChart'), {
            type: 'doughnut',
            data: {
                labels: """ + json.dumps(list(category_stats.keys())) + """,
                datasets: [{
                    data: """ + json.dumps(list(category_stats.values())) + """,
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a']
                }]
            },
            options: {{
                responsive: true,
                plugins: {{
                    title: {{ display: true, text: '领域分布', color: '#e2e8f0', font: {{ size: 16 }} }},
                    legend: {{ position: 'bottom', labels: {{ color: '#94a3b8' }} }}
                }}
            }}
        });
        
        new Chart(document.getElementById('timelineChart'), {
            type: 'line',
            data: {
                labels: """ + json.dumps([d['date'] for d in sorted(timeline_data, key=lambda x: x['date'])[-7:]]) + """,
                datasets: [{
                    label: '每日新增',
                    data: """ + json.dumps([d['count'] for d in sorted(timeline_data, key=lambda x: x['date'])[-7:]]) + """,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {{
                responsive: true,
                plugins: {{
                    title: {{ display: true, text: '最近7天趋势', color: '#e2e8f0', font: {{ size: 16 }} }},
                    legend: {{ display: false }}
                }},
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#334155' }} }},
                    y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#334155' }} }}
                }}
            }}
        });
    </script>
</body>
</html>"""
        return html
    
    def _empty_dashboard(self) -> str:
        """返回空数据看板"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI安全追踪看板</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .empty { text-align: center; }
        .empty h1 { font-size: 2rem; margin-bottom: 1rem; }
        .empty p { color: #94a3b8; }
    </style>
</head>
<body>
    <div class="empty">
        <h1>🛡️ AI安全追踪看板</h1>
        <p>数据收集中... 请稍后再试</p>
    </div>
</body>
</html>"""
    
    def push_to_github(self) -> bool:
        """推送到GitHub"""
        try:
            subprocess.run(['git', '-C', str(self.base_dir), 'add', '.'], 
                          check=True, capture_output=True)
            commit_msg = f"Auto-update: {datetime.now().strftime('%Y-%m-%d')}"
            subprocess.run(['git', '-C', str(self.base_dir), 'commit', '-m', commit_msg],
                          check=True, capture_output=True)
            subprocess.run(['git', '-C', str(self.base_dir), 'push'],
                          check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"GitHub推送失败: {e.stderr.decode() if e.stderr else str(e)}")
            return False

def main():
    tracker = PaperTracker()
    
    print(f"📂 工作目录: {tracker.base_dir}")
    
    # 1. 搜索新论文
    print("🔍 搜索arXiv新论文...")
    papers = tracker.search_arxiv(days_back=1)
    print(f"✅ 发现 {len(papers)} 篇新论文")
    
    # 2. 保存数据
    if papers:
        tracker.save_papers(papers)
    
    # 3. 生成每日简报
    daily_report = tracker.generate_daily_report()
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = tracker.daily_dir / f"{today}.md"
    report_path.write_text(daily_report, encoding='utf-8')
    print(f"✅ 生成每日简报: {report_path}")
    
    # 4. 生成可视化看板
    dashboard_html = tracker.generate_dashboard_html()
    (tracker.base_dir / 'board.html').write_text(dashboard_html, encoding='utf-8')
    print(f"✅ 生成看板: {tracker.base_dir / 'board.html'}")
    
    # 5. 推送到GitHub（仅在本地有配置时）
    print("🚀 推送到GitHub...")
    if tracker.push_to_github():
        print("✅ 推送成功")
    else:
        print("⚠️ 跳过推送（可能由GitHub Actions处理）")

if __name__ == '__main__':
    main()
