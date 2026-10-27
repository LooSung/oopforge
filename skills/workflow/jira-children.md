---
name: workflow-jira-children
description: Write the child tasks of one existing Jira epic or story. Each title carries one track tag. A track this repository does not implement says how the other repository does the work.
tags: [workflow, planning, jira]
stability: experimental
---

# Workflow — Jira Children

## Purpose

Turn one existing epic or story into its child tasks. Each title is `[F.E]`,
`[B.E]`, `[AI]`, or `[DOC]`. A child this repository implements lists work here. A child
another repository implements says how that repository does the work and how it
connects. The parent body stays as it is.

## Startup

1. Parent: an epic or story key or URL is required. Read its title, body, and
   existing children first. A bug or task is not a parent here; say so and stop.
2. Read only what a child must point to: the parent, one sibling child for
   voice, and the few code files a child names.
3. Home is the track this repository implements. Use the track the request
   gives this repo. If it is missing, ask once. Do not infer home from
   OOPforge or Compforge.
4. Choose tracks only from the parent and this request. `[F.E]` is a screen or
   client behavior. `[B.E]` is an API, module, or persistence behavior. `[AI]`
   is a model, prompt, retrieval, or eval behavior. `[DOC]` is a document or
   report whose done-when is that document. A note or link that supports
   another track stays on that track's card. One slice with no track is one
   question, asked once, before any child is written.
5. One named slice is one child. When no slices are named, write one child per
   track the parent needs, including a track another repository implements
   when the parent connects to it. Skip a child that already matches the same
   parent, track, and slice. Cap is 6; if the split needs more, ask which six
   before writing any.
6. Begin with
   `Mode: children | Parent: <key> (epic|story) | Home: F.E|B.E|AI|DOC | Tracks: F.E, B.E | Count: <n>`
   and nothing before it.

## Child

Set the Jira issue type to Task. Set the parent and leave that issue's
description unchanged. Title shape is `[F.E] …`, `[B.E] …`, `[AI] …`, or `[DOC] …`: one
tag, one space, then the slice. The tag is the whole title distinction. A
story under an epic is still one story card in `workflow/jira-card.md`. If the
site rejects a Task under a story, create a Sub-task with the same title and
body.

```markdown
## 개요
* 부모 [KEY 제목](url)의 F.E 몫임
* 구현 저장소: …
* …

## 작업 내용 (Checkbox)
- [ ] …

## 영향 범위
* **구현 저장소**: 이 저장소 / 프론트 / 백엔드 / AI / 문서
* **대상**: …
* **계약 변경**: 있음 / 없음 (한 줄 이유)
* **데이터 변경**: 있음 / 없음 (한 줄 이유)

## 테스트 확인 (Checkbox)
- [ ] …

## 참고
* 부모: [KEY 제목](url)
* 문서/링크: 경로 + 절
```

- `개요` is 3–5 bullets, noun-ending Korean (`…함`, `…음`). The first bullet
  names the parent and the track. The second names where it is implemented.
- Home child: the track matches this repository. Second bullet: `이 저장소에서
  구현함`. `작업 내용` is work in this repository, 3–6 checkboxes, one concern
  each, in build order. F.E considers the visible result, where state lives,
  and empty/error/loading when the slice has them. B.E considers the use case,
  the boundary, and persistence when data changes. AI considers input and
  output, failure behavior, and the check that shows it worked. DOC considers
  the reader, the claims, and the sources.
- Foreign child: another repository implements this track. Second bullet names
  that repository and says this repository does not implement the track.
  Home AI and child F.E: `구현은 프론트 저장소임. 이 저장소는 AI라 화면을
  만들지 않음.` `작업 내용` is how that repository does the work, 3–6
  checkboxes. Include the connection the parent already settled: what this
  repository exposes, and what the other side calls or shows. Include how that
  side behaves when the connection fails.
- When the connection is still an open choice, one `개요` bullet names the
  options and the preferred one. Do not invent an endpoint, event, or payload.
- `영향 범위` always names `구현 저장소`, then uses the track's meaning. F.E:
  대상 is the screen or component, 계약 is the API dependency, 데이터 is client
  storage. B.E: 대상 is the service or module, 계약 is the API, 데이터 is the
  DB. AI: 대상 is the prompt, retrieval, or eval, 계약 is the model
  input/output, 데이터 is the corpus or index. DOC: 대상 is the document
  or report, 계약 is the facts it must carry, 데이터 is the source it cites.
- `테스트 확인` has 2–4 observable outcomes (`…한다`, `…이 나온다`). A foreign
  child's outcomes are what a reviewer sees in the other repository.
- `참고` always links the parent. Use `-` for an empty doc line.
- Order children F.E, then B.E, then AI, then DOC. Extra slices of a track stay together
  in the order the parent names them.

## Shared writing rules

- If a sentence took analysis to reach, keep the conclusion and drop the path
  to it. Never paste chat history, option matrices, or code.
- Match the voice of sibling children over this file when they differ.
- Target under 40 rendered lines per child.
- Never leave a template section out; use `-` when it is empty.

## Writing to Jira

- With an Atlassian tool and an explicit request to write, create each child
  with `contentFormat: html` and the chosen issue type. Checkboxes must be
  `<ul data-type="task-list"><li data-type="task-item"><input type="checkbox"> …</li></ul>`;
  markdown `- [ ]` is stored as literal text.
- Re-read each issue after saving and fix mojibake or typos in the same turn.
- Without a tool, output each title and its markdown, ready to paste.
- Creating under another person's parent: do it only when asked, and say so
  in the reply.

## Prohibited

- Never change code, tests, configuration, or documents other than the children.
- Never edit the parent.
- Never put this repository's implementation steps on a foreign child, or the
  other repository's steps on the home child.
- Never invent a track, slice, owner, date, estimate, or scope that the parent
  and this request did not already contain.
- Never create a child of a bug or task in this mode.
- Never exceed 6 children, and never write a second parent's children in the
  same turn.

## Completion

Report each title, whether it is home or foreign, and the key or that the text
is ready to paste. Name tracks or slices skipped because they were unclear or
already present, and the decisions the children leave open.
