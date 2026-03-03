# 🛡️ AI安全追踪 Dashboard

> 🔄 **最后同步:** 2026-03-03 18:25 UTC+8 | 🤖 **AI 速览已生成**

---

## 📅 今日速览 (2026-03-03)
> **Agent 总结的今日高价值趋势：**
> * 今日共有 **19篇** AI安全相关论文和 **3篇** 厂商博客更新。大模型方向出现**首篇系统性Agent安全威胁模型**，定义了从工具滥用到多Agent污染的六大攻击面；同时Microsoft发布**首个自托管AI Agent安全运行指南**，直接适用于OpenClaw等自托管场景。**
> * 👉 [点击阅读今日详细简报](daily/2026-03-03.md)

### 🌟 今日重点情报

| 标题 & 机构 | 核心亮点 (TL;DR) | 领域标签 | 来源 | 笔记链接 |
| :--- | :--- | :--- | :--- | :--- |
| **[从安全Agent到安全Agent Web]**<br>*学术研究* | 首篇系统性Agent安全威胁模型，定义6大攻击面（工具滥用、记忆污染、规划劫持等） | `LLM安全` `Agent安全` | arXiv | [📝 笔记](Reports/arXiv/2026-03-03-Agent-Security.md) |
| **[安全运行OpenClaw]**<br>*Microsoft* | 首个自托管AI Agent安全指南，三层防御（身份/隔离/监控），Critical风险等级 | `Agent安全` `运行时安全` | Blog | [📝 笔记](Reports/Blogs/2026-02-19-OpenClaw-Security.md) |
| **[Shadow API欺诈]**<br>*学术研究* | 揭示第三方API虚假声明前沿模型，高价换低质，数据泄露风险 | `供应链安全` | arXiv | [📝 笔记](Reports/arXiv/2026-03-03-Shadow-APIs.md) |
| **[DualSentinel检测]**<br>*学术研究* | 双熵分析检测黑盒LLM后门/提示注入，轻量级高精度 | `LLM安全` | arXiv | [📝 笔记](Reports/arXiv/2026-03-03-DualSentinel.md) |
| **[OAuth钓鱼攻击]**<br>*Microsoft* | OAuth重定向滥用绕过邮件网关，新型社会工程学攻击 | `钓鱼攻击` | Blog | [📝 笔记](Reports/Blogs/2026-03-02-OAuth-Phishing.md) |

---

## 🗂️ 近 7 天动态 (按领域分类)

### 1. 大模型安全 (LLM Security)
> *追踪提示注入、越狱、模型投毒、隐私泄露与红队评测。*
* `[03-03]` **[DualSentinel](https://arxiv.org/abs/2603.01574)** - 基于双熵分析检测黑盒LLM的后门和提示注入攻击 - [📝 笔记](Reports/arXiv/2026-03-03-DualSentinel.md)
* `[03-03]` **[Defensive Refusal Bias](https://arxiv.org/abs/2603.01246)** - 安全对齐导致LLM拒绝帮助合法防御者，揭示对齐技术的副作用

### 2. Agent 安全 (Agent Security)
> *追踪工具调用、记忆系统、浏览器Agent与代码执行代理的攻击面。*
* `[03-03]` **[从安全Agent到安全Agent Web](https://arxiv.org/abs/2603.01564)** - 首篇系统性Agent安全威胁模型，定义6大攻击面 - [📝 笔记](Reports/arXiv/2026-03-03-Agent-Security.md)
* `[03-03]` **[安全运行OpenClaw](https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/)** - Microsoft发布自托管AI Agent安全指南 - [📝 笔记](Reports/Blogs/2026-02-19-OpenClaw-Security.md)

### 3. IoT 安全 (IoT Security)
> *追踪边缘设备、工控终端、智能家居与视觉传感器安全。*
* `[03-03]` **[系统综述：IoT和车联网隐私保护](https://arxiv.org/abs/2603.01876)** - 系统性综述IoT和V2X隐私保护技术 - [📝 笔记](Reports/arXiv/2026-03-03-IoT-Privacy.md)
* `[03-03]` **[ACC入侵检测](https://arxiv.org/abs/2603.01173)** - 将ML IDS集成到自适应巡航控制系统

### 4. 自动化渗透测试 (Automated Penetration Testing)
> *追踪漏洞发现、PoC生成、攻击路径规划与攻防演练自动化。*
* `[03-03]` **[vEcho](https://arxiv.org/abs/2603.01154)** - 使用LLM从漏洞验证转向主动发现 - [📝 笔记](Reports/arXiv/2026-03-03-vEcho.md)
* `[03-03]` **[LLM自动化补丁](https://arxiv.org/abs/2603.01257)** - 系统性研究LLM在自动化补丁生成中的架构 - [📝 笔记](Reports/arXiv/2026-03-03-LLM-Patching.md)
* `[03-03]` **[SubstratumGraphEnv](https://arxiv.org/abs/2603.01340)** - 强化学习环境用于建模系统攻击路径

### 5. AI 供应链与平台安全 (AI Supply Chain & Platform Security)
> *追踪模型仓库、数据集、RAG、向量数据库和部署链路中的系统性风险。*
* `[03-03]` **[Shadow API欺诈](https://arxiv.org/abs/2603.01919)** - 揭示第三方API虚假声明前沿模型的欺诈行为 - [📝 笔记](Reports/arXiv/2026-03-03-Shadow-APIs.md)
* `[03-03]` **[LLM推理隐私保护](https://arxiv.org/abs/2603.01499)** - 通过协作混淆实现LLM推理的隐私保护

### 6. 基础安全研究与评测 (Security Foundations & Evaluation)
> *追踪对抗机器学习、安全对齐、威胁建模与安全评测。*
* `[03-03]` **[AI应用威胁建模](https://www.microsoft.com/en-us/security/blog/2026/02/26/threat-modeling-ai-applications/)** - Microsoft发布AI应用威胁建模指南 - [📝 笔记](Reports/Blogs/2026-02-26-AI-Threat-Modeling.md)
* `[03-03]` **[对抗性多模态对齐](https://arxiv.org/abs/2603.01784)** - 通过结构化对抗进化实现多模态对齐

---

## 📚 知识库与历史归档

**按时间检索:**
* [本周汇总](daily/weekly/) - 待生成
* [历史每日简报归档](daily/archives/) - 待生成

**按来源检索:**
* [arXiv 研究笔记总览](Reports/arXiv/)
* [漏洞与通告归档](Reports/Vulns/)
* [厂商博客与工程更新](Reports/Blogs/)
* [开源工具与平台安全](Reports/OpenSource/)

---

## 🎯 快速导航

- **[今日速览](daily/2026-03-03.md)** - 2026-03-03 详细简报
- **[Agent安全专题](Reports/arXiv/2026-03-03-Agent-Security.md)** - Agent安全威胁模型
- **[OpenClaw安全指南](Reports/Blogs/2026-02-19-OpenClaw-Security.md)** - 自托管Agent最佳实践
- **[AI威胁建模](Reports/Blogs/2026-02-26-AI-Threat-Modeling.md)** - AI应用威胁建模指南

---

## 📊 追踪统计

- **追踪开始时间**: 2026-03-03
- **已处理论文数**: 19篇
- **已创建笔记**: 6篇（5篇论文 + 3篇博客）
- **覆盖领域**: 6大领域（LLM/Agent/IoT/Auto-Pentest/供应链/基础研究）
- **数据源**: arXiv, Microsoft Security Blog

---

*🤖 由 AI安全情报追踪助手 自动维护*
*📅 最后更新: 2026-03-03*
