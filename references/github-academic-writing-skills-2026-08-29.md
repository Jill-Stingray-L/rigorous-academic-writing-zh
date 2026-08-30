# GitHub 学术撰写 Skill 对比（2026-08-29）

## 结论

当前 `rigorous-academic-writing-zh` 的定位是合理的：它比热门“大而全”科研工作流更适合中文论文/报告的审阅、修订和终稿审计，且已经把事实、证据边界、图表语义和最小修改放在优先级最高的位置。近期最有价值的改进是**可验证性与交付契约**，而不是扩展为多代理论文生产线：先为现有审计脚本补回归样例并修复误报；再以短小、可选的方式加入证据/引用状态和交付摘要。

## 方法与样本边界

- 抓取日：2026-08-29（Asia/Shanghai）。星标和 fork 为 GitHub 页面/REST 搜索当日快照；`k` 是 GitHub 页面显示的四舍五入值。最近更新取各仓库 `main` 的 GitHub commits Atom feed 的首个 `updated` 时间，避免把 star/watch 等仓库活动误当成源码更新。
- 入口交叉：GitHub 公开仓库搜索使用 `academic writing`、`scientific writing`、`research paper writing`、`thesis writing`、`academic-writing skill`、`scientific-writing SKILL.md`、`academic writing claude skill`、`academic writing codex skill`；再用热门科研 skill 集合的 README 和候选仓库自身目录核对。入选需公开、源码可读，并且至少有一个直接服务 manuscript/paper/thesis/rebuttal/scientific-writing 的单元。
- 这不是 GitHub 全站排名。匿名 Code Search 要求登录，且后续 GitHub Core API 命中速率限制；因此本报告是“高相关且有热度的可复核样本”，不是穷尽性清单。资源清单仓库、纯论文代写产品和只做文献检索的仓库不列为可比 skill。

## 核心样本（源码与一手元数据）

| 样本 | 热度快照；最近提交 | 可比性与源码 | 功能边界、工作流与明显取舍 |
| --- | --- | --- | --- |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 44,124★ / 3,499 forks；2026-08-27T09:55:24Z ([提交源](https://github.com/Imbad0202/academic-research-skills/commits/main.atom)) | **直接 SKILL**：[academic-paper/SKILL.md](https://github.com/Imbad0202/academic-research-skills/blob/main/academic-paper/SKILL.md)、[academic-paper-reviewer/SKILL.md](https://github.com/Imbad0202/academic-research-skills/blob/main/academic-paper-reviewer/SKILL.md) | 以 12 个角色覆盖配置、检索、结构、论证、起草、引用、摘要、评审和多格式输出，并提供计划、修订、引文检查等多种模式。覆盖面和阶段交付可作功能地图；但两个入口分别约 48 KB 和 38 KB，触发词、角色、状态协议和多轮门禁远超中文审校所需，最能说明“高热度不等于应复制复杂度”。 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 37,056★ / 3,517 forks；2026-08-28T21:41:21Z ([提交源](https://github.com/K-Dense-AI/scientific-agent-skills/commits/main.atom)) | **直接 SKILL**：[scientific-writing/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) | 从保密/外传授权、研究设计和报告规范，到 source manifest、claim/evidence、方法—结果一致性、本地审计、作者/AI 披露和人工提交批准。强项是把“起草、核验、提交”分离，并以可审计记录约束。代价是工作区/清单/ID 较重、以英文科学论文为中心，不适合每次中文局部润色都完整运行。 |
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | 37.7k★ / 2.1k forks；2026-08-28T05:00:55Z ([提交源](https://github.com/Yuan1z0825/nature-skills/commits/main.atom)) | **直接 SKILL**：[nature-writing](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-writing/SKILL.md)、[nature-polishing](https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-polishing/SKILL.md) | 以 `task/paper_type/section/language/journal` manifest 路由，按需加载片段；对 Results 的“最短充分证据链”、主文/图注/SI 分配和整稿一致性扫查尤有价值。代价是 Nature 风格与英文/中译英导向；其“Nature-style”是语料提炼而非期刊官方规则，不能替代目标期刊现行要求。 |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 12.1k★ / 880 forks；2026-06-16T01:36:40Z ([提交源](https://github.com/Orchestra-Research/AI-Research-SKILLs/commits/main.atom)) | **直接 SKILL**：[20-ml-paper-writing/ml-paper-writing/SKILL.md](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/main/20-ml-paper-writing/ml-paper-writing/SKILL.md) | 面向 NeurIPS/ICML/ICLR/ACL/AAAI/COLM 的 repo→贡献确认→草稿→反馈循环；引用必须检索/核验/BibTeX 获取，不确定处以占位符显式保留。可迁移的是“引用不能从记忆补全”和缺口可见化；局限是 ML venue 模板、年份和外部 API 依赖会过时，且其“先给完整初稿”的主动性不总适合证据尚未冻结的文稿。 |
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | 5,248★ / 417 forks；2026-08-27T09:45:00Z ([提交源](https://github.com/Galaxy-Dawn/claude-scholar/commits/main.atom)) | **套件内直接单元**：[nature-writing/SKILL.md](https://github.com/Galaxy-Dawn/claude-scholar/blob/main/skills/nature-writing/SKILL.md)（入口说明：[README](https://github.com/Galaxy-Dawn/claude-scholar/blob/main/skills/nature-writing/README.md)） | 将 `question → evidence → experiment → analysis → claim → writing` 串为研究生命周期，另分 citation verification、self-review、rebuttal 等职责。适合从实验与知识库到论文的项目级工作；作为本 skill 的直接替代过宽，且主分支为 Claude 工作流、Codex 在独立分支，移植需核对宿主差异。 |
| [zLanqing/codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | 3.3k★ / 192 forks；2026-05-14T09:08:48Z ([提交源](https://github.com/zLanqing/codex-claude-academic-skills/commits/main.atom)) | **直接 SKILL**：[research-writing-skill/SKILL.md](https://github.com/zLanqing/codex-claude-academic-skills/blob/main/research-writing-skill/SKILL.md) | 中文优先：材料盘点→问题/缺口/方法/证据/贡献/限制大纲→分章草拟→逻辑、术语、引文核查；不编造。其“原文/已有数据、用户确认、上下文推断、建议性扩展”四分法和收尾缺口摘要值得吸收。局限是证据绑定仅为原则、没有可执行账本；示例偏光电/仿真。 |
| [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) | 177★ / 10 forks；2026-07-20T21:24:08Z ([提交源](https://github.com/SNL-UCSB/paper-writing-skill/commits/main.atom)) | **直接 SKILL**：[SKILL.md](https://github.com/SNL-UCSB/paper-writing-skill/blob/main/SKILL.md) | 以 project context、结构化 brainstorming、claim–evaluation 映射、topic sentence 和跨章节术语漂移检查构造论证，并要求 LaTeX/PDF 交付前检查。可借鉴“每项实验的论证职责”；但规则来自 UCSB systems/networking lab，触发范围过宽、每次强制加载 author profile，且“zero hedging/active voice”不适用于需要校准不确定性的通用科研写作。 |

### 高热度但仅作非等价参照

[ahmetbersoz/chatgpt-prompts-for-academic-writing](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing)（4.9k★ / 394 forks，最近提交 2024-01-25T08:48:11Z，[提交源](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing/commits/main.atom)）是[提示词 README](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing/blob/main/README.md)，而非 Agent `SKILL.md`。它覆盖构思、语言、文献综述和研究计划，说明此类需求的持续热度；但没有可执行的证据、引用、方法—结果或文档审计契约，**不能**当作当前 skill 的同类实现或优化蓝本。

另查到 [PangenomeAI/academic-skills-food-nutrition](https://github.com/PangenomeAI/academic-skills-food-nutrition)（28★ / 2 forks；2026-08-24T01:22:19Z，[提交源](https://github.com/PangenomeAI/academic-skills-food-nutrition/commits/main.atom)）的 [food-paper/SKILL.md](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/main/food-paper/SKILL.md)。它有 journal-aware 的 12 角色 manuscript pipeline、统计/图表/引用/审稿回复分工和领域报告默认值；因热度尚低且 Food/Nutrition 专属，作为架构反例而非热门核心样本：不应把其多代理全流程复制到通用中文审校 skill。

## 与当前 skill 的初步对比

比较对象为本仓库 [SKILL.md](../SKILL.md)。当前主文件约 7.5 KB / 89 行；深度论文任务会按路由加载 `SKILL.md`、`document-model-and-audit.md`、`rigor-and-evidence.md`、`paper-structure.md` 与（语言终校时）`chinese-style-patterns.md`。它已具备一些高热样本常见而关键的能力：不编造、证据优先、信息锚点保护、方法—结果—主张闭环、跨章节依赖传播、DOCX/PDF 视觉审计，以及“局部润色/深度修订/终稿审计/反馈整合”四种范围边界。

| 维度 | 当前优势 | 可补的最小能力 | 不应照搬 |
| --- | --- | --- | --- |
| 证据与引用 | 信息锚点、事实边界和不凭空补证据的规则清晰；适合中文审校。 | 借 K-Dense/zLanqing 的状态化交付：把“已由材料支持 / 待作者核验 / 缺材料”列在正文外；为引用增加“存在性、书目信息、主张支持范围”三项可选核验。 | 要求每段都写 claim/evidence ID、全量 manifest 或强制外部查询。 |
| 论证与结构 | 不只润色语句，已检查研究问题、方法—结果和图表功能。 | 借 SNL 的“每项实验承担何种论证功能”和 Yuan 的“最短充分证据链/主文—图注—补充材料分配”。 | 固定某实验室的 voice、无条件去 hedging、固定 IMRaD 或 Nature 叙事。 |
| 任务路由与上下文 | 已按论文、报告、语言终校、风格样本分层读取 references。 | 借 Yuan 的轴式路由，明确 `任务（起草/修订/审计/反馈）×文稿类型×章节×语言/目标规范`，仅加载必要参考文件。 | 多代理编排、全量读取参考库、面向期刊的硬编码年份/页数。 |
| 交付与可靠性 | 四种模式的修改边界明确，且已有 `audit_academic_zh.py`。 | 明确每种模式的最小输出契约（修订稿/问题清单/证据缺口/已改范围）；先增加真实文稿片段 fixture 与预期输出，再修复脚本误报并做回归检查。 | 在尚无 test/eval 的情况下继续增加检查规则或大型脚本。 |
| 伦理、保密与提交 | 已禁止虚构，且强调证据边界。 | 从 K-Dense 压缩借入一条：涉及未发表稿、审稿材料、个人/受限数据的外发前需用户明确授权，并把 AI 披露、作者/投稿决定保留给作者与目标期刊规则。 | 把医学/临床的全套 reporting-guideline、author registry 和 submission scaffold 设为每次必经步骤。 |

## 优化优先级与精简判断

1. **P0：先让现有审计可回归。** 当前仓库没有 `tests/`、`evals/` 或可复核的输入—输出 fixture；且已观察到 `audit_academic_zh.py` 对主 skill 产生截断式 `METHOD_DECLARATION_LOW_MENTION` 误报、表格式章节触发 `THIN_SECTION`。先用最小 fixture 锁定这些规则，再修改检测；这是比继续加规则更高价值的改进。
2. **P1：增加很短的“交付摘要 + 证据状态”模板。** 仅在审计、深度修订和反馈整合中要求列出：使用材料、已改范围、`待核验` 引用/事实、`待补` 材料、未决口径。借鉴 zLanqing/K-Dense 的可见性，不把 ID 或工作日志塞进论文正文。
3. **P2：把引用核验做成按需能力。** 用三项检查（书目信息是否存在、是否支持该主张、是否覆盖限定范围）补强当前“引用位置及其支持范围”的原则；网络不可用时明确为“未独立核验”，不猜 DOI，不把检索失败等同于否定。
4. **P3：只在需要时细化路由。** 现有主文件已经紧凑，暂无明显应删的大段。若增加任务轴或 output contract，应把期刊、章节修辞和提交细节放入 `references/`，保持入口文件为路由和不可违背边界。

因此，当前最好的“精简”不是删去事实保护或五阶段顺序，而是**拒绝引入**多代理编排、每条主张 ID、通用 LaTeX 模板、固定会议年份/篇幅和全量官方清单。它们会放大上下文与维护成本，也会把当前的中文、跨学科、最小修改优势稀释掉。

## 证据定位与局限

- 上表每个技能名均链接仓库；“源码”链接均为对应 `SKILL.md`（或明确标注的 README）；“提交源”为该仓库 GitHub 一手 Atom feed。功能、边界、工作流和局限均来自这些源码，而非博客或榜单。
- 当前时间点的 GitHub stars/forks 会持续变化；将来复查时应以仓库页面或 GitHub REST API 重取，不应把本文快照当作永久数值。
- 相关不等于质量或安全审计：本报告未执行候选仓库脚本、未安装依赖，也没有验证其作者对“Nature 风格”、期刊要求或统计能力的外部主张。所有期刊/机构规则仍应在实际任务时访问目标规则的当前一手来源。
