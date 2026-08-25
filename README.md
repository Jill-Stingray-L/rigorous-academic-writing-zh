<h1 align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="严谨中文科研写作：核对事实、引用、方法—结果关系和主张强度的中文科研审校 Skill">
</h1>

<p align="center">对中文论文与研究报告进行系统审校，核对事实、引用、方法—结果关系和主张强度，并修订结构与表达。</p>

面向中文科学论文、学位论文、研究报告和技术报告的 Codex Skill。它支持局部润色、深度修订、反馈整合和终稿审计；处理语言之前，先核对文稿中的事实、证据和论证关系。

`Evidence-first` · `Academic Chinese` · `Python 3` · `MIT`

## 一个简化的审校示例

以下例子用于说明审校判断，不代表特定研究结果。

> **原句**
>
> A 组准确率为 92%，B 组为 81%，证明该方法具有显著优势。

现有信息可以支持两组相差 11 个百分点，但不能单独支持“显著”或“证明”。前者通常需要统计检验，后者还取决于研究设计和结论范围。

> **修订**
>
> A 组准确率为 92%，B 组为 81%，前者高出 11 个百分点。

修改保留原始数字和比较对象，只收缩证据尚不能支持的主张。这个原则同样适用于因果关系、实施成效、鲁棒性、泛化能力和跨场景有效性等结论。

## 审校范围

| 层级 | 核对重点 |
|---|---|
| 事实与信息 | 核对数字、单位、范围、样本、专有名词、图表编号和引用位置，防止口径变化或具体信息被泛化。 |
| 研究设计 | 检查研究问题、材料、方法、结果和结论的对应关系，确认声明的方法得到实际应用。 |
| 主张与证据 | 区分事实、计算、描述、解释、评价和因果主张，避免把相关写成因果、把结构适用写成运行验证。 |
| 结构与表达 | 检查章节功能、术语、指代、句法和学术中文，处理术语漂移、翻译腔和模板化表达。 |

脚本命中、词频和句段统计只用于定位复核位置。是否修改以及怎样修改，仍由上下文中的语义、证据和文稿规范决定。

## 四种任务模式

| 模式 | 处理范围 |
|---|---|
| 局部润色 | 用于内容和论证已经稳定的文本，处理词语、句法、指代、节奏和少量段内顺序。 |
| 深度修订 | 用于整章、全文或结构性问题，允许调整段落、章节接口和方法—结果关系。 |
| 反馈整合 | 整理导师批注、审稿意见、会议纪要或多版意见，追踪依据、处置和验证结果。 |
| 终稿审计 | 在提交或交付前定位事实、证据、结构、术语和格式风险。 |

审计任务默认报告问题，不自动扩展为全文改写。局部润色也不会自行改变研究设计或论证结构。

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

审校始终按照以下顺序处理：

```text
事实与不可改动项 → 研究问题 → 方法与结果 → 主张与证据 → 结构 → 术语 → 表达
```

深度修订还会对照原文和修订稿，检查时间、数量、对象、案例、限定条件和不确定性是否被无理由删减或概括。完整规则见 [SKILL.md](./SKILL.md)。

## 安装

### 使用 skill-installer

在 Codex 中调用 `$skill-installer`，提供本仓库的 GitHub URL，并要求安装 `rigorous-academic-writing-zh`。

### 使用 Git

在 PowerShell 中执行：

```powershell
git clone https://github.com/Jill-Stingray-L/rigorous-academic-writing-zh.git `
  "$HOME/.agents/skills/rigorous-academic-writing-zh"
```

个人 Skill 的默认目录是 `$HOME/.agents/skills`。如果安装后没有被 Codex 识别，请重新启动 Codex。

## 首次使用

在 Codex 中显式调用：

```text
$rigorous-academic-writing-zh
请对这份中文论文进行终稿审计，核对事实与引用、方法—结果关系和主张强度。先列出需要复核的问题，不要直接重写全文。
```

也可以明确要求局部润色、深度修订或反馈整合。任务描述与 Skill 的适用范围一致时，Codex 也可以自动选择它。

## 确定性审计脚本

仓库包含一个仅使用 Python 标准库的辅助脚本，支持 UTF-8 Markdown 和纯文本：

```powershell
python scripts/audit_academic_zh.py manuscript.md
python scripts/audit_academic_zh.py manuscript.md --format json
python scripts/audit_academic_zh.py manuscript.md --glossary glossary.json
```

脚本用于定位聊天或编辑残留、术语字面变体、图表编号、长句、局部结构重复和连接词等线索。它不判断作者身份，不给论文打分，也不自动改写输入文本。

Markdown 标题树、叶节点小节和章节厚度检查只适用于 Markdown。纯文本需要进行结构审计时，应先把正式章节标题规范化为 Markdown 标题。

## 能力边界

- 不补写没有来源的数据、样本、文献、DOI、页码、引语或实施成效。
- 不提供作者身份概率、检测通过承诺或规避检测方案。
- 不为改变统计特征而随机拆句、轮换同义词或加入语言噪声。
- 原稿与来源发生实质冲突时，在正文外标明冲突并请求确认。
- 表面句式只有造成具体的语义、证据、指代或表达问题时才处理。

## 仓库结构

```text
rigorous-academic-writing-zh/
├── SKILL.md                         # 入口、适用范围与核心工作流
├── agents/openai.yaml               # Codex 界面元数据
├── scripts/audit_academic_zh.py     # 确定性与统计审计脚本
├── references/                      # 按任务类型加载的审校规范
└── assets/readme/hero.svg           # README 视觉资产
```

## 参考与维护

规则来源和维护说明见 [references/provenance.md](./references/provenance.md)。外部资料用于提出候选问题和设计约束，不直接构成作者身份判断或自动修改依据。

Codex Skill 的目录结构、发现方式和安装位置以 [OpenAI 官方 Build skills 文档](https://learn.chatgpt.com/docs/build-skills) 为准。

## License

[MIT](./LICENSE) © 2026 rigorous-academic-writing-zh contributors
