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
    
    def search_arxiv(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """搜索arXiv最新AI安全相关论文"""
        
        # AI安全相关的分类
        search_terms = [
            'cat:cs.CR',  # Cryptography and Security
            'cat:cs.LG',  # Machine Learning
            'cat:cs.AI'   # Artificial Intelligence
        ]
        
        query = ' OR '.join(search_terms)
        url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending'
        
        papers = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read().decode('utf-8')
            
            # 使用更宽松的正则匹配
            entries = re.findall(r'<entry>.*?</entry>', data, re.DOTALL)
            
            for entry in entries:
                # 解析论文信息
                id_match = re.search(r'/abs/(\d+\.\d+)', entry)
                title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                pub_match = re.search(r'<published>(\d{4}-\d{2}-\d{2})', entry)
                summary_match = re.search(r'<summary>(.*)</summary>', entry, re.DOTALL)
                
                if not all([id_match, title_match, pub_match]):
                    continue
                
                paper_id = id_match.group(1)
                title = title_match.group(1).strip().replace('\n', ' ')
                pub_date_str = pub_match.group(1)
                summary = summary_match.group(1).strip().replace('\n', ' ')[:500] if summary_match else ""
                
                # 解析日期并过滤
                try:
                    pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d')
                    if pub_date < cutoff_date:
                        continue
                except:
                    continue
                
                # AI安全关键词过滤
                security_keywords = [
                    'security', 'privacy', 'adversarial', 'attack', 'defense',
                    'robustness', 'safety', 'vulnerability', 'injection', 'poisoning',
                    'inference', 'encryption', 'authentication', 'federated', 'differential',
                    'conformal', 'causality'
                ]
                
                title_lower = title.lower() + ' ' + summary.lower()
                if not any(kw in title_lower for kw in security_keywords):
                    continue
                
                # 只返回未处理的论文
                if paper_id not in self.processed_ids:
                    papers.append({
                        'id': paper_id,
                        'title': title,
                        'url': f"https://arxiv.org/abs/{paper_id}",
                        'published': pub_date_str,
                        'summary': summary,
                        'source': 'arXiv'
                    })
        except Exception as e:
            print(f"arXiv搜索失败: {e}")
        
        return papers
    
    def classify_paper(self, paper: Dict[str, Any]) -> str:
        """分类论文到6大领域"""
        title_lower = paper['title'].lower() + ' ' + paper['summary'].lower()
        
        if any(kw in title_lower for kw in ['privacy', 'differential privacy', 'federated', 'inference']):
            return '隐私保护'
        elif any(kw in title_lower for kw in ['robustness', 'adversarial', 'attack', 'defense', 'conformal']):
            return '鲁棒性安全'
        elif any(kw in title_lower for kw in ['security', 'encryption', 'authentication', 'vulnerability']):
            return '系统安全'
        elif any(kw in title_lower for kw in ['safety', 'injection', 'poisoning', 'causality']):
            return 'AI安全'
        else:
            return '其他'
    
    def save_papers(self, papers: List[Dict[str, Any]]) -> None:
        """保存论文数据"""
        # 添加新论文到已处理集合
        for paper in papers:
            self.processed_ids.add(paper['id'])
        
        # 保存到文件
        data = {
            'updated_at': datetime.now().isoformat(),
            'processed_ids': list(self.processed_ids),
            'total_count': len(self.processed_ids)
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def generate_daily_report(self) -> str:
        """生成每日简报"""
        papers = self.search_arxiv(days_back=7)
        
        report = f"# {datetime.now().strftime('%Y-%m-%d')} - AI安全论文追踪报告\n\n"
        report += f"## 📊 统计信息\n\n"
        report += f"- **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"- **新论文数**: {len(papers)} 篇\n"
        report += f"- **时间范围**: 最近7天\n\n"
        
        if papers:
            # 按分类统计
            categories = {}
            for paper in papers:
                cat = self.classify_paper(paper)
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(paper)
            
            report += "## 📚 分类汇总\n\n"
            for cat, paper_list in categories.items():
                if paper_list:
                    report += f"### {cat} ({len(paper_list)} 篇)\n\n"
                    for paper in paper_list[:5]:
                        report += f"- [{paper['title']}]({paper['url']})\n"
                    report += "\n"
        else:
            report += "## 暂无新论文\n\n"
        
        return report
    
    def generate_dashboard_html(self) -> str:
        """生成可视化看板"""
        papers = self.search_arxiv(days_back=7)
        
        # 分类
        classified = {
            '隐私保护': [],
            '鲁棒性安全': [],
            '系统安全': [],
            'AI安全': [],
            '其他': []
        }
        
        for paper in papers:
            cat = self.classify_paper(paper)
            classified[cat].append(paper)
        
        total = len(papers)
        today = datetime.now().strftime('%Y-%m-%d')
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI安全论文追踪看板</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        .header h1 {{ 
            color: #667eea;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }}
        .stat-card {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-number {{ font-size: 36px; font-weight: bold; }}
        .stat-label {{ opacity: 0.9; }}
        
        .category {{ margin-bottom: 30px; }}
        .category-title {{
            background: white;
            padding: 15px 20px;
            border-radius: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .paper-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }}
        .paper {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .paper:hover {{ transform: translateY(-5px); }}
        .paper-title {{ 
            font-size: 16px; 
            font-weight: 600; 
            color: #2c3e50; 
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        .paper-meta {{ 
            color: #7f8c8d; 
            font-size: 13px; 
            margin-bottom: 10px;
        }}
        .paper-summary {{ 
            color: #34495e; 
            font-size: 14px; 
            line-height: 1.6;
        }}
        .paper-link {{ 
            display: inline-block;
            margin-top: 10px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        .empty {{ text-align: center; color: white; padding: 20px; opacity: 0.8; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI安全论文追踪看板</h1>
            <p style="color: #7f8c8d;">最近7天 AI安全领域最新研究动态</p>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total}</div>
                    <div class="stat-label">总论文数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len([c for cats in classified.values() for c in cats if cats])}</div>
                    <div class="stat-label">活跃领域</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{today}</div>
                    <div class="stat-label">更新日期</div>
                </div>
            </div>
        </div>
"""
        
        for category, papers_list in classified.items():
            count = len(papers_list)
            html += f"""
        <div class="category">
            <div class="category-title">
                {category} ({count} 篇)
            </div>
"""
            
            if papers_list:
                html += '<div class="paper-grid">'
                for paper in papers_list[:20]:
                    html += f"""
                <div class="paper">
                    <div class="paper-title">{paper['title']}</div>
                    <div class="paper-meta">📅 {paper['published']}</div>
                    <div class="paper-summary">{paper['summary'][:200]}...</div>
                    <a href="{paper['url']}" target="_blank" class="paper-link">→ 查看论文</a>
                </div>
"""
                html += '</div>'
            else:
                html += '<div class="empty">暂无论文</div>'
            
            html += '</div>'
        
        html += """
    </div>
</body>
</html>
"""
        
        return html
    
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
    papers = tracker.search_arxiv(days_back=7)
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
