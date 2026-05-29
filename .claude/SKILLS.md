# Claude Code Skills 触发场景说明

本文档说明已安装 skills 的适用场景、触发时机与典型用法。Skills 安装在全局目录：

```
C:\Users\38993\.claude\skills\
```

在 Claude Code 中可通过**自然语言提及 skill 名称**，或使用 **`/skill-name`** 斜杠命令（部分 skill 支持）。重启 Claude Code 后生效。

---

## 快速对照表

| Skill | 一句话场景 | 典型触发词 |
|-------|-----------|-----------|
| `using-superpowers` | 每次新会话的入口，规定如何查找并调用其他 skill | 开始任何对话时自动/手动加载 |
| `brainstorming` | 动手写代码前，先澄清需求与设计 | 新功能、改行为、做组件 |
| `writing-plans` | 有需求后，拆成可执行计划（先计划后编码） | 多步骤任务、有 spec 要实现 |
| `planning-with-files` | 复杂任务用文件持久化计划与进度 | 5+ 步、研究型、跨会话任务 |
| `using-git-worktrees` | 需要隔离工作区再开工 | 新 feature 分支、执行计划前 |
| `test-driven-development` | 写实现代码之前先写测试 | 新功能、修 bug |
| `subagent-driven-development` | 按计划逐任务执行，任务间做审查 | 有计划、任务可独立并行 |
| `dispatching-parallel-agents` | 多个互不依赖的任务同时推进 | 2+ 独立子任务 |
| `executing-plans` | 在单独会话中执行已写好的计划 | 已有 implementation plan |
| `systematic-debugging` | 遇到 bug 或测试失败，先调查再修 | 报错、行为异常、测试红 |
| `requesting-code-review` | 完成功能后主动发起代码审查 | 大功能完成、合并前 |
| `code-review` | 同上（合并版 skill） | PR 审查、合并前验证 |
| `receiving-code-review` | 收到审查意见后，理性评估再改 | 别人给了 review 评论 |
| `verification-before-completion` | 声称「做完了」之前必须跑验证 | 要 commit、提 PR、说 fixed |
| `finishing-a-development-branch` | 开发完成，决定 merge/PR/清理 | 测试全绿、要收尾 |
| `writing-skills` | 编写或验证新 skill | 写 SKILL.md、改 skill |
| `skill-creator` | 创建 skill 并做 eval 迭代 | 从零做 skill、优化触发描述 |
| `frontend-design` | 做有设计感的前端界面 | 网页、组件、应用 UI |
| `pdf` | 一切 PDF 相关操作 | .pdf、合并、表单、OCR |
| `humanizer-zh` | 去除中文文本的 AI 写作痕迹 | 润色、去 AI 味、改写文章 |
| `web-access` | 联网搜索、抓取、浏览器 CDP 操作 | 搜资料、抓网页、登录站点 |
| `docx` | Word 文档创建/编辑/提取 | .docx、报告、备忘录 |
| `xlsx` | 电子表格读写与清洗 | .xlsx、.csv、公式、图表 |
| `pptx` | 演示文稿创建与编辑 | slides、deck、.pptx |
| `pua` | AI 反复失败时加压、换思路 | 加油、别偷懒、/pua |
| `code-interpreter` | 沙箱里跑代码验证逻辑 | 调试、试算法、装包测试 |
| `ui-ux-pro-max` | 专业 UI/UX 设计系统与规范 | 落地页、Dashboard、配色字体 |
| `web-accessibility` | Web 无障碍审计与修复 | WCAG、a11y、axe 报错 |

---

## 一、写作与内容

### humanizer-zh

**何时触发**

- 润色 AI 生成的文章、README、文档、小说段落
- 审阅文本，发现「AI 味」太重（套话、三段式、破折号堆砌、宣传腔）
- 需要让文字更像人写的，而非机器模板

**不要触发**

- 纯技术代码审查（用 `code-review`）
- 只需要改错别字、不涉及文风（直接编辑即可）

**示例说法**

```
/humanizer-zh 请人性化下面这段文字：……
用 humanizer 改一下 NOVEL 里这一章，去掉 AI 痕迹
```

---

## 二、文档处理

### pdf

**何时触发**

- 读取、提取 PDF 中的文字或表格
- 合并、拆分、旋转页面、加水印
- 新建 PDF、填写表单、加解密
- 从扫描件 OCR 成可搜索 PDF
- 用户提到任意 `.pdf` 文件或要求「生成 PDF」

**不要触发**

- Word（`.docx`）—— 本 skill 专用于 PDF
- 仅需把 Markdown 转 PDF 且没有复杂版式时，可先问用户是否接受简单方案

**示例说法**

```
用 pdf skill 提取这份表单的字段
把这三个 PDF 合并成一个
```

---

## 三、前端设计

### frontend-design

**何时触发**

- 搭建网页、组件、单页应用或完整前端界面
- 需要**有辨识度**的 UI，避免千篇一律的「AI 审美」
- 用户强调设计感、品牌感、视觉风格

**不要触发**

- 纯后端 API、脚本、数据处理
- 只改一个 CSS 颜色等极小改动（不必整套 design thinking）

**示例说法**

```
用 frontend-design 做一个番茄钟风格的设置页
帮我设计一个小说创作工作台界面，偏编辑杂志风
```

---

## 四、规划与任务管理

### planning-with-files

**何时触发**

- 多步骤项目（预计需要 **5 次以上** 工具调用）
- 研究型任务、需要跨多次对话持续推进
- 希望用 `task_plan.md`、`findings.md`、`progress.md` 持久化进度
- `/clear` 之后要从文件恢复上下文

**工作流要点**

1. 创建 `task_plan.md`（阶段与目标）
2. 研究发现写入 `findings.md`
3. 操作记录写入 `progress.md`
4. 重大决策前重读计划

**不要触发**

- 单行改 typo、一次就能答完的问题
- 已有明确超短指令且无需留档

**示例说法**

```
/planning-with-files 规划挪威旅行文档生成流程
用 planning with files 拆解这个刷题 App 的重构
```

> 完整 hooks（自动注入计划、完成检查）需额外安装 `planning-with-files` **插件**；当前为 skill 版，主要靠 agent 按 SKILL.md 执行。

---

## 五、代码审查

### code-review / requesting-code-review

**何时触发**

- 完成一个功能或较大改动，合并或提 PR 之前
- 需要独立视角检查正确性、安全、是否符合项目规范
- 用户明确要求「review 一下」「看看 PR」

**区别**

| Skill | 角色 |
|-------|------|
| `code-review` | 合并入口，派发审查子 agent |
| `requesting-code-review` | Superpowers 原版，语义相同 |

二者保留其一即可；日常说「code review」会匹配到 `code-review`。

### receiving-code-review

**何时触发**

- 收到他人（或子 agent）的 review 意见之后
- 准备在改代码之前，需要**甄别**意见是否合理
- 反馈含糊或可能有误时，避免盲目照做

**不要触发**

- 还没有 review 意见，只是要写代码（用 TDD / brainstorming）

---

## 六、Skill 创作

### skill-creator

**何时触发**

- 从零创建新 skill
- 修改、优化已有 skill 的 SKILL.md
- 跑 eval、benchmark、优化 `description` 以提高触发准确率

**配套工具**

- `scripts/quick_validate.py` — 校验格式
- `scripts/run_eval.py` — 跑评测
- `eval-viewer/` — 查看结果

### writing-skills

**何时触发**

- 编写或编辑 skill 的**结构与文风**（Superpowers 系写法）
- 部署前验证 skill 是否可被正确触发
- 与 `skill-creator` 互补：前者偏流程与规范，后者偏工具与 eval

**示例说法**

```
帮我写一个用于生成 Word 文档的 skill
优化 humanizer-zh 的 description，让它更容易被触发
```

---

## 七、Superpowers 开发工作流

Superpowers 是一套**有顺序**的工程实践 skills。推荐在「正经写代码」的任务中按下面链路使用。

```
using-superpowers（入口）
    ↓
brainstorming（澄清需求与设计，禁止直接开写）
    ↓
writing-plans（拆成 2–5 分钟小任务 + 文件路径）
    ↓
[可选] planning-with-files（复杂任务持久化到 md）
    ↓
using-git-worktrees（隔离工作区）
    ↓
test-driven-development（先红后绿）
    ↓
subagent-driven-development 或 executing-plans（执行）
    ↓
dispatching-parallel-agents（仅当子任务彼此独立）
    ↓
systematic-debugging（遇 bug 时插入）
    ↓
requesting-code-review / code-review
    ↓
verification-before-completion（声称完成前跑测试/构建）
    ↓
finishing-a-development-branch（merge / PR / 清理）
```

### 各 skill 触发细节

| Skill | 触发时机 |
|-------|---------|
| **using-superpowers** | **每次新对话开始**；要求先查 skill 再回复（含澄清问题） |
| **brainstorming** | 任何创意/功能/组件/行为修改的**第一步**；先问清楚再写代码 |
| **writing-plans** | 已有 spec 或需求，**动手改代码之前** |
| **using-git-worktrees** | 开新 feature 或执行计划前，需要与当前工作区隔离 |
| **test-driven-development** | 实现任何 feature 或 bugfix，**写实现代码之前** |
| **subagent-driven-development** | 当前会话执行计划，任务相对独立，任务间穿插 review |
| **executing-plans** | 已有书面计划，在**另一次会话**中执行（带检查点） |
| **dispatching-parallel-agents** | 同时有 2+ 个**无共享状态、无先后顺序**的任务 |
| **systematic-debugging** | 任何 bug、测试失败、意外行为；**提出修复方案之前** |
| **verification-before-completion** | 要说「完成了 / 修好了 / 测试过了」之前；必须看到命令输出 |
| **finishing-a-development-branch** | 实现完成且测试通过，决定如何合并或开 PR |

**示例说法**

```
用 superpowers 流程做这个功能
先 brainstorming 再写代码
按 TDD 实现这个 bugfix
```

> Superpowers 的 **SessionStart 自动注入**需安装 `obra/superpowers` 插件；当前为 skill 版，需在对话中主动提及 `using-superpowers` 或「按 superpowers 流程」。

---

## 八、按任务类型选 Skill

| 你想做的事 | 优先使用的 Skill |
|-----------|-----------------|
| 改小说/文章，去 AI 味 | `humanizer-zh` |
| 处理 PDF | `pdf` |
| 做漂亮网页/UI | `frontend-design` |
| 大项目拆步骤、记进度 | `planning-with-files` |
| 新功能从 0 到 1 | `brainstorming` → `writing-plans` → `test-driven-development` |
| 修 bug | `systematic-debugging` |
| 准备合并代码 | `code-review` → `verification-before-completion` |
| 别人 review 了你 | `receiving-code-review` |
| 写自己的 skill | `skill-creator` + `writing-skills` |
| 不确定用哪个 | `using-superpowers` |

---

## 九、安装位置与更新

```
C:\Users\38993\.claude\skills\
├── humanizer-zh\
├── pdf\
├── frontend-design\
├── planning-with-files\
├── skill-creator\
├── code-review\
├── using-superpowers\      # Superpowers 入口
├── brainstorming\          # … 等 14 个 Superpowers 子 skill
└── …
```

**更新单个 skill（网络正常时）**

```bash
npx skills add eze-is/web-access -g -y -a claude-code --copy
npx skills add anthropics/skills -g -y -a claude-code --copy -s docx -s xlsx -s pptx
npx skills add tanweai/pua -g -y -a claude-code --copy -s pua
npx skills add nextlevelbuilder/ui-ux-pro-max-skill -g -y -a claude-code --copy -s ui-ux-pro-max
npx skills add akillness/oh-my-skills -g -y -a claude-code --copy -s web-accessibility
npx skills add aws-samples/sample-strands-agent-with-agentcore -g -y -a claude-code --copy -s code-interpreter
```

**列出已安装**

```bash
npx skills ls -g
```

---

## 十、与本项目（TESTuser）的结合建议

| 项目场景 | 推荐 Skill |
|---------|-----------|
| 续写 / 润色 `🦊相遇.txt` | `humanizer-zh` |
| 生成旅行计划 Word / PDF | `docx` + `pdf` + `planning-with-files` |
| 改 `番茄钟.html` 界面 | `frontend-design` 或 `ui-ux-pro-max` |
| 审查番茄钟无障碍 | `web-accessibility` |
| 查挪威旅行资料 | `web-access` |
| 刷题 App / Python 工具开发 | Superpowers 全链路 + `code-review` |
| 为小说工作台写专用 skill | `skill-creator` |

可在项目 `CLAUDE.md` 中加一句：「复杂任务优先读 `.claude/SKILLS.md` 选择 skill。」
