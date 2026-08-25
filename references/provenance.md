# 设计来源

本文件供 skill 维护和来源核对使用，不属于普通写作任务的运行规范。外部材料用于形成候选问题类型；最终规则以事实保护、证据边界、学术规范和语境判断为准。

## 一、通用文本问题与来源核验

- [Wikipedia: Signs of AI writing，永久修订版 1370524124](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1370524124)
- [Wikipedia: WikiProject AI Cleanup，永久修订版 1370354867](https://en.wikipedia.org/w/index.php?title=Wikipedia:WikiProject_AI_Cleanup&oldid=1370354867)

这些页面支持把宣传性评价、模糊归因、浅层总结、编辑痕迹、引用错配和机械格式作为复核线索，同时强调单一风格特征不能证明作者身份或文本来源。

## 二、中文与学术写作候选规则

- [op7418/humanizer-zh](https://github.com/op7418/humanizer-zh)
- [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer)
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop)
- [cangtianhuang/humanizer-academic-zh](https://github.com/cangtianhuang/humanizer-academic-zh)
- [henmuc/codex-academic-humanizer](https://github.com/henmuc/codex-academic-humanizer)
- [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)

相关材料为中文翻译腔、术语稳定、概念标签、强结论、章节语体、引用保护和最小修改提供候选检查项。

其中 `lieflat-less-ai-tone` 提供中文人类文本与多模型生成文本的候选风格特征对照，用于区分统计差异与可执行写作规则。相关结果只用于排除或弱化缺乏独立写作质量依据的表面形式规则，不作为作者身份判断依据。

## 三、作者风格与节奏检查

- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)
- [academic-paper draft writer](https://github.com/Imbad0202/academic-research-skills/blob/main/academic-paper/agents/draft_writer_agent.md)
- [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex)

相关材料为 Style Calibration、直接进入、句长与段长节奏检查提供设计线索。数值阈值在本 skill 中作为导航参数，不作为自动改写命令。

## 四、诊断指标与信息分辨率

- 用户提供的“人味/诊断指标”文章分析摘要（2026-08-25；原文书目信息未随本轮材料提供）。

本轮材料支持两项增量设计：诊断指标不得反向定义生成目标；修改应保护原文已有的信息锚点和信息分辨率。由此明确禁止 Human-likeness、AI-like、作者指纹、surprisal 目标区间或“修改直到达到 X”等生产目标，并把 surprisal、功能词距离、embedding 风格距离等未来探索隔离到 research、experiment 或 optional diagnostic 场景。原文来源信息补齐前，不据此声称具体文献结论。

## 五、维护原则

来源文件只回答规则来自何处；运行规范回答当前如何工作。新增来源时，先判断它是否带来新的行为约束，再决定是否修改 `SKILL.md` 或 operational references。

每条通用规则设置一个主要定义位置。其他 reference 只有在文稿类型、审校阶段或执行方式产生新的行为差异时才作具体化说明，不重复完整规则；维护时优先修改主要定义位置，并检查引用它的文件是否仍然一致。
