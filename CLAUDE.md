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

换乘恋爱-冬日之约/  — ENHYPEN 换乘恋爱同人小说（ABO世界观，非互动/纯叙事）
  剧情存档/
    换乘恋爱-冬日之约-Day1-3.txt     Day 1-3 完整剧情
    换乘恋爱-冬日之约-Day1-6.txt     Day 1-6 完整剧情（写作中）
    角色设定.txt                    人物设定参数
    游戏机制说明.txt                 世界观/状态变量逻辑

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
