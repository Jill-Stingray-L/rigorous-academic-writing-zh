#!/usr/bin/env python3
"""Locate review-worthy patterns in Chinese academic Markdown or plain text.

The script is an editorial navigation aid. It does not infer authorship, score
academic quality, rewrite the input, or make semantic decisions for the user.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Finding:
    code: str
    category: str
    line: int
    message: str
    excerpt: str


@dataclass(frozen=True)
class GlossaryTerm:
    preferred: str
    variants: tuple[str, ...]
    confusable: tuple[str, ...]


@dataclass(frozen=True)
class MethodDeclaration:
    name: str
    line: int
    mentions: int


PATTERNS: tuple[tuple[str, str, re.Pattern[str], str], ...] = (
    (
        "CHAT_TRACE",
        "deterministic",
        re.compile(r"希望(?:这|以上)?对(?:您|你)有帮助|请告诉我|当然[！!]|下面为(?:您|你)|如需.{0,12}请"),
        "疑似残留聊天或协作话语；正式正文通常直接陈述内容。",
    ),
    (
        "EDITORIAL_MARKER",
        "deterministic",
        re.compile(r"^\s*(?:注|来源|提示|待补充|待完善|TODO|FIXME)\s*[:：]", re.I),
        "疑似编辑提示或制作说明；确认目标格式是否要求保留。",
    ),
    (
        "DEFICIENCY_NOTE",
        "semantic-lead",
        re.compile(
            r"现有(?:材料|资料|数据).{0,30}(?:尚未|未能|没有|缺少|未包含)"
            r"|(?:当前|该)结果.{0,30}(?:不足以|不能据此)"
            r"|由于.{0,50}(?:尚不明确|缺失|缺少|不足).{0,30}(?:不能|无法)"
        ),
        "正文可能在用材料缺口代替分析；检查主张边界及其在正文中的必要性。",
    ),
    (
        "VAGUE_ATTRIBUTION",
        "citation",
        re.compile(r"研究表明|研究显示|专家认为|业内普遍认为|有观点认为|相关资料显示|多项研究(?:表明|显示)"),
        "存在泛化归因；核对同句是否有具体且能支持该命题的引文。",
    ),
    (
        "OVERCLAIM",
        "semantic-lead",
        re.compile(
            r"证明了|验证了|已经影响|显著(?:提高|降低|改善|增强)"
            r"|有效(?:提高|降低|解决|改善)|直接导致|必然导致"
            r"|具有(?:较强|良好|优秀)?(?:鲁棒性|泛化能力|跨场景(?:适用性|有效性))"
        ),
        "结论强度较高；核对研究设计、检验、外部验证或运行记录是否支持。",
    ),
    (
        "PROMOTIONAL",
        "style",
        re.compile(r"至关重要|开创性|里程碑|全方位|强大(?:的)?|深刻揭示|赋能|奠定(?:了)?坚实基础|前景广阔|未来可期|迈出(?:了)?重要一步"),
        "存在宣传性或宏大化措辞；优先改为具体结果、机制或适用条件。",
    ),
    (
        "NEGATIVE_PARALLEL",
        "style",
        re.compile(r"不仅.{0,50}(?:而且|更是)|不只是.{0,50}而是|不是.{0,50}而是"),
        "存在否定式对比或排比；确认直接陈述目标状态是否更清楚。",
    ),
    (
        "COMMAND_TONE",
        "style",
        re.compile(r"不得|严禁|不允许|必须避免|禁止(?:将|把|使用|采用)"),
        "存在命令式语气；研究叙述可优先说明纳入条件、判定规则和处置方式。",
    ),
    (
        "EMPTY_CLOSURE",
        "style",
        re.compile(r"由此可见|不难发现|综上所述|这充分说明|具有重要意义|意义深远|提供(?:了)?有益参考"),
        "疑似公式化总结；检查是否增加了新的结果或解释。",
    ),
    (
        "THROAT_CLEARING",
        "style",
        re.compile(r"^\s*(?:随着.{0,30}(?:发展|推进|变化)|在(?:当今|当前).{0,30}背景下|众所周知|在深入讨论.{0,20}之前|值得注意的是)"),
        "段首可能存在无信息铺垫；检查其是否提供必要背景、范围或条件；评价性起笔还应确认评论对象能在本句或紧邻上下文唯一识别。",
    ),
    (
        "DEFENSIVE_CLARIFICATION",
        "semantic-lead",
        re.compile(r"需要说明的是|这并不意味着|不能理解为|不应理解为"),
        "存在澄清句；核对前文是否确有歧义、争议或重要边界。",
    ),
    (
        "ABSTRACT_CHAIN",
        "style",
        re.compile(r"通过.{0,60}实现.{0,60}(?:进而|从而).{0,60}(?:确保|促进|推动)"),
        "一句中可能压缩了多层动作或因果；核对主语、步骤和证据。",
    ),
    (
        "REPEATED_PUNCTUATION",
        "deterministic",
        re.compile(r"[，,]{2,}|[。．.]{2,}|[；;]{2,}|[：:]{2,}"),
        "发现连续标点；核对排版或文本转换是否产生异常。",
    ),
)

FIXED_METHOD_TERMS = (
    "帕累托",
    "5Why",
    "五问法",
    "鱼骨分析",
    "鱼骨图",
    "故障树",
    "BPMN",
    "德尔菲",
    "层次分析法",
    "结构方程",
    "扎根理论",
)

METHOD_TRIGGER_RE = re.compile(r"采用|运用|使用|应用|进行|开展|基于")
METHOD_SUFFIXES = (
    "回归分析",
    "分析法",
    "方法",
    "模型",
    "算法",
    "框架",
    "检验",
    "分析",
    "建模",
    "回归",
    "聚类",
    "网络",
    "估计",
    "优化",
    "匹配",
    "编码",
    "分类",
    "评分",
    "测量",
    "定位",
    "识别",
    "统计",
    "调查",
    "访谈",
    "实验",
    "观察",
    "模拟",
    "仿真",
    "推断",
    "预测",
    "评价",
    "评估",
    "法",
)
METHOD_SUFFIX_PATTERN = "|".join(re.escape(term) for term in METHOD_SUFFIXES)
METHOD_CONTINUATION_PATTERN = (
    r"进行|开展|用于|用以|以便|从而|并据此|得到|获得|完成|构建|建立|"
    r"分析|研究|评价|评估|影响|预测|处理|解释|检验|识别|计算|判定|确定|考察|比较"
)
METHOD_ENTITY_RE = re.compile(
    rf"^(?P<name>[\u4e00-\u9fffA-Za-z0-9·+/_（）()\-–—\s]{{1,36}}?(?:{METHOD_SUFFIX_PATTERN}))"
    rf"(?=$|(?:{METHOD_CONTINUATION_PATTERN}))",
    re.I,
)
FIXED_METHOD_RE = re.compile(
    rf"^(?P<name>{'|'.join(re.escape(term) for term in sorted(FIXED_METHOD_TERMS, key=len, reverse=True))})"
    rf"(?=$|(?:{METHOD_CONTINUATION_PATTERN}))",
    re.I,
)
METHOD_SPLIT_RE = re.compile(r"\s*(?:、|,|，|以及|及|和|与)\s*")
METHOD_ACTION_RE = re.compile(
    r"(?:进行|开展|用于|用以|以便|从而|并据此|得到|获得|完成|构建|建立|"
    r"对(?:数据|样本|材料|对象|结果|关系|问题|字段))"
)
METHOD_ACRONYM_CANDIDATE_RE = re.compile(
    r"(?:采用|运用|使用|应用|基于)\s*"
    r"(?P<name>[A-Za-z][A-Za-z0-9]*(?:[-+/.][A-Za-z0-9]+)*)\s*"
    r"(?P<action>估计|评估|预测|分类|识别|检验|分析|拟合|匹配|建模)",
    re.I,
)

CITATION_RE = re.compile(
    r"\[[0-9０-９]+(?:\s*[-—,，]\s*[0-9０-９]+)*\]"
    r"|\([A-Za-z\u4e00-\u9fff][^()]{0,45},?\s*(?:19|20)\d{2}[a-z]?\)"
    r"|（[A-Za-z\u4e00-\u9fff][^（）]{0,45}[，,]?\s*(?:19|20)\d{2}[a-z]?）"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
CAPTION_RE = re.compile(
    r"^\s*(图|表)\s*([0-9０-９]+(?:\s*[-—.．]\s*[0-9０-９]+)*)"
    r"(?:\s+|[：:.、]\s*).{1,120}$",
    re.I,
)
DISPLAY_REF_RE = re.compile(
    r"(图|表)\s*([0-9０-９]+(?:\s*[-—.．]\s*[0-9０-９]+)*)",
    re.I,
)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?])")
CONNECTOR_RE = re.compile(
    r"^(首先|其次|再次|最后|此外|同时|因此|然而|其中|进一步|具体而言|总体而言|综上所述|由此可见)[，,：:]?"
)
BILINGUAL_NAME_RE = re.compile(r"([\u4e00-\u9fff]{2,20})[（(]([A-Za-z][A-Za-z0-9 /+&.-]{2,50})[）)]")
FULLWIDTH_DIGITS = str.maketrans("０１２３４５６７８９", "0123456789")


def compact_excerpt(text: str, limit: int = 96) -> str:
    value = re.sub(r"\s+", " ", text.strip())
    return value if len(value) <= limit else value[: limit - 1] + "…"


def visible_length(text: str) -> int:
    return len(re.sub(r"\s+|[*_`#>|]", "", text))


def sentence_has_citation(line: str, match_start: int) -> bool:
    left = max(
        line.rfind("。", 0, match_start),
        line.rfind("！", 0, match_start),
        line.rfind("？", 0, match_start),
    )
    rights = [p for mark in "。！？!?" if (p := line.find(mark, match_start)) >= 0]
    right = min(rights) + 1 if rights else len(line)
    return bool(CITATION_RE.search(line[left + 1 : right]))


def mask_fenced_code(lines: Sequence[str]) -> list[str]:
    masked: list[str] = []
    in_fence = False
    fence_char = ""
    fence_length = 0
    for line in lines:
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                in_fence = False
                fence_char = ""
                fence_length = 0
            masked.append("")
        else:
            masked.append("" if in_fence else line)
    return masked


def mask_reference_sections(lines: Sequence[str]) -> list[str]:
    masked = list(lines)
    reference_level: int | None = None
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2)
            if reference_level is not None and level <= reference_level:
                reference_level = None
            if re.search(r"^(?:参考文献|References?)\s*$", title, re.I):
                reference_level = level
        if reference_level is not None:
            masked[index] = ""
    return masked


def iter_prose_paragraphs(lines: Sequence[str]) -> Iterable[tuple[int, str]]:
    start = 0
    parts: list[str] = []

    def flush() -> tuple[int, str] | None:
        nonlocal start, parts
        if not parts:
            return None
        item = (start, " ".join(parts))
        start = 0
        parts = []
        return item

    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        skip = (
            not stripped
            or HEADING_RE.match(line)
            or CAPTION_RE.match(line)
            or stripped.startswith(("|", "![", "- ", "* ", "+ "))
            or bool(re.match(r"^\d+[.)、]\s+", stripped))
        )
        if skip:
            item = flush()
            if item:
                yield item
            continue
        if not parts:
            start = number
        parts.append(stripped.lstrip("> "))
    item = flush()
    if item:
        yield item


def load_glossary(path: Path | None) -> list[GlossaryTerm]:
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    entries: list[GlossaryTerm] = []

    def make_term(preferred: object, variants: object, confusable: object) -> GlossaryTerm:
        if not isinstance(preferred, str) or not preferred.strip():
            raise ValueError("glossary preferred must be a non-empty string")
        if not isinstance(variants, list) or not all(isinstance(v, str) for v in variants):
            raise ValueError("glossary variants must be a string array")
        if not isinstance(confusable, list) or not all(isinstance(v, str) for v in confusable):
            raise ValueError("glossary confusable must be a string array")
        clean_variants = tuple(dict.fromkeys(v for v in variants if v and v != preferred))
        clean_confusable = tuple(dict.fromkeys(v for v in confusable if v and v != preferred))
        return GlossaryTerm(preferred.strip(), clean_variants, clean_confusable)

    if isinstance(data, dict) and "terms" in data:
        terms = data["terms"]
        if not isinstance(terms, list):
            raise ValueError('glossary "terms" must be an array')
        for item in terms:
            if not isinstance(item, dict):
                raise ValueError("each glossary term must be an object")
            entries.append(
                make_term(
                    item.get("preferred"),
                    item.get("variants", []),
                    item.get("confusable", []),
                )
            )
        return entries

    if not isinstance(data, dict):
        raise ValueError("glossary must be an object")
    for preferred, value in data.items():
        if isinstance(value, list):
            entries.append(make_term(preferred, value, []))
        elif isinstance(value, dict):
            entries.append(
                make_term(
                    value.get("preferred", preferred),
                    value.get("variants", []),
                    value.get("confusable", []),
                )
            )
        else:
            raise ValueError(
                'glossary format: {"术语": ["变体"]} or {"terms": [{"preferred": ..., "variants": [], "confusable": []}]}'
            )
    return entries


def audit_patterns(lines: Sequence[str]) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(lines, 1):
        for code, category, pattern, message in PATTERNS:
            for match in pattern.finditer(line):
                if code == "VAGUE_ATTRIBUTION" and sentence_has_citation(line, match.start()):
                    continue
                findings.append(Finding(code, category, number, message, compact_excerpt(line)))
    return findings


def audit_sentence_shape(lines: Sequence[str], long_sentence: int) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, source_line in enumerate(lines, 1):
        if source_line.lstrip().startswith(("#", "|", "关键词", "关键字", "Key words", "Keywords")):
            continue
        for sentence in SENTENCE_SPLIT_RE.split(source_line):
            stripped = sentence.strip()
            if not stripped:
                continue
            punctuation = sum(stripped.count(mark) for mark in "，；：,—")
            if visible_length(stripped) >= long_sentence and punctuation >= 4:
                findings.append(
                    Finding(
                        "LONG_SENTENCE",
                        "statistical",
                        line_number,
                        f"句子约 {visible_length(stripped)} 字且包含多层标点；长句本身不是问题，仅复核多层判断、标点和限定关系是否难以理解。",
                        compact_excerpt(stripped),
                    )
                )
            if stripped.count("；") >= 2:
                findings.append(
                    Finding(
                        "SEMICOLON_CHAIN",
                        "statistical",
                        line_number,
                        "同一句包含多个分号；核对并列关系是否真正平行。",
                        compact_excerpt(stripped),
                    )
                )
            if stripped.count("—") >= 2:
                findings.append(
                    Finding(
                        "DASH_CHAIN",
                        "statistical",
                        line_number,
                        "同一句多次使用破折号；确认补充关系是否清楚。",
                        compact_excerpt(stripped),
                    )
                )
    return findings


def coefficient_of_variation(values: Sequence[int]) -> float:
    mean = statistics.fmean(values)
    return statistics.pstdev(values) / mean if mean else 0.0


def audit_rhythm(
    paragraphs: Sequence[tuple[int, str]],
    sentence_window: int,
    sentence_cv: float,
    paragraph_window: int,
    paragraph_cv: float,
    minimum_paragraph_chars: int,
) -> list[Finding]:
    findings: list[Finding] = []
    sentences: list[tuple[int, str, int]] = []
    for line, paragraph in paragraphs:
        for sentence in SENTENCE_SPLIT_RE.split(paragraph):
            sentence = sentence.strip()
            length = visible_length(sentence)
            if length >= 12:
                sentences.append((line, sentence, length))

    index = 0
    while sentence_window > 1 and index + sentence_window <= len(sentences):
        window = sentences[index : index + sentence_window]
        lengths = [item[2] for item in window]
        if coefficient_of_variation(lengths) <= sentence_cv:
            findings.append(
                Finding(
                    "UNIFORM_SENTENCE_RHYTHM",
                    "statistical",
                    window[0][0],
                    f"连续 {sentence_window} 句长度为 {lengths}，变异系数较低；长度本身不是问题，仅检查句法骨架、信息功能或推进方式是否机械重复。",
                    compact_excerpt(" ".join(item[1] for item in window)),
                )
            )
            index += sentence_window
        else:
            index += 1

    eligible = [(line, text, visible_length(text)) for line, text in paragraphs if visible_length(text) >= minimum_paragraph_chars]
    index = 0
    while paragraph_window > 1 and index + paragraph_window <= len(eligible):
        window = eligible[index : index + paragraph_window]
        lengths = [item[2] for item in window]
        if coefficient_of_variation(lengths) <= paragraph_cv:
            findings.append(
                Finding(
                    "UNIFORM_PARAGRAPH_LENGTH",
                    "statistical",
                    window[0][0],
                    f"连续 {paragraph_window} 段长度为 {lengths}，变异系数较低；长度本身不是问题，仅检查段落功能和组织方式是否机械同构。",
                    compact_excerpt(" | ".join(item[1] for item in window)),
                )
            )
            index += paragraph_window
        else:
            index += 1
    return findings


def audit_connectors(paragraphs: Sequence[tuple[int, str]], window_size: int = 6) -> list[Finding]:
    starts: list[tuple[int, str, str]] = []
    for line, paragraph in paragraphs:
        for sentence in SENTENCE_SPLIT_RE.split(paragraph):
            stripped = sentence.strip()
            match = CONNECTOR_RE.match(stripped)
            if match:
                starts.append((line, match.group(1), stripped))
    findings: list[Finding] = []
    index = 0
    while index + 3 <= len(starts):
        window = starts[index : index + window_size]
        counts = Counter(item[1] for item in window)
        connector, count = counts.most_common(1)[0]
        if count >= 3:
            first = next(item for item in window if item[1] == connector)
            findings.append(
                Finding(
                    "REPEATED_CONNECTOR",
                    "statistical",
                    first[0],
                    f"相邻句群中“{connector}”作为句首连接词出现 {count} 次；检查逻辑关系是否机械重复。",
                    compact_excerpt(" ".join(item[2] for item in window if item[1] == connector)),
                )
            )
            index += len(window)
        else:
            index += 1
    return findings


def audit_translation_patterns(paragraphs: Sequence[tuple[int, str]]) -> list[Finding]:
    findings: list[Finding] = []
    bilingual: dict[tuple[str, str], list[tuple[int, str]]] = {}
    for line, paragraph in paragraphs:
        for clause in re.split(r"[，,；;。！？!?：:]", paragraph):
            if clause.count("的") >= 4 and visible_length(clause) >= 18:
                findings.append(
                    Finding(
                        "LONG_DE_CHAIN",
                        "statistical",
                        line,
                        f"同一分句包含 {clause.count('的')} 个“的”；检查所属、分类和动作关系是否需要拆开。",
                        compact_excerpt(clause),
                    )
                )
        qi_count = paragraph.count("其")
        density = qi_count * 100 / max(visible_length(paragraph), 1)
        if qi_count >= 3 and density >= 1.5:
            findings.append(
                Finding(
                    "HIGH_QI_DENSITY",
                    "statistical",
                    line,
                    f"本段“其”出现 {qi_count} 次（约 {density:.1f}/100 字）；核对每处是否有唯一先行词。",
                    compact_excerpt(paragraph),
                )
            )
        for match in BILINGUAL_NAME_RE.finditer(paragraph):
            key = (match.group(1), re.sub(r"\s+", " ", match.group(2)).lower())
            bilingual.setdefault(key, []).append((line, match.group(0)))
    for occurrences in bilingual.values():
        for line, text in occurrences[1:]:
            findings.append(
                Finding(
                    "REPEATED_BILINGUAL_NAME",
                    "deterministic",
                    line,
                    "同一中英文名称重复并列；检查是否仅需在首次出现时双写。",
                    compact_excerpt(text),
                )
            )
    return findings


def audit_glossary(lines: Sequence[str], glossary: Sequence[GlossaryTerm]) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(lines, 1):
        for term in glossary:
            for variant in term.variants:
                if variant in line:
                    findings.append(
                        Finding(
                            "TERM_VARIANT",
                            "deterministic",
                            number,
                            f"术语“{variant}”应与规范名称“{term.preferred}”核对。",
                            compact_excerpt(line),
                        )
                    )
            for candidate in term.confusable:
                if candidate in line:
                    findings.append(
                        Finding(
                            "TERM_CONFUSABLE",
                            "semantic-lead",
                            number,
                            f"“{candidate}”与“{term.preferred}”语义接近但不可自动替换；请按上下文判断。",
                            compact_excerpt(line),
                        )
                    )
    return findings


def clean_method_candidate(value: str) -> str:
    value = re.sub(r"^(?:本研究|本文|研究中|主要|综合|一种|该)", "", value.strip())
    value = METHOD_TRIGGER_RE.split(value)[-1]
    value = re.sub(r"(?:等|相结合|组合)$", "", value.strip())
    return value.strip(" 的、,，")


def extract_method_entity(value: str) -> str | None:
    candidate = clean_method_candidate(value)
    if not candidate:
        return None
    match = METHOD_ENTITY_RE.match(candidate) or FIXED_METHOD_RE.match(candidate)
    if not match:
        return None
    name = re.sub(r"\s+", " ", match.group("name")).strip()
    return name if 1 < len(name) <= 36 else None


def extract_method_declarations(lines: Sequence[str]) -> list[tuple[str, int]]:
    declarations: list[tuple[str, int]] = []
    for number, line in enumerate(lines, 1):
        for trigger in METHOD_TRIGGER_RE.finditer(line):
            segment = line[trigger.end() : trigger.end() + 120]
            segment = re.split(r"[。；：\n]", segment, maxsplit=1)[0]
            segment = METHOD_ACTION_RE.split(segment, maxsplit=1)[0]
            for part in METHOD_SPLIT_RE.split(segment):
                name = extract_method_entity(part)
                if name:
                    declarations.append((name, number))
            break
    return declarations


def audit_method_closure(lines: Sequence[str]) -> tuple[list[Finding], list[MethodDeclaration]]:
    findings: list[Finding] = []
    text = "\n".join(lines)
    lowered = text.lower()
    raw_declarations = extract_method_declarations(lines)
    unique: dict[str, int] = {}
    for name, line in raw_declarations:
        unique.setdefault(name, line)
    declarations: list[MethodDeclaration] = []
    for name, line in unique.items():
        mentions = lowered.count(name.lower())
        declarations.append(MethodDeclaration(name, line, mentions))
        if mentions <= 1:
            findings.append(
                Finding(
                    "METHOD_DECLARATION_LOW_MENTION",
                    "semantic-lead",
                    line,
                    f"动态识别到方法声明“{name}”，全文字面出现 {mentions} 次；用方法—结果矩阵复核实际应用。",
                    name,
                )
            )
    declared_lower = {item.name.lower() for item in declarations}
    for term in FIXED_METHOD_TERMS:
        count = lowered.count(term.lower())
        if count == 1 and not any(term.lower() in name or name in term.lower() for name in declared_lower):
            position_line = next((i for i, line in enumerate(lines, 1) if term.lower() in line.lower()), 1)
            findings.append(
                Finding(
                    "METHOD_SINGLE_MENTION",
                    "statistical",
                    position_line,
                    f"辅助词表中的方法“{term}”全文只出现一次；该线索不能替代方法—结果语义审计。",
                    term,
                )
            )
    declarations.sort(key=lambda item: (item.line, item.name))
    return findings, declarations


def audit_method_acronym_candidates(lines: Sequence[str]) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(lines, 1):
        for match in METHOD_ACRONYM_CANDIDATE_RE.finditer(line):
            name = match.group("name")
            action = match.group("action")
            findings.append(
                Finding(
                    "METHOD_ACRONYM_CANDIDATE",
                    "semantic-lead",
                    number,
                    f"“{name}”后接“{action}”动作，可能是缩写方法或算法，也可能是软件或工具；请经语义确认后再纳入方法表。",
                    compact_excerpt(line),
                )
            )
    return findings


def normalize_label(kind: str, number: str) -> str:
    number = number.translate(FULLWIDTH_DIGITS)
    number = re.sub(r"\s*[-—.．]\s*", "-", number)
    return f"{kind}{number}"


def audit_displays(lines: Sequence[str]) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    captions: dict[str, list[tuple[int, str]]] = {}
    references: dict[str, list[tuple[int, str]]] = {}
    caption_lines: set[int] = set()
    for number, line in enumerate(lines, 1):
        match = CAPTION_RE.match(line)
        if match:
            label = normalize_label(match.group(1), match.group(2))
            captions.setdefault(label, []).append((number, line))
            caption_lines.add(number)
    for number, line in enumerate(lines, 1):
        if number in caption_lines:
            continue
        for match in DISPLAY_REF_RE.finditer(line):
            label = normalize_label(match.group(1), match.group(2))
            references.setdefault(label, []).append((number, line))

    for label, items in captions.items():
        if len(items) > 1:
            for number, line in items[1:]:
                findings.append(
                    Finding(
                        "DISPLAY_DUPLICATE_LABEL",
                        "deterministic",
                        number,
                        f"{label} 出现重复题注；核对编号。",
                        compact_excerpt(line),
                    )
                )
        if label not in references:
            number, line = items[0]
            findings.append(
                Finding(
                    "DISPLAY_UNCITED",
                    "deterministic",
                    number,
                    f"{label} 只在题注中出现；检查正文是否引用并解释该图表。",
                    compact_excerpt(line),
                )
            )
    for label, items in references.items():
        if label not in captions:
            number, line = items[0]
            findings.append(
                Finding(
                    "DISPLAY_REFERENCE_MISSING",
                    "deterministic",
                    number,
                    f"正文引用 {label}，但未找到对应题注。",
                    compact_excerpt(line),
                )
            )
    return findings, sorted(captions)


def audit_sections(lines: Sequence[str], minimum_chars: int) -> list[Finding]:
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2)))
    findings: list[Finding] = []
    for position, (index, level, title) in enumerate(headings):
        if level == 1 or re.search(r"参考文献|附录|致谢|修改说明|审计记录|正文外", title, re.I):
            continue
        next_index = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        has_child = position + 1 < len(headings) and headings[position + 1][1] > level
        if has_child:
            continue
        body = lines[index + 1 : next_index]
        prose_lines = [
            line.strip()
            for line in body
            if line.strip()
            and not line.lstrip().startswith(("#", "|", "![", "- ", "* ", "+ "))
            and not re.match(r"^\d+[.)、]\s+", line.strip())
            and not CAPTION_RE.match(line)
        ]
        prose = "".join(prose_lines)
        length = visible_length(prose)
        if length < minimum_chars:
            findings.append(
                Finding(
                    "THIN_SECTION",
                    "structural",
                    index + 1,
                    f"叶节点小节正文约 {length} 字；检查它是否仅由图表、列表或一句结论承担。",
                    compact_excerpt(title),
                )
            )
    return findings


def deduplicate(findings: Sequence[Finding]) -> list[Finding]:
    seen: set[tuple[str, int, str]] = set()
    result: list[Finding] = []
    for item in sorted(findings, key=lambda x: (x.line, x.code, x.excerpt)):
        key = (item.code, item.line, item.excerpt)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def render_text(path: Path, findings: Sequence[Finding]) -> str:
    counts = Counter(item.code for item in findings)
    categories = Counter(item.category for item in findings)
    output = [
        f"审计文件：{path}",
        "说明：以下为人工复核线索，不是作者身份判定、质量评分或自动修改命令。",
        "",
    ]
    if not findings:
        output.append("未发现脚本能够识别的风险线索；仍需进行证据、引用和语义人工核查。")
        return "\n".join(output)
    output.append("类别计数：" + "，".join(f"{key}={value}" for key, value in sorted(categories.items())))
    output.append("规则计数：" + "，".join(f"{key}={value}" for key, value in sorted(counts.items())))
    output.append("")
    for item in findings:
        output.append(f"L{item.line} [{item.code}] {item.message}")
        output.append(f"  {item.excerpt}")
    return "\n".join(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 Markdown or plain-text file")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--glossary", type=Path, help="JSON glossary; legacy and terms-array schemas are supported")
    parser.add_argument("--long-sentence", type=int, default=100, help="minimum visible characters for long-sentence review")
    parser.add_argument(
        "--minimum-section-chars",
        type=int,
        default=100,
        help="minimum prose characters for Markdown leaf sections",
    )
    parser.add_argument("--sentence-rhythm-window", type=int, default=6, help="sentence count in rhythm window")
    parser.add_argument("--sentence-rhythm-cv", type=float, default=0.12, help="maximum coefficient of variation for rhythm lead")
    parser.add_argument("--paragraph-rhythm-window", type=int, default=4, help="paragraph count in rhythm window")
    parser.add_argument("--paragraph-rhythm-cv", type=float, default=0.12, help="maximum coefficient of variation for paragraph lead")
    parser.add_argument("--minimum-paragraph-chars", type=int, default=60, help="minimum paragraph length included in rhythm checks")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (
        args.long_sentence < 1
        or args.minimum_section_chars < 0
        or args.sentence_rhythm_window < 2
        or args.paragraph_rhythm_window < 2
        or args.minimum_paragraph_chars < 1
        or not 0 <= args.sentence_rhythm_cv <= 1
        or not 0 <= args.paragraph_rhythm_cv <= 1
    ):
        raise ValueError("thresholds are outside their allowed ranges")

    text = args.input.read_text(encoding="utf-8-sig")
    source_lines = text.splitlines()
    active_lines = mask_fenced_code(source_lines)
    content_lines = mask_reference_sections(active_lines)
    has_markdown_headings = any(HEADING_RE.match(line) for line in active_lines)
    glossary = load_glossary(args.glossary)
    paragraphs = list(iter_prose_paragraphs(content_lines))

    method_findings, declarations = audit_method_closure(content_lines)
    display_findings, display_labels = audit_displays(active_lines)
    findings = deduplicate(
        audit_patterns(content_lines)
        + audit_sentence_shape(content_lines, args.long_sentence)
        + audit_rhythm(
            paragraphs,
            args.sentence_rhythm_window,
            args.sentence_rhythm_cv,
            args.paragraph_rhythm_window,
            args.paragraph_rhythm_cv,
            args.minimum_paragraph_chars,
        )
        + audit_connectors(paragraphs)
        + audit_translation_patterns(paragraphs)
        + audit_glossary(content_lines, glossary)
        + audit_method_acronym_candidates(content_lines)
        + method_findings
        + display_findings
        + audit_sections(active_lines, args.minimum_section_chars)
    )

    if args.format == "json":
        payload = {
            "file": str(args.input),
            "disclaimer": "editorial navigation only; not authorship detection, quality scoring, or an automatic rewrite decision",
            "document": {
                "lines": len(source_lines),
                "visible_characters": visible_length("\n".join(content_lines)),
                "prose_paragraphs": len(paragraphs),
                "structure_scope": "markdown_heading_tree" if has_markdown_headings else "plain_text_no_heading_tree",
                "display_labels": display_labels,
                "declared_methods": [asdict(item) for item in declarations],
                "glossary_terms": len(glossary),
            },
            "parameters": {
                "long_sentence": args.long_sentence,
                "minimum_section_chars": args.minimum_section_chars,
                "sentence_rhythm_window": args.sentence_rhythm_window,
                "sentence_rhythm_cv": args.sentence_rhythm_cv,
                "paragraph_rhythm_window": args.paragraph_rhythm_window,
                "paragraph_rhythm_cv": args.paragraph_rhythm_cv,
                "minimum_paragraph_chars": args.minimum_paragraph_chars,
            },
            "counts_by_category": dict(sorted(Counter(item.category for item in findings).items())),
            "counts_by_code": dict(sorted(Counter(item.code for item in findings).items())),
            "findings": [asdict(item) for item in findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(args.input, findings))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"audit error: {exc}", file=sys.stderr)
        raise SystemExit(2)
