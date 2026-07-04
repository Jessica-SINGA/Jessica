# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a mixed-content project centered on creative writing (interactive ABO-universe fiction featuring K-pop group ENHYPEN's Sunoo) with supporting utility tools and documents.

## Agent Skills

For complex or multi-step tasks, read [`.claude/SKILLS.md`](.claude/SKILLS.md) first and choose the appropriate skill (e.g. `humanizer-zh` for prose editing, `frontend-design` for UI, `planning-with-files` for large tasks, Superpowers workflow for feature development).

## Directory Structure

```
novel-writing/     — 相遇 interactive fiction + analysis docs
  🦊相遇.txt           Main interactive fiction (~15K lines, ~1MB)
  相遇分析报告.docx
  番茄都市言情top20.docx

transit-love-sim/  — ENHYPEN 换乘恋爱 simulator prompt
  换乘恋爱-ENHYPEN-simulator.md

norway-travel/     — Norway aurora travel plans + Seoul plan
  travel_plan_v2.html, travel_plan.html, seoul_plan.html
  *.docx (travel plans), generate_travel_plan.py
  norway_research.md, norway-news-data.json, norway-icon.svg
  word_template.ps1

pomodoro/          — Pomodoro timer app
  番茄钟.html

flight-tracker/    — Flight price tracker data
  flight-prices.json

social-pages/      — Social media travel pages
  social-check.html, social-travel-plans.html

study-app/         — Study tool
  study.html, study_manifest.json

cpa/               — CPA exam materials
  CPAaccountingbook1.pdf

images/            — Image assets
  sunoo/           Idol photos
```

## HTML App (pomodoro/番茄钟.html)

Single-page app with zero dependencies. Features:
- Pomodoro timer with work/break cycles
- LocalStorage-based settings persistence
- Desktop notifications
- Keyboard shortcuts (Space = start/pause, R = reset)
- Catppuccin-themed dark UI with SVG progress ring

To run: open `pomodoro/番茄钟.html` in any modern browser.

## PowerShell Script (norway-travel/word_template.ps1)

COM-based Word document generation template. Requires Microsoft Office. Usage:
```powershell
powershell -File norway-travel/word_template.ps1
```

## Writing Quality Standards（所有写作任务通用）

以下规则适用于每次写作，无论是小说、对话、剧情还是其他任何文字创作：

### 1. 代词检查（必须做）
- 全文扫描「他」「她」使用是否正确（金善禹=他，小茶=她）
- 完成后必须用脚本或手动确认零错误

### 2. 禁止破折号
- 全文不允许出现「——」（中文破折号）
- 需要用省略或停顿的地方用「……」代替
- 需要断句的地方用句号断句，不用破折号连接

### 3. 每次写作完成后必须用 humanizer-zh skill 润色
- 删除「不是……而是……」句式
- 删除三段式列举
- 控制句子长短节奏
- 删除填充短语（值得注意的是、此外、与此同时等）
- 删除"金句"式结尾
- 删除模糊归因（专家认为、有人指出等）
- 自然化语言，避免AI腔
- 润色后评分须 ≥ 35/50

### 4. ABO写作惯例（适用时）
- 信息素描写贯穿全程，不可只在开头提一次
- Alpha的压制感和Omega的身体反应要匹配
- 标记过程包含腺体咬合+信息素注入两个步骤
- 标记后信息素交融，气味混合

## Creative Writing Convention (novel-writing/🦊相遇.txt)

- Entries begin with `<日期、地点>` (date, location) header
- Written in third-person narrative
- Uses ABO universe world-building rules
- Character KIM SUNOO (金善禹) is the protagonist, an ENHYPEN member
- Dialogues and actions describe interactions with character "小茶"

## Transit Love Simulator (transit-love-sim/)

- Copy the full prompt into a new Claude Code session to play
- User controls 小茶; Claude plays host + 7 other characters
- Use `/humanizer-zh`, `/humanize-chinese`, `/chinese-novelist` during gameplay for polish
