# OOPforge — Roadmap

**미래 지향** 문서다. 완료된 변경의 상세 이력은 [`CHANGELOG.md`](../CHANGELOG.md)에 있다. 여기에는 **"이건 반드시 한다"**만 남긴다 — 하고 싶은 것이 아니라 정체성을 지키며 성장하는 데 꼭 필요한 것.

---

## 0. 비전 (정체성 — 흔들지 않음)

> **OOPforge는 백엔드 OOP/DDD에 특화된 Spec-Driven 방법론 + 아키텍처 강제(fitness function) 팩이다.**

- 우리는 **수직(vertical) 방법론**이다. 범용 코딩 에이전트·코드 인덱서·컨텍스트 압축기 같은 **수평(horizontal) 인프라**가 아니다.
- 대상은 **Java(Spring) / Python(FastAPI) 백엔드**와 **OOP/DDD를 제대로 하려는 팀**. 그 좁은 영역에서 **가장 깊다**.
- Spec-Driven Development(SDD) 생태계 안에서, OOPforge는 "도메인 모델/레이어 경계/전술적 DDD"에 특화된 변종이다.
- **효과 지표는 토큰 절감이 아니라 아키텍처 위반율과 재작업률이다.** 제약 없는 세션은 레이어/도메인 경계를 무너뜨리고, 명시적 제약(constitution + skills + fitness function)은 위반을 거의 0으로 만든다.

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
- `[중기]` **B1. MCP 서버 모드** — `oopforge serve --mcp`. 스킬/룰/안티패턴을 MCP로 주입, 룰 위반 시 **실시간 피드백**. instructions 파일·재시작 없이 작동. **opt-in 실험**으로 시작. (멀티에이전트 환경에서 각 에이전트에 규율을 얹는 우리다운 방법 — 오케스트레이터가 되는 것과 다름)

### 축 C — 강제 & 증명

- `[단기]` **C2. 도메인 리뷰 자동화** — Craft 기반 PR diff가 안티패턴/하드룰 위반을 자동 코멘트. GitHub Action 템플릿. 위반 메시지를 에이전트에 피드백해 **자가교정** 유도. (수직 도구의 진짜 무기)
- `[단기]` **C4. 정성적 Proof + 포지셔닝** — 무개입 vs OOPforge before/after diff, README 상단 install + Craft 실행 GIF/asciinema, 위반율/재작업 약한 정량표. `docs/positioning.md` 경쟁 비교표 + "우리는 무엇이 아닌가"를 README 첫 화면으로. (가장 싸고 임팩트 큼)
- `[중기]` **C1. fitness function 확장** — 헥사고날용 import-linter/ArchUnit, archlint에 축 A 패턴 검사 추가(outbox 트랜잭션, saga 경계, 다중 Aggregate 탐지).

---

## 다음 릴리스 우선순위 (단기)

| 우선 | 항목 |
|---|---|
| C4 | before/after proof + README GIF + `docs/positioning.md` |
| C2 | PR diff 자동 리뷰 |
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

- **언어 확장** (수직 정체성 유지 선에서만, 각 언어 layered + hexagonal + runnable 예제 필수): Kotlin Spring → TypeScript NestJS → Go → C# .NET
- **패키징**: Phase 1 symlink 팩(현재) → Phase 2 플러그인 마켓플레이스 + MCP 서버 모드 → Phase 3 Claude Agent SDK 기반 독립 CLI
