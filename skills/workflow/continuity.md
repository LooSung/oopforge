---
name: workflow-continuity
description: 작업 맥락을 단일 문서로 저장하고 다음 세션에서 먼저 읽어 이어가는 OOPforge 연속성 규칙. 실행 작업은 기본 자동 생성(opt-out).
tags: [workflow, memory, continuity]
stability: experimental
---

# Workflow — Continuity

## 목적

대화가 끊겨도 작업을 이어갈 수 있게 한다.
작업마다 단일 Markdown 문서를 만들어 결정·진행·다음 할 일을 누적하고,
다음 세션은 그 문서를 **먼저 읽어** 맥락을 복원한다.

## 작업 위치

- 기본값: 대상 프로젝트 루트의 `.craft/`.
- 오버라이드: 대상 프로젝트 `AGENTS.md`에 `OOPforge work dir: <path>` 한 줄이 있으면 그 경로를 우선한다.
- 끄기(opt-out): 대상 프로젝트 `AGENTS.md`에 `OOPforge continuity: off` 한 줄이 있으면 생성하지 않는다.
- 작업당 문서 하나: `<work dir>/<kind>-<slug>.md`.
  - `kind`는 `feature`, `refactor`, `bugfix` 중 하나.
  - `slug`는 kebab-case. 같은 작업이 항상 같은 파일로 복원되도록 결정론적으로 짓는다.
  - 예: `.craft/feature-member-management.md`, `.craft/refactor-order-service.md`.

## Resume 프로토콜 (작업 시작 시)

1. work dir이 있으면 목록을 확인한다.
2. 현재 요청과 관련된 문서가 있으면 **그 문서를 먼저 읽고** 이어간다.
3. 관련 문서가 없으면 아래 **첫 세션 (자동 생성)** 을 따른다.
4. 사용자가 특정 문서를 지목하면 그 문서를 따른다.

## 첫 세션 (자동 생성, opt-out)

관련 작업 문서가 없을 때, **작업 종류로 생성 여부를 결정론적으로 판단한다.** 묻지 않는다.

| 작업 분류 | 동작 |
|---|---|
| `feature` / `refactor` / `bugfix` (실행 작업) | **자동 생성** 후 한 줄 고지 |
| advisory · 추천만 · 단일 Value Object 등 초소형 | 생성하지 않음 |
| `AGENTS.md`에 `OOPforge continuity: off` | 생성하지 않음 |

자동 생성 시 한 줄 고지:

> 이 작업을 `.craft/<kind>-<slug>.md`에 기록합니다. (끄려면 `AGENTS.md`에 `OOPforge continuity: off`)

생성 절차:

1. work dir과 작업 문서를 만든다.
2. 대상 프로젝트 `.gitignore`에 `.craft/`가 없으면 추가한다 (개인 작업 노트, 커밋하지 않음).
3. 오버라이드 경로를 쓰면 그 경로를 `.gitignore` 대상으로 한다.

## 작업 문서 포맷

작업당 이 한 장에 모든 것을 누적한다.

```markdown
# <Title> — <kind>

## Status
- Stage: <discovery|design|skeleton|implement|test|refactor|done>
- Updated: <date>
- Next: <한 줄로 다음 할 일>

## Context / Goal
- 무엇을, 왜.

## Decisions (append-only)
- [<date>] <결정> — <이유>

## Progress
- [x] 끝난 일
- [ ] 남은 일

## Open Questions / Risks
- 모르는 것, 위험.

## Links
- commit / PR / 관련 코드 경로
```

## 갱신 규칙

- 의미 있는 결정이 나오면 `Decisions`에 **append**한다 (기존 줄을 지우지 않는다).
- 작업 단위가 끝나면 `Status`와 `Progress`를 갱신한다.
- Craft 완료 보고(Design Decisions, Verification, Remaining Risks)는 이 문서에 반영한다.
- **완료 게이트**: 문서가 존재하는 작업은 이 문서를 갱신하기 전에는 done 보고를 하지 않는다.

## 큰 작업

- 새 도메인이나 큰 기능은 단계별 산출물(`discovery.md`, `design.md` 등)을 work dir 옆에 둘 수 있다.
- 그 경우에도 `<kind>-<slug>.md`가 단일 진입점(앵커)으로 남아 단계 문서를 링크한다.

## 금지

- **advisory·초소형 작업에 `.craft/` 생성 금지** — 실행 작업(feature/refactor/bugfix)만 자동 생성.
- **`OOPforge continuity: off`면 생성 금지** — 사용자 opt-out을 존중한다.
- **결정 로그 덮어쓰기 금지** — append만 한다.
- **민감 정보 기록 금지** — 비밀키, 토큰, 개인정보를 문서에 남기지 않는다.
- **결과 보고서로 쓰기 금지** — 진행 중 맥락과 다음 할 일을 적는다.
- **work dir 커밋 강요 금지** — 기본은 gitignore. 팀 공유가 필요하면 사용자가 결정한다.
