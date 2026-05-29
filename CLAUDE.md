# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a mixed-content project centered on creative writing (interactive ABO-universe fiction featuring K-pop group ENHYPEN's Sunoo) with supporting utility tools and documents.

## Agent Skills

For complex or multi-step tasks, read [`.claude/SKILLS.md`](.claude/SKILLS.md) first and choose the appropriate skill (e.g. `humanizer-zh` for prose editing, `frontend-design` for UI, `planning-with-files` for large tasks, Superpowers workflow for feature development).


- `🦊相遇.txt` — Main interactive fiction file (~15K lines, ~1MB). Written in script/roleplay format with date-location headers and third-person narrative. Follows ABO universe rules with ENHYPEN members.
- `番茄钟.html` — Self-contained Pomodoro timer app (HTML + CSS + JS). Open directly in browser, no build step needed.
- `word_template.ps1` — PowerShell script using COM to generate Word documents (requires Microsoft Office installed).
- `sunoo/` — Image assets (idol photos).
- Various `.docx` files — Analysis reports and documents.

## HTML App (番茄钟.html)

Single-page app with zero dependencies. Features:
- Pomodoro timer with work/break cycles
- LocalStorage-based settings persistence
- Desktop notifications
- Keyboard shortcuts (Space = start/pause, R = reset)
- Catppuccin-themed dark UI with SVG progress ring

To run: open `番茄钟.html` in any modern browser.

## PowerShell Script (word_template.ps1)

COM-based Word document generation template. Requires Microsoft Office. Usage:
```powershell
# Edit $OutputPath and content sections as needed, then:
powershell -File word_template.ps1
```

## Creative Writing Convention (🦊相遇.txt)

- Entries begin with `<日期、地点>` (date, location) header
- Written in third-person narrative
- Uses ABO universe world-building rules
- Character KIM SUNOO (金善禹) is the protagonist, an ENHYPEN member
- Dialogues and actions describe interactions with character "小茶"
