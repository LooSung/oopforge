---
name: workflow-jira-card
description: Write or rewrite one Jira task, story, bug, or epic in the fixed Korean template for that type, without changing code.
tags: [workflow, planning, jira]
stability: experimental
---

# Workflow — Jira Card

## Purpose

Turn a discussed change into one Jira issue a teammate can read in two minutes.
The type chooses the template. Wording is plain Korean. Reasoning stays out of
the card. Writes nothing but that one issue.

## Startup

1. Target: an issue key or URL means rewrite — read its title, body, and linked
   issues first. No key means a new issue; ask for the project key only if the
   repository or recent issues do not reveal it.
2. Read only what the card must point to: the plan or design decision, one or
   two sibling issues for voice, and the few code files the card names.
3. Choose one type. `버그` or `bug` selects bug. `에픽` or `epic` selects epic.
   `스토리` or `story` selects story. Otherwise select task. When the request
   names more than one type, use the type it assigns to this issue. If that is
   still ambiguous, ask which single type to write.
4. Begin with `Mode: new | rewrite | Type: task | story | bug | epic | Target: <key or paste>`
   and nothing before it.

## Task and story

Same sections, in this order. Set the Jira issue type to Task or Story.
Story `개요` starts with who can do what. Task `개요` starts with which module
changes and why now.

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

- `개요` is 3–6 bullets, noun-ending Korean (`…함`, `…음`). After the opening
  bullet: how in one line, what differs from the plan or current code, what is
  out of scope. Mention the ticket it was split from or merged into.
- One settled decision is one bullet. One open decision is one bullet that names
  the options and the preferred one with its deciding reason.
- `작업 내용` has 5–9 checkboxes, one concern each, in build order. No `S1/S2`
  prefixes, no path lists; at most one path or identifier per item.
- `테스트 확인` lists observable outcomes (`…한다`, `…이 나온다`). Put the
  project's standard check command last when sibling issues do.
- `영향 범위` names repositories and modules in words, not trees.
- Do not create the child tasks of a story in the same turn.

## Bug

Set the Jira issue type to Bug.

```markdown
## 현상
* …

## 기대 / 실제
* **기대**: …
* **실제**: …

## 재현·근거
* …

## 수정 범위 (Checkbox)
- [ ] …

## 확인 (Checkbox)
- [ ] …

## 참고
* 관련 이슈: [KEY 제목](url)(관계 한 구절)
* 문서/링크: 경로 + 절
```

- `현상` states where it breaks and what breaks, using discussed facts only.
- `기대` and `실제` are one line each.
- `재현·근거` repeats only steps or evidence already given. Use `-` when none
  was given.
- `수정 범위` has 3–6 checkboxes, one concern each.
- `확인` lists observable outcomes after the fix.

## Epic

Set the Jira issue type to Epic. No implementation checklist.

```markdown
## 결과
* …

## 범위
* **안**: …
* **밖**: …

## 자식
* 이후 자식은 이 에픽을 부모로 연결하고, 이 목록에는 추가하지 않음
* [KEY 제목](url)(관계 한 구절)

## 참고
* 문서/링크: 경로 + 절
```

- `결과` is 2–4 bullets and includes an observable done-when.
- The first `자식` bullet is fixed. Keep it when rewriting. Further bullets are
  only starting issues that already exist at first write. Omit them when there
  are none. Do not append keys to this list later.
- Do not create child issues in the same turn.

## Shared writing rules

- If a sentence took analysis to reach, keep the conclusion and drop the path
  to it. Never paste chat history, option matrices, or code.
- Match the voice of sibling issues over this file when they differ.
- Target under 60 rendered lines.
- Never leave a template section out; use `-` when it is empty.

## Writing to Jira

- When the issue being created names an existing epic, set its parent to that
  epic and leave the epic description unchanged.
- With an Atlassian tool and an explicit request to write, create or edit the
  one issue with `contentFormat: html` and the chosen issue type. Checkboxes
  must be
  `<ul data-type="task-list"><li data-type="task-item"><input type="checkbox"> …</li></ul>`;
  markdown `- [ ]` is stored as literal text.
- Re-read the issue after saving and fix mojibake or typos in the same turn.
- Without a tool, output the markdown ready to paste.
- Renaming or rewriting another person's issue: do it only when asked, and say
  so in the reply.

## Prohibited

- Never change code, tests, configuration, or documents other than the card.
- Never invent scope, dates, owners, estimates, reproduction steps, or child
  issues that were not discussed.
- Never create a second issue in the same turn.

## Completion

Report the issue key or that the text is ready to paste, the type written, and
the decisions the card leaves open.
