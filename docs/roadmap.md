# OOPforge — Roadmap

**미래 지향** 문서다. 완료된 변경의 상세 이력은 [`CHANGELOG.md`](../CHANGELOG.md)에 있다. 여기에는 **"이건 반드시 한다"**만 남긴다 — 하고 싶은 것이 아니라 정체성을 지키며 성장하는 데 꼭 필요한 것.

---

## 0. 비전 (정체성 — 흔들지 않음)

> **OOPforge는 백엔드 OOP/DDD에 특화된 Spec-Driven 방법론 + 아키텍처 강제(fitness function) 팩이다.**

- 우리는 **수직(vertical) 방법론**이다. 범용 코딩 에이전트·코드 인덱서·컨텍스트 압축기 같은 **수평(horizontal) 인프라**가 아니다.
- 대상은 **Java(Spring) / Python(FastAPI) 백엔드**와 **OOP/DDD를 제대로 하려는 팀**. 그 좁은 영역에서 **가장 깊다**.
- Spec-Driven Development(SDD) 생태계 안에서, OOPforge는 "도메인 모델/레이어 경계/전술적 DDD"에 특화된 변종이다.
- **효과 지표는 토큰 절감이 아니라 아키텍처 위반율과 재작업률이다.** 명시적 제약(constitution + skills + fitness function)이 이 지표를 실제로 낮추는지 재현 가능한 대조 실험으로 검증한다.

---

## 핵심 원칙 (유지 — 손대지 않는다)

- 작은 스킬 (200줄/스킬, 한 스킬 한 개념)
- 측정 가능한 하드 룰 (300줄/파일, 20줄/메서드)
- 단계별 휴먼 체크포인트 (Discovery → Design → … → Test)
- 도메인 우선, 프레임워크는 어댑터로
- 토큰/비용을 핵심 지표로 삼지 않는다
- **범용 에이전트와 경쟁하지 않는다** — 그 위에 얹히는 방법론이다

---

## 반드시 할 것

성장은 "넓히기"가 아니라 세 축을 깊게 파는 것이다. 각 항목에 시간 태그(`[단기]` 다음 릴리스 · `[중기]` 분기).

```
축 A. 백엔드 깊이   — 전술적 DDD. 우리만의 해자.
축 B. 마찰 제거     — MCP·스펙 정렬. 채택 장벽 ↓.
축 C. 강제 & 증명   — fitness function·리뷰 자동화·정성 proof.
```

### 축 A — 백엔드 깊이 (해자)

- `[단기]` `skills/oop/transactional-outbox.md` — DB 쓰기와 이벤트 발행을 **같은 트랜잭션**에. relay/CDC로 브로커 전달. ghost/lost 이벤트 방지.
- `[중기]` `skills/oop/saga.md` — Aggregate/서비스를 가로지르는 프로세스 + **보상 트랜잭션** (choreography vs orchestration).
- `[중기]` `skills/oop/domain-events.md` — 내부 vs 통합 이벤트, **idempotent consumer**, 이벤트 스키마 버저닝/upcaster.
- `[중기]` `skills/workflow/production-readiness.md` — Implement 후 NFR 게이트: 입력 검증, `ErrorResponse` 단일화, 멱등성, 재시도/백오프, 관측성, 감사 로그, PII/시크릿. **도메인 순수성을 깨지 않고 어댑터 레이어에서** 충족.

### 축 B — 마찰 제거 (채택 장벽 ↓)

- `[단기]` **B2. Agent Skills 스펙 정렬** — `SKILL.md` frontmatter(`name`/`description`) + progressive disclosure 표준화 → Claude/Codex/Cursor 외 에이전트 호환.
- `[단기]` **B3. 레포 위생** — 죽은/중복 스킬·끊긴 링크 정리, 빌드 산출물 ignore, 문서 링크 무결성 CI.
- `[중기]` **B1. MCP 서버 모드** — `oopforge serve --mcp`. archlint·안티패턴 탐지·도메인 리뷰를 **MCP 툴로 노출**해 에이전트가 코딩 중 위반을 **실시간 피드백**받고 자가교정. 스킬을 나르는 게 아니라 **강제(enforcement)가 핵심** — 코드 인덱서/메모리 인프라를 흉내 내지 않는다. instructions 파일·재시작 없이 작동, **opt-in 실험**으로 시작. (멀티에이전트 환경에서 각 에이전트에 규율을 얹는 우리다운 방법 — 오케스트레이터가 되는 것과 다름)

### 축 C — 강제 & 증명

- `[단기]` **C2. 도메인 리뷰 자동화** — ✅ MVP 완료(상세 이력 CHANGELOG): PR diff에서 **신규 하드룰 위반만** read-only로 코멘트(+machine JSON), GitHub Action, OOPforge 레포 dogfood로 검증. **남은 범위**: 안티패턴·메서드 길이 detector, archlint layered/CQRS 재사용, 타깃 프로젝트용 Action 템플릿 배포, 위반 피드백 기반 **자가교정** 루프. (수직 도구의 진짜 무기)
- `[단기]` **C4. 반복 Proof + 데모** — 고정 프로토콜로 무개입 vs OOPforge 짝 실험을 반복하고, 유리·중립·불리한 결과를 모두 공개. README에 Craft 실행 GIF/asciinema와 위반율·재작업 요약을 연결하되 단일 실행을 개선율로 일반화하지 않는다.
- `[중기]` **C1. fitness function 확장** — 헥사고날용 import-linter/ArchUnit, archlint에 축 A 패턴 검사 추가(outbox 트랜잭션, saga 경계, 다중 Aggregate 탐지).

---

## 다음 릴리스 우선순위 (단기)

| 우선 | 항목 |
|---|---|
| C4 | 반복 before/after proof 공개 + README Craft 데모 |
| C2+ | 도메인 리뷰 탐지기 확장(안티패턴·메서드 길이·archlint 재사용) + 타깃 프로젝트 템플릿 (MVP는 완료) |
| A1 | `transactional-outbox.md` |
| B2 | `SKILL.md` frontmatter 표준화 |
| B3 | 레포 위생 |

---

## 비-목표 (의도적으로 안 함 — 가드레일)

- **수평 인프라화** — 범용 에이전트·코드 인덱서·컨텍스트 압축기와 경쟁하지 않음
- **멀티에이전트 오케스트레이션** — worktree 격리·세션 관리·에이전트 간 통신은 우리 몫이 아니다. 우리는 **각 에이전트가 따르는 설계 규율**이지 오케스트레이터가 아니다
- **토큰/비용 벤치마크 경쟁** — 지표는 위반율·재작업률
- **메가 스킬/메가 프롬프트** — 한 파일에 여러 개념 X
- **GUI/IDE 플러그인** — CLI/에이전트 통합으로 충분
- **자동 코드 생성기** — 패턴은 가르치고, 코드는 에이전트가 작성
- **UI/모바일/ML 진출** — DDD 핵심 + 백엔드 OOP에 집중
- **불안정한 통합을 default install에 포함** — 실험(MCP 등)은 별도 opt-in

---

## 장기

### 언어 확장 선행 조건 (이 순서로 끝낸 뒤에 확장)

언어 확장은 "**검증되고 강제되는 수직**"을 복제하는 일이다. 원본(Java/Python)이 증명·강제·정리되기 전에 언어를 늘리면 미검증·미강제 방법론을 N배로 곱해 유지보수·드리프트만 폭증한다. 아래를 순서대로 끝낸 뒤 확장한다.

1. **C4 — 반복 proof 공개** — 한 스택에서 위반율·재작업률이 실제로 낮아진다는 재현 가능한 증거 확보. 증거 없이 확장하면 근거 없는 주장을 4배 복제하는 것. **1번 게이트.**
2. **B3 — 레포 위생 + 문서 링크 무결성 CI** — 확장 = 문서·예제 N배 = 드리프트 표면 N배. 확장 전에 정리하고 링크 무결성 CI를 걸어 승수를 줄인다.
3. **C1 — fitness function 확장(헥사고날 import-linter/ArchUnit + archlint 패턴) + C2+ 탐지기 확장** — 새 언어마다 "layered + hexagonal + runnable"을 요구하므로, 헥사고날까지 **강제 템플릿**을 성숙시켜 "예제만 있는 확장"이 아니라 "강제·증명이 딸려오는 확장"이 되게 한다.
4. **B2 — SKILL.md frontmatter 표준화** — 팩 표면이 커질수록 커지는 이식성 이득. 저비용, 확장 전에 끊어둔다.

축 A(outbox/saga/domain-events/production-readiness)는 현재 스택의 **깊이(콘텐츠)**로, 패턴이 언어 중립이라 확장의 게이트는 아니다(해자 강화 차원에서 병행 가능).

### 확장 대상

- **언어 확장** (수직 정체성 유지 선에서만, 각 언어 layered + hexagonal + runnable 예제 필수): Kotlin Spring → TypeScript NestJS → Go → C# .NET
- **패키징**: Phase 1 symlink 팩(현재) → Phase 2 플러그인 마켓플레이스 + MCP 서버 모드 → Phase 3 Claude Agent SDK 기반 독립 CLI
