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

相关材料为中文翻译腔、术语稳定、概念标签、强结论、章节语体、引用保护和最小修改提供候选检查项。

## 三、作者风格与节奏检查

- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)
- [academic-paper draft writer](https://github.com/Imbad0202/academic-research-skills/blob/main/academic-paper/agents/draft_writer_agent.md)
- [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex)

相关材料为 Style Calibration、直接进入、句长与段长节奏检查提供设计线索。数值阈值在本 skill 中作为导航参数，不作为自动改写命令。

## 四、维护原则

来源文件只回答规则来自何处；运行规范回答当前如何工作。新增来源时，先判断它是否带来新的行为约束，再决定是否修改 `SKILL.md` 或 operational references。

每条通用规则设置一个主要定义位置。其他 reference 只有在文稿类型、审校阶段或执行方式产生新的行为差异时才作具体化说明，不重复完整规则；维护时优先修改主要定义位置，并检查引用它的文件是否仍然一致。
