# OOPforge — Roadmap

OOPforge가 지향하는 방향과 우선순위. **미래 지향** 문서다 — 완료된 변경의 상세 이력은 [`CHANGELOG.md`](../CHANGELOG.md)에 있다.

이 로드맵은 **시간축(단기/중기/장기)을 넘어** "우리가 진짜로 무엇이며, 무엇을 깊게 파고들 것인가"를 먼저 고정한다. 백엔드 OOP/DDD에 **수직 특화**된 정체성을 지키는 것이 모든 우선순위보다 앞선다.

---

## 0. 비전 (정체성 — 흔들지 않음)

> **OOPforge는 백엔드 OOP/DDD에 특화된 Spec-Driven 방법론 + 아키텍처 강제(fitness function) 팩이다.**

- 우리는 **수직(vertical) 방법론**이다. 범용 코딩 에이전트(oh-my-pi)·코드 인덱서(codegraph)·컨텍스트 압축기(headroom) 같은 **수평(horizontal) 인프라**가 아니다.
- 대상은 **Java(Spring) / Python(FastAPI) 백엔드**와 **OOP/DDD를 제대로 하려는 팀**. 그 좁은 영역에서 **가장 깊다**.
- 상위 트렌드인 **Spec-Driven Development(SDD)** 생태계(Spec Kit, Kiro, OpenSpec, BMAD 등) 안에서, OOPforge는 "도메인 모델/레이어 경계/전술적 DDD"에 특화된 변종이다. 범용 SDD가 다루지 않는 **백엔드 전술 패턴**을 책임진다.

### 우리가 푸는 진짜 문제 (측정 가능)

AI 에이전트는 제약이 없으면 백엔드 아키텍처를 무너뜨린다 — 업계 관측상 **제약 없는 세션의 다수가 레이어/도메인 경계를 위반**하고, 명시적 제약(constitution + skills + fitness function)을 주면 위반이 **거의 0으로** 떨어진다. OOPforge의 효과 지표는 토큰 절감이 아니라 **아키텍처 위반율**과 **재작업률**이다.

### 우리의 증거 방식 (벤치마크 ≠ 토큰)

수평 도구는 "토큰 X% 절감"이라는 보편 숫자로 증명한다. 우리는 못 이기는 게임이고, 할 필요도 없다. OOPforge의 증거는:

1. **정성적 Before/After** — 같은 요구사항을 무개입(vibe coding) vs OOPforge로 만든 결과 diff.
2. **runnable 예제** — 같은 도메인을 layered/hexagonal/CQRS로 (이미 보유).
3. **약한 정량** — archlint 위반 수, 도메인 테스트 커버리지, 재작업 횟수 (유/무 비교).

---

## 핵심 원칙 (유지)

이미 잘하고 있는 것은 손대지 않는다. 이 원칙이 OOPforge의 정체성이며, 변경할 때는 매우 신중히 한다.

- 작은 스킬 (200줄/스킬, 한 스킬 한 개념)
- 측정 가능한 하드 룰 (300줄/파일, 20줄/메서드)
- 단계별 휴먼 체크포인트 (Discovery → Design → … → Test)
- 도메인 우선, 프레임워크는 어댑터로
- **토큰/비용 절감을 핵심 지표로 삼지 않는다** — 우리는 압축 도구가 아니다
- **범용 에이전트와 경쟁하지 않는다** — 그 위에 얹히는 방법론이다

---

## 발전 축 (시간축보다 먼저)

성장은 "넓히기"가 아니라 세 축을 깊게 파는 것이다. 각 항목에 시간 태그(`[단기]` 다음 릴리스 · `[중기]` 분기 · `[장기]` 연간)를 단다.

```
축 A. 백엔드 깊이   — 전술적 DDD·프로덕션 준비. 우리만의 해자.
축 B. 마찰 제거     — MCP·스펙 정렬·진입 가이드. 채택 장벽 ↓.
축 C. 강제 & 증명   — fitness function·리뷰 자동화·학습 루프·정성 proof.
```

---

## 축 A — 백엔드 깊이 (우리만의 해자)

범용 SDD/룰팩이 못 가르치는 **전술적 DDD 패턴**과 **프로덕션 준비**. 여기가 OOPforge가 대체 불가능해지는 지점이다.

### A1. 전술적 DDD 스킬 확장 `skills/oop/` `[단기~중기]`

현재 `domain-model`·`use-case-boundary`·`cqrs`·**`transaction-boundary`(v0.9.2)** 보유. 이어서:

- ~~`transaction-boundary.md`~~ ✅ v0.9.2 — **하나의 트랜잭션에 하나의 Aggregate**. 다중 Aggregate 수정은 결과적 일관성 신호.
- `transactional-outbox.md` `[단기]` — DB 쓰기와 이벤트 발행을 **같은 트랜잭션**에. relay/CDC로 브로커 전달. ghost/lost 이벤트 방지.
- `saga.md` `[중기]` — Aggregate/서비스를 가로지르는 프로세스, **보상 트랜잭션**. choreography(단순) vs orchestration(복잡).
- `domain-events.md` `[중기]` — 내부 도메인 이벤트 vs 통합(integration) 이벤트, **idempotent consumer**, 이벤트 스키마 **버저닝/upcaster**.
- (event sourcing은 CQRS와 묶어 별도 advisory로 — 남발 경계)

### A2. 안티패턴 카탈로그 확장 `skills/antipatterns/` `[단기]`

~~핵심 4종 + flat-package~~ ✅ v0.9.2 (`anemic-domain`, `controller-fat`, `repository-with-business-logic`, `god-aggregate`, `flat-package`). 추가 후보:

- (수요 시) `god-service.md` — application service에 모든 유스케이스·규칙 집중
- Craft 리뷰·CI가 참조할 메시지 템플릿 보강 `[중기]`

### A3. 프로덕션 준비 게이트 `[중기]`

"80% 문제" — 에이전트는 기능은 만들지만 **비기능 요구(NFR)를 체계적으로 빼먹는다**. Implement 후 명시적 체크 단계:

- `skills/workflow/production-readiness.md` — 입력 검증, 에러 응답 스키마 단일화(`ErrorResponse`), 멱등성, 재시도/백오프, 관측성(로그/트레이스 훅), 감사 로그, PII/시크릿 취급, 레이트리밋 자리.
- 도메인 순수성을 깨지 않으면서 **어댑터 레이어에서** 충족하도록 가이드.

### A4. 점진적 채택 & 레거시 진입 `[단기~중기]`

- `skills/workflow/adopt-legacy.md` `[단기]` — 기존 레거시에 작은 bounded context 1개부터 끼워넣는 절차. "전체를 다 바꾸지 말 것".
- 진입 기준 체크리스트 `[중기]` — layered → 헥사고날/clean → CQRS (어댑터 수·도메인 수·팀 크기 기준).
- `skills/workflow/migrate-layered-to-hexagonal.md` `[중기]` — 마이그레이션 스킬.

---

## 축 B — 마찰 제거 (채택 장벽 ↓)

수평 도구가 이긴 진짜 이유는 "한 줄 설치 → 즉시 작동". OOPforge는 symlink + 재시작이라 무겁다.

### B1. MCP 서버 모드 `[중기]`

- `oopforge serve --mcp` — 스킬/룰/안티패턴을 MCP `initialize` 응답으로 에이전트에 주입, 룰 위반 시 **실시간 피드백**. (codegraph/headroom처럼 instructions 파일 없이 동작)
- Phase 2/3(marketplace/CLI)와 **별개의 배포 채널**로 격상. 단 비-목표("불안정 통합 default 금지") 준수 — **opt-in 실험**으로 시작.

### B2. Agent Skills 스펙 정렬 `[단기]`

- 업계 `SKILL.md` 표준(frontmatter `name`/`description`, **progressive disclosure**, 본문 권장 한도)에 맞춰 스킬 메타데이터 정비 → Claude/Codex/Cursor 외 에이전트 호환성 확보.
- OOPforge의 200줄 룰은 이미 progressive disclosure에 부합 → 유지하며 frontmatter만 표준화.

### B3. 레포 위생 마무리 `[단기]`

- `skills/` 내부 죽은·중복 내용, 끊긴 상호 링크 점검.
- 빌드 산출물·캐시 ignore 정비(`__pycache__`, `*.egg-info`, gradle 산출물 등).
- 문서 간 링크 무결성 CI 검사(끊긴 상대경로 차단).

---

## 축 C — 강제 & 증명 (fitness function + proof)

"AGENTS.md만으론 부족"이 업계 합의다. 룰은 **CI에서 빌드를 깨야** 하고, 실패는 **에이전트 자가교정 루프**로 돌아가야 한다.

### C1. fitness function 확장 `[중기]`

- 헥사고날 예제용 import-linter/ArchUnit 변종 (현재 layered만 표준 도구 강제).
- archlint에 축 A 패턴 검사 추가: outbox(쓰기+발행 동일 트랜잭션), saga 경계, 다중 Aggregate 트랜잭션 탐지.
- (수요 시) 타깃 프로젝트 부트스트랩 — `--with-lint`, `--with-openapi`. install.sh와 분리된 별도 스크립트.

### C2. 도메인 리뷰 자동화 `[단기로 상향]`

수직 도구의 진짜 무기. 가치 전달 + 구조적 증명을 동시에.

- Craft 기반 PR diff 리뷰가 안티패턴/하드룰 위반을 자동 코멘트.
- GitHub Action 템플릿 제공. 위반 메시지를 에이전트에 피드백해 자가교정 유도.

### C3. 학습 루프 `[중기]`

- 리뷰에서 반복 잡히는 위반 → 프로젝트 `AGENTS.md`/`.craft/`에 교정 규칙으로 **누적**.
- "이 팀은 자꾸 anemic domain을 만든다" → 다음 세션 첫 턴에 경고. (continuity 자산 확장)

### C4. 정성적 Proof 자산 `[단기로 상향]`

- **무개입 vs OOPforge** 결과를 나란히 보여주는 before/after diff 문서.
- README 상단 30초 install + Craft 실행 흐름 GIF/asciinema (현재 0개라 임팩트 큼).
- 위반율/재작업 약한 정량 표 (토큰 아님).

### C5. OpenAPI 기본 탑재 완성 `[중기]`

- 모든 백엔드 스켈레톤이 Swagger UI 기본 ON (현재 Java layered만 springdoc).
- 에러 응답 스키마(`ErrorResponse`) 단일화 — A3 프로덕션 게이트와 연결.

---

## 포지셔닝 (정체성 명문화) `[단기]`

가장 싸고 효과 큰 작업. README + `docs/positioning.md`에 **경쟁 비교표**. 단 경쟁자는 codegraph/headroom이 아니라:

| 비교 대상 | OOPforge가 다른 점 |
|---|---|
| 그냥 `AGENTS.md`에 "DDD 지켜" 한 줄 | constitution은 필요하지만 불충분. 우리는 skills + **CI fitness function** + 휴먼 체크포인트까지 |
| 범용 스킬팩(superpowers 등) | 백엔드 OOP/DDD **전술 패턴**에 특화 (outbox/saga/aggregate 경계) |
| 범용 SDD(Spec Kit/Kiro) | SDD 워크플로 위에 **도메인 모델링·레이어 강제**를 얹은 백엔드 변종 |
| 무개입 vibe coding | God Service·anemic domain을 **구조적으로 차단** |

"우리는 무엇이 아닌가"(프론트·ML·범용 에이전트 X)를 **README 첫 화면**으로 승격.

---

## 최근 완료 (요약)

상세는 [`CHANGELOG.md`](../CHANGELOG.md) 참조. 현재 최신: **v0.9.2**.

- **안티패턴 카탈로그 + 트랜잭션 경계 (v0.9.2)** — `anemic-domain`·`controller-fat`·`repository-with-business-logic`·`god-aggregate` 추가. `transaction-boundary.md`(한 TX = 한 Aggregate). Craft/Hard Rules/reviewer checklist 연결. 로드맵 A1·A2 단기 항목 진척.
- **에이전트 행동 가드레일 (v0.9.1)** — `oop-discipline` #10 Assumptions / #11 Surgical changes. Craft에 Assumptions 게이트·Scope drift, playbook `verify:`, Hard Rules에 외과수술식 수정. Karpathy식 실패 패턴을 통째 복제하지 않고 Craft 레이어에만 흡수.
- **스킬 영어 정본화 (v0.9.0)** — 모든 `skills/`를 영어로 번역(에이전트 지시문은 영어가 정본). 한국어는 개념 가이드 `docs/methodology.ko.md` 1개로 흡수. 로드맵 B2(Agent Skills 스펙 정렬)·B3(레포 위생) 진척.
- **DRY-with-DDD (v0.8.5)** — `oop-discipline` #9로 DRY를 추가하되 Rule of Three + 바운디드 컨텍스트 경계 가드레일로 한정. 원칙 감사 결과 유일한 빈칸을 메움.
- **과설계 방지 사다리 (v0.8.4)** — `oop-discipline` #7을 작성 직전 번호 사다리로 강화(본질 vs 우발 복잡성 구분, 안전 항목 비협상, 미룬 것은 upgrade path 표식). `implement.md` 발화 지점에 연결. ponytail의 YAGNI 사다리를 백엔드 OOP/DDD 맥락으로 차용하되 도메인 구조는 면제.
- **레포 군살 제거 (v0.8.3)** — `docs/sample-output/` 전체와 JA/ZH 문서(~20개) 제거. 문서를 **영어(정본) + 한국어**로 축소하고 정책 명문화.
- **runnable 예제 패밀리** — `calculator` 한 도메인을 java/python × layered/hexagonal/hexagonal-cqrs 6종으로 통일.
- **아키텍처 강제 (2겹)** — stdlib `archlint.py`(레이어 + CQRS) + 표준 도구(import-linter, ArchUnit)를 `arch-lint.yml`에서 PR 차단.
- **Craft 진입점 정착** — `/oopforge:craft` 단일 진입점. 스택 범위 게이트(Java Spring / Python FastAPI).
- **Continuity 자동화** — 실행 작업이면 `.craft/` 자동 생성(opt-out).
- **스킬 추가** — CQRS, 안티패턴 시작(`flat-package`), 린트 강제 가이드(`lint-enforcement`).

---

## 비-목표 (의도적으로 안 함)

- **수평 인프라화** — 범용 에이전트·코드 인덱서·컨텍스트 압축기와 경쟁하지 않음
- **토큰/비용 벤치마크 경쟁** — 우리 지표는 위반율·재작업률
- **메가 스킬/메가 프롬프트** — 한 파일에 여러 개념 묶지 않음
- **GUI/IDE 플러그인** — CLI/에이전트 통합으로 충분
- **자동 코드 생성기** — 패턴은 가르치고, 코드는 에이전트가 작성
- **모든 패턴/도메인 커버** — DDD 핵심 + 백엔드 OOP에 집중. UI/모바일/ML 진출 X
- **불안정한 통합을 default install에 포함** — 실험적 통합(MCP 등)은 별도 opt-in

---

## 언어 확장 `[장기]` — 넓히되 신중

수직 정체성을 지키는 선에서만. 각 언어는 layered + hexagonal 두 변종 + runnable 예제 필수(예제 품질을 희생하면 정체성 훼손).

1. **Kotlin Spring** — OOP/DDD 친화도 매우 높음, Java 코드 거의 재활용
2. **TypeScript NestJS** — 데코레이터·DI가 Spring과 유사, Node 생태계 커버
3. **Go** — 구조체 기반이지만 인터페이스로 헥사고날 가능. 별도 가이드 필요
4. **C# .NET** — 엔터프라이즈 수요, MediatR과 자연스럽게 결합

---

## 패키징 단계 (배포)

- **Phase 1** — symlink 기반 경량 포터블 팩 (현재)
- **Phase 2** — Claude Code / Codex / Cursor 플러그인 마켓플레이스 + **MCP 서버 모드(축 B1)**
- **Phase 3** — Claude Agent SDK 기반 독립 CLI

---

## 기여 우선순위

새 컨트리뷰터 추천 순서(작은 단위부터):

1. 안티패턴 카탈로그 1개 추가 (축 A2)
2. 전술 DDD 스킬 1개 추가 (축 A1 — outbox/saga 등)
3. 기존 스킬에 "변형" 섹션 보강
4. 신규 언어 layered 레이아웃 + 예제 추가 (장기)
5. 린트 템플릿/변종 추가 (축 C1)
6. 레거시 진입 가이드 케이스 스터디 추가 (축 A4)
