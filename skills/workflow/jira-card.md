---
name: workflow-jira-card
description: Write or rewrite one Jira work card in the fixed five-section Korean template, readable without the codebase and free of analysis dumps.
tags: [workflow, planning, jira]
stability: experimental
---

# Workflow — Jira Card

## Purpose

Turn a discussed feature, fix, or task into one Jira card a teammate can read
in two minutes. The section template is fixed; the wording is plain Korean;
reasoning stays out of the card. Writes nothing but the card.

## Startup

1. Target: an issue key or URL means rewrite — read its title, body, and linked
   issues first. No key means a new card; ask for the project key only if the
   repository or recent cards do not reveal it.
2. Read only what the card must point to: the plan or design decision, one or
   two sibling cards for voice, and the few code files the card names.
3. Begin with `Mode: new | rewrite | Target: <key or paste>` and nothing before it.

## Template (sections and order are fixed)

```markdown
## 개요
* …

## 작업 내용 (Checkbox)
- [ ] …

## 영향 범위
* **서비스/모듈**: …
* **API 변경**: 있음 / 없음 (한 줄 이유)
* **DB 변경**: 있음 / 없음 (한 줄 이유)

## 테스트 확인 (Checkbox)
- [ ] …

## 참고
* 관련 이슈: [KEY 제목](url)(관계 한 구절)
* 문서/링크: 경로 + 절
```

## Writing rules

- `개요` is 3–6 bullets, noun-ending Korean (`…함`, `…음`), in this order:
  what it is, why now, how in one line, what differs from the plan or current
  code, what is out of scope. Mention the ticket it was split from or merged into.
- One settled decision is one bullet. One open decision is one bullet that names
  the options and the preferred one with its deciding reason.
- `작업 내용` has 5–9 checkboxes, one concern each, in build order. No `S1/S2`
  prefixes, no path lists; at most one path or identifier per item.
- `테스트 확인` lists observable outcomes (`…한다`, `…이 나온다`). Put the
  project's standard check command last when sibling cards do.
- `영향 범위` names repositories and modules in words, not trees.
- If a sentence took analysis to reach, keep the conclusion and drop the path
  to it. Never paste chat history, option matrices, or code.
- Match the voice of sibling cards over this file when they differ.
- Target under 60 rendered lines.

## Writing to Jira

- With an Atlassian tool and an explicit request to write, create or edit the
  issue with `contentFormat: html`. Checkboxes must be
  `<ul data-type="task-list"><li data-type="task-item"><input type="checkbox"> …</li></ul>`;
  markdown `- [ ]` is stored as literal text.
- Re-read the issue after saving and fix mojibake or typos in the same turn.
- Without a tool, output the markdown ready to paste.
- Renaming or rewriting another person's card: do it only when asked, and say
  so in the reply.

## Prohibited

- Never change code, tests, configuration, or documents other than the card.
- Never invent scope, dates, owners, or estimates that were not discussed.
- Never leave a template section out; use `-` when it is empty.

## Completion

Report the issue key or that the text is ready to paste, and list the decisions
the card leaves open.
