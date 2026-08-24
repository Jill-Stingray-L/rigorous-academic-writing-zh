<h1 align="center">严谨中文科研写作</h1>

<p align="center">守住事实与引用边界，再改善论证、结构与表达。</p>

<p align="center">
  <img src="./assets/readme/hero.webp" width="100%" alt="论文页面、证据链、审校批注与放大镜组成的中文科研写作审校场景">
</p>

面向中文科学论文、学位论文、研究报告和技术报告的 Codex Skill。它把事实保护、证据边界和研究问题放在语言润色之前，帮助作者完成局部润色、深度修订、反馈整合与终稿审计。

`Evidence-first` · `Academic Chinese` · `Python 3` · `MIT`

## 它解决什么问题

- 保护数字、公式、单位、专有名词、限定条件、图表编号与引用范围。
- 检查研究问题、方法、结果和结论是否形成可追踪的闭环。
- 区分事实、描述、解释、评价与因果主张，校准主张强度。
- 稳定术语、章节功能和图表论证，再处理模板化、翻译腔与不自然表达。
- 将脚本命中视为人工复核入口，而不是质量评分或作者身份判断。

## 工作方式

```text
动态建立文档模型
        ↓
确定性与统计检查
        ↓
语义审计
        ↓
最小充分修改
        ↓
回归审计
```

处理优先级始终是：

```text
事实与不可改动项 → 研究问题 → 方法与结果 → 主张与证据 → 结构 → 术语 → 表达
```

完整规则见 [SKILL.md](./SKILL.md)。

## 安装

### 使用 skill-installer

在 Codex 中调用 `$skill-installer`，并提供本仓库的 GitHub URL，要求将 `rigorous-academic-writing-zh` 安装到个人 skills 目录。

### 使用 Git

复制本仓库 **Code → HTTPS** 中的地址，然后在 PowerShell 执行：

```powershell
$repoUrl = Read-Host "粘贴仓库 HTTPS 地址"
git clone $repoUrl "$HOME/.agents/skills/rigorous-academic-writing-zh"
```

Codex 通常会自动检测新安装的 skill；如果未出现，请重新启动 Codex。个人 skill 的官方默认位置是 `$HOME/.agents/skills`。

## 使用

在 Codex 中显式调用：

```text
$rigorous-academic-writing-zh
请对这份中文论文进行终稿审计，优先检查事实、引用、方法—结果闭环和主张强度。
```

也可以直接描述局部润色、深度修订、反馈整合或终稿审计任务；当请求与 skill 的描述匹配时，Codex 可以自动选择它。

## 确定性审计脚本

脚本支持 UTF-8 Markdown 和纯文本，仅使用 Python 标准库：

```powershell
python scripts/audit_academic_zh.py manuscript.md
python scripts/audit_academic_zh.py manuscript.md --format json
python scripts/audit_academic_zh.py manuscript.md --glossary glossary.json
```

它会定位聊天或编辑残留、术语字面变体、图表编号、长句、节奏均一和重复连接词等线索。它不会判断作者身份、给论文打分、自动改写文本或代替语义审计。

> Markdown 标题树、叶节点小节与章节厚度检查只适用于 Markdown；纯文本需要先把正式章节标题规范化为 Markdown 标题。

## 目录结构

```text
rigorous-academic-writing-zh/
├── SKILL.md                         # 入口、触发范围与核心工作流
├── agents/openai.yaml               # Codex 界面元数据
├── scripts/audit_academic_zh.py     # 确定性审计脚本
├── references/                      # 按任务需要加载的规范
└── assets/readme/hero.webp          # GitHub README 视觉资产
```

## 设计边界

- 不编造数据、样本、文献、DOI、页码、引语或实施成效。
- 不提供作者身份概率、检测通过承诺或规避检测方案。
- 不以随机拆句、同义词轮换或语言噪声制造“人类写作”特征。
- 原稿与来源发生实质冲突时，在正文外标明并请求确认。
- 审计任务默认报告问题，不自动扩展为全文改写。

## 参考与维护

规则的设计来源与维护说明见 [references/provenance.md](./references/provenance.md)。外部项目和资料仅作为问题类型与设计线索；各来源仍受其各自许可证和使用条款约束。

Codex skill 的目录结构、发现方式和安装位置以 [OpenAI 官方 Build skills 文档](https://learn.chatgpt.com/docs/build-skills) 为准。

## License

[MIT](./LICENSE) © 2026 rigorous-academic-writing-zh contributors
