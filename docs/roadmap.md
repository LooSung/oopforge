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

## 남은 작업

### v0.10.0 — 증명과 강제 연결 (현재)

**C4 — 반복 Proof + Craft 데모**

고정 조건의 control/OOPforge 짝 실험을 반복해 단일 실행의 우연을 분리한다.
유리한 결과를 만드는 것이 아니라 나온 결과를 그대로 누적하는 작업이다.

끝나는 조건:

- 같은 조건의 유효 짝을 최소 3개까지 누적하고 원시 근거를 공개한다.
- 유리·중립·불리한 결과를 모두 포함해 요약한다.
- README에 Craft GIF/asciinema를 연결한다.

**C2+ — 도메인 리뷰 자동화 확장**

- 안티패턴 탐지와 archlint layered/CQRS 검사를 재사용한다.
- 타깃 프로젝트 Action 템플릿을 제공한다.
- 위반 피드백 기반 자가교정 루프를 연결한다.

### v0.11.0 — 백엔드 깊이 (다음)

**A1 — Transactional Outbox**

DB 쓰기와 이벤트 발행을 같은 트랜잭션에 묶고 relay/CDC 전달,
ghost/lost 이벤트 방지를 가르친다.

### v0.12.0 — 이식성과 위생

**B2 — Claude/Codex/Cursor 3개 하네스 동등 지원 + Agent Skills 스펙 정렬**

- Claude, Codex, Cursor를 모두 1급 지원 대상으로 두고 설치·명령·스킬
  로딩·깨끗한 세션 검증 기준을 맞춘다.
- Cursor 공식 `.cursor-plugin/plugin.json`과
  `~/.cursor/plugins/local/oopforge` 로컬 플러그인 경로를 검증한다.
- `commands/craft.md`의 공식 command frontmatter를 맞추고
  `.cursor-plugin/README.md`와 `docs/cursor.md`의 낡은 Phase 2 설명을 고친다.
- 세 하네스 검증 후 `SKILL.md` frontmatter와 progressive disclosure를
  표준화해 다른 Agent Skills 호환 환경으로 넓힌다.

**B3 — 레포 위생**

죽은·중복 스킬, 끊긴 링크, 빌드 산출물을 정리하고 문서 링크
무결성 CI를 건다.

---

## 장기 목표

### 백엔드 깊이

- `skills/oop/saga.md` — Aggregate/서비스를 가로지르는 프로세스와 보상 트랜잭션.
- `skills/oop/domain-events.md` — 내부/통합 이벤트, idempotent consumer,
  이벤트 스키마 버저닝과 upcaster.
- `skills/workflow/production-readiness.md` — 입력 검증, 오류 응답, 멱등성,
  재시도, 관측성, 감사 로그, PII/시크릿을 어댑터에서 충족하는 NFR 게이트.

### 강제와 배포

- **C1. fitness function 확장** — 헥사고날 import-linter/ArchUnit,
  outbox·saga·다중 Aggregate 검사.
- **B1. MCP 서버 모드** — archlint·안티패턴 탐지·도메인 리뷰를
  실시간 자가교정 도구로 노출하는 opt-in 실험.
- **패키징** — symlink 팩에서 플러그인 마켓플레이스, 이후 독립 CLI로 발전.

### 언어 확장

C4 반복 증거, B3 위생, C1/C2+ 강제, B2 이식성을 먼저 갖춘다.
그 뒤 각 언어에 layered + hexagonal + runnable 예제와 강제를 함께 제공한다.

Kotlin Spring → TypeScript NestJS → Go → C# .NET

---

## 비-목표 (가드레일)

- **수평 인프라화** — 범용 에이전트·코드 인덱서·컨텍스트 압축기와 경쟁하지 않음
- **멀티에이전트 오케스트레이션** — worktree 격리·세션 관리·에이전트 간 통신은 우리 몫이 아니다. 우리는 **각 에이전트가 따르는 설계 규율**이지 오케스트레이터가 아니다
- **토큰/비용 벤치마크 경쟁** — 지표는 위반율·재작업률
- **메가 스킬/메가 프롬프트** — 한 파일에 여러 개념 X
- **GUI/IDE 플러그인** — CLI/에이전트 통합으로 충분
- **자동 코드 생성기** — 패턴은 가르치고, 코드는 에이전트가 작성
- **UI/모바일/ML 진출** — DDD 핵심 + 백엔드 OOP에 집중
- **불안정한 통합을 default install에 포함** — 실험(MCP 등)은 별도 opt-in
