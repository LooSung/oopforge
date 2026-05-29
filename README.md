# OOPforge

> **Forge small. Compose forever.**
>
> OOP 철학을 도구로 벼린다. Claude Code · Codex CLI · OpenCode 등 어떤 AI 코딩 에이전트에도 주입 가능한 skills + workflow 묶음.

[English README](./README.en.md) · [한국어](./README.md)

---

## 왜 OOPforge인가 — 다른 방법론 팩과 무엇이 다른가

이미 [obra/superpowers](https://github.com/obra/superpowers) 같은 훌륭한 범용 워크플로우 팩이 있다. OOPforge는 그것들과 **경쟁이 아니라 보완** 한다:

| | obra/superpowers | SuperClaude | **OOPforge** |
|---|---|---|---|
| **초점** | 워크플로우 · TDD | 풀 플랫폼 · 슬래시 커맨드 | **DDD · 헥사고날 · OOP 도메인 모델링** |
| **언어** | 범용 | 범용 | **Java + Python 양손잡이** |
| **언어 (UI)** | 영어 | 영중일 | **한국어 1차 + English** |
| **룰 표현** | 가이드라인 | 행동 모드 | **300줄, 한 책임 — 명확한 메트릭** |

요약: **DDD를 진지하게 하는 한국어권 OOP 개발자를 위한 superpowers.**
범용 도구 옆에 같이 깔아도 충돌 없음.

---

## 철학

> **Model is replaceable. Workflow is permanent.**

모델은 계속 바뀐다 — Claude, GPT, Gemini, OSS, 그 다음 무엇이든.
하지만 **workflow, contracts, architectural discipline** 은 오래 살아남는다.

OOPforge는 모델 레이어가 아니라 **개발 프로토콜 레이어** 다.

### 4가지 원칙

1. **Small** — 한 스킬은 한 개념. 200줄 이하.
2. **Clean** — 프레임워크 의존성 없는 도메인. 주석은 "왜"만.
3. **Composable** — 작은 조각을 시간을 들여 붙여나간다.
4. **Sustainable** — Mega prompt 금지. Human checkpoint 유지.

---

## 설치

### 빠르게 (curl 한 줄)

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/bootstrap.sh)"
```

### 수동

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x install.sh uninstall.sh doctor.sh
./install.sh
./doctor.sh
```

`install.sh` 는 감지된 Claude Code / Codex CLI 설정 디렉토리에 OOPforge 폴더를 심볼릭 링크한다:

- Claude Code → `~/.claude/skills/oopforge`, `~/.claude/agents/oopforge`, `~/.claude/commands/oopforge`
- Codex CLI → `~/.codex/skills/oopforge`
- Cursor → `.cursor-plugin/` 매니페스트 준비 (Phase 2 플러그인 등록용)
- OpenCode → experimental. 기본 제외, 필요할 때만 `INSTALL_OPENCODE=1 ./install.sh`

심볼릭 링크이므로 **`~/.oopforge` 한 곳만 수정하면 모든 에이전트에 즉시 반영** 된다.

---

## 사용

### Claude Code 슬래시 커맨드

```text
/oopforge:discovery 주문 도메인
/oopforge:design 주문 생성 유스케이스
/oopforge:skeleton
/oopforge:implement
```

### Subagent 호출

```text
@ddd-architect 결제 도메인을 모델링해줘
```

### 다른 에이전트에서

스킬이 자동으로 컨텍스트에 노출된다. 자연스럽게 요청만 하면 됨:

> "Java로 Order 애그리거트를 만들어줘. OOPforge 가이드라인 따라서."

---

## 구조

```
oopforge/
├── .claude-plugin/                ← Claude Code 플러그인 매니페스트 (Phase 2)
├── .codex-plugin/                 ← Codex 플러그인 매니페스트 (Phase 2)
├── .cursor-plugin/                ← Cursor 플러그인 매니페스트 (Phase 2)
├── .opencode/                     ← OpenCode experimental notes
├── skills/
│   ├── _meta/skill-template.md    ← 새 스킬 작성 규칙
│   ├── workflow/                   ← Discovery → Design → Skeleton → Implement
│   ├── oop/                        ← 언어 무관 OOP/DDD 패턴
│   │   ├── aggregate-root
│   │   ├── value-object
│   │   ├── application-service
│   │   ├── repository-port
│   │   ├── domain-event           ★ v0.2
│   │   ├── bounded-context        ★ v0.2
│   │   ├── factory-method         ★ v0.2
│   │   └── specification-pattern  ★ v0.2
│   └── lang/                       ← 언어별 구체화
│       ├── java/                   ← Spring, JPA
│       └── python/                 ← Pydantic, FastAPI
├── agents/                         ← Claude Code subagents
├── commands/                       ← Claude Code slash commands
├── bootstrap.sh
├── doctor.sh
├── install.sh
└── uninstall.sh
```

---

## 워크플로우

OOPforge가 강제하는 4단계. 절대 합치지 않는다.

| 단계 | 산출물 | 금지 |
|---|---|---|
| **Discovery** | 용어집, 바운디드 컨텍스트 | 코드 |
| **Design** | 유스케이스 시그니처, 애그리거트 윤곽 | 구현 |
| **Skeleton** | 패키지 구조, 인터페이스 | 비즈니스 로직 |
| **Implement** | 유스케이스 단위 구현 + 테스트 | 다음 유스케이스 동시 작업 |

각 단계 끝에서 사람의 승인을 묻는다. 자동화의 함정을 피하기 위함.

---

## 코딩 룰 (측정 가능한 메트릭으로)

- **도메인 레이어 프레임워크 import: 0개**
- **한 파일: 300줄 이하**
- **한 메서드: 20줄 이하 권장**
- **한 스킬 파일: 200줄 이하**
- public 메서드는 유스케이스 동사 (CRUD 이름 금지)
- public setter 금지, 정적 팩토리 메서드 사용
- 컬렉션은 방어적 복사
- 테스트 없는 도메인 로직 커밋 금지
- 주석은 "왜"만, "무엇"은 이름으로

---

## 새 스킬 추가하기

`skills/_meta/skill-template.md` 를 먼저 읽어라. 모든 스킬은 그 형식을 따른다.

```bash
cp skills/_meta/skill-template.md skills/oop/<new-skill>.md
# 편집 후
git add . && git commit -m "feat(oop): add <new-skill> skill"
```

---

## 로드맵

- **Phase 1 (현재)** — Lightweight portable methodology layer (심볼릭 링크 설치)
- **Phase 2** — Claude Code / Codex / Cursor 플러그인 마켓플레이스 등록
- **Phase 3** — Standalone CLI (Claude Agent SDK 위)

Phase 1을 충분히 사용한 다음에야 Phase 2로 간다.

---

## 영감 / 참고

- [obra/superpowers](https://github.com/obra/superpowers) — 멀티 하네스 플러그인 구조 영감
- [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) — 풀 플랫폼 접근 참고
- *Domain-Driven Design* — Eric Evans
- *Implementing DDD* — Vaughn Vernon
- *Clean Architecture* — Robert C. Martin

---

## 라이선스

MIT
