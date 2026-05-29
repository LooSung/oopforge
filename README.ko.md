# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **Forge small. Compose forever.**
>
> OOP 철학을 도구로 벼린다. Claude Code · Codex CLI · Cursor 등 AI 코딩 에이전트에 주입 가능한 skills + workflow 묶음.

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## 왜 OOPforge인가

OOPforge는 **DDD / OOP 전문 AI 엔지니어링 팩**이다. 범용 에이전트 프레임워크가 아니다.

| 원칙 | 의미 |
|---|---|
| **Small** | 한 스킬 = 한 개념, 스킬 200줄 이하 |
| **Measurable** | 파일 300줄, 메서드 20줄 — 리뷰 가능 단위 |
| **Workflow-first** | Discovery → Test, 사람 승인 유지 |
| **Proof over philosophy** | 실행 가능한 Java/Python 예제 |
| **Domain-first** | 도메인 레이어 프레임워크 import 0 |

요약: **구조가 기본값**이 되도록 해서 God Service 생성을 막는다.

---

## Before / After

팀은 DDD 다이어그램은 알지만, 실제로는 `@Service` 하나에 로직이 몰리는 경우가 많다. OOPforge는 **그 구조를 기본값**으로 만든다.

### Before (흔한 Spring 서비스)

```java
@Service
public class OrderService {
    public void createOrder(CreateOrderRequest req) {
        // 검증, 가격, 저장, 이벤트 — 한 클래스에 전부
        orderRepository.save(toEntity(req));
        eventPublisher.publish(...);
    }
}
```

**문제:** God Service · 도메인 모델 없음 · 비즈니스 규칙 분산 · 단위 테스트 어려움 · AI가 같은 패턴 반복 생성

### After (OOPforge)

```java
Order order = Order.place(orderId, customerId, lines);   // domain
placeOrder.handle(command);                            // use case
orderRepository.save(order);                             // port
order.popEvents();                                       // OrderPlaced
```

```text
order/domain/Order.java
order/application/provided/PlaceOrder.java
order/application/required/OrderRepository.java
order/application/service/PlaceOrderService.java
order/adapter/web/OrderController.java
order/adapter/persistence/InMemoryOrderRepository.java
```

**효과:** 도메인 중심 · 책임 분리 · Spring 없이 도메인 테스트 · 유지보수 용이 · 에이전트가 반복 가능한 레이아웃 따름

실행 가능한 참고 구현: [`examples/order-java/`](./examples/order-java/) (Java) · [`examples/order-python/`](./examples/order-python/) (Python)

---

## 철학

> **Model is replaceable. Workflow is permanent.**

모델은 계속 바뀐다 — Claude, GPT, OSS, 그 다음 무엇이든.
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

| Agent | 상태 | 설치 경로 |
|---|---|---|
| **Claude Code** | 지원 | `~/.claude/{skills,agents,commands}/oopforge` |
| **Codex CLI** | 지원 | `~/.codex/skills/oopforge` |
| **Cursor** | 미지원 (Phase 2) | 설치 스크립트 없음 — `.cursor-plugin/` 매니페스트만 존재 |
| **OpenCode** | 실험적 | `INSTALL_OPENCODE=1 ./install.sh` |

심볼릭 링크이므로 **`~/.oopforge` 에서 `git pull` 하면 스킬 내용이 즉시 반영** 된다.

설치 경로를 다시 잡아야 할 때 (새 링크 타깃이 추가된 버전 업 등):

```bash
cd ~/.oopforge && git pull && ./install.sh update
```

`./install.sh update` 는 `uninstall.sh` 실행 후 symlink를 재설치한다.

**Cursor 현재 사용법:** 프로젝트에 `AGENTS.md` 를 복사하거나 참조한다. [docs/cursor.md](./docs/cursor.md) 참고. 마켓플레이스 패키징은 Phase 2 예정 (ETA 없음).

**Claude Code:** [docs/claude-code.md](./docs/claude-code.md) · **OpenCode (실험):** [docs/opencode.md](./docs/opencode.md)

---

## 문제 해결 (Troubleshooting)

```bash
./doctor.sh                              # 설치 상태 확인
./uninstall.sh && ./install.sh           # 재설치
cd ~/.oopforge && git pull && ./install.sh update   # 업데이트 후 symlink 갱신
./install.sh --dry-run                   # 실행 계획만 보기
./install.sh --force                     # 기존 symlink 교체
./scripts/smoke-test.sh                  # 로컬 smoke test
```

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
├── examples/order-java/           ← Java Spring hexagonal 참고 구현
├── examples/order-python/         ← Python FastAPI hexagonal 참고 구현
├── docs/                          ← Cursor, Claude Code, OpenCode 가이드
├── .claude-plugin/                ← Claude Code 플러그인 매니페스트 (Phase 2)
├── .codex-plugin/                 ← Codex 플러그인 매니페스트 (Phase 2)
├── .cursor-plugin/                ← Cursor 플러그인 매니페스트 (Phase 2)
├── .opencode/                     ← OpenCode experimental notes
├── skills/
│   ├── _meta/skill-template.md    ← 새 스킬 작성 규칙
│   ├── workflow/                   ← 권장 순서: Discovery → Design → Delivery Plan → Skeleton → Implement → Test
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
├── agents/                         ← Claude Code subagents (ddd-architect, domain-reviewer)
├── commands/                       ← Claude Code workflow slash commands
├── AGENTS.md                        ← 공통 에이전트 지시 파일
├── CLAUDE.md                        ← Claude Code 진입 지시
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
- **한 파일: 300줄 이하** — PR 리뷰 가능 단위 (~15분 리뷰)
- **한 메서드: 20줄 이하 권장** — 단일 책임, 이름으로 의도 표현
- **한 스킬 파일: 200줄 이하** — 에이전트 컨텍스트 1회 로드 = 한 개념
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
- **Phase 2** — Claude Code / Codex / Cursor 플러그인 마켓플레이스 등록 (Cursor: ETA 없음, 매니페스트만 존재)
- **Phase 3** — Standalone CLI (Claude Agent SDK 위)

Phase 1을 충분히 사용한 다음에야 Phase 2로 간다.

---

## 영감

- *Domain-Driven Design* — Eric Evans
- *Implementing DDD* — Vaughn Vernon
- *Clean Architecture* — Robert C. Martin

---

## 참고 (Reference)

OOPforge와 별개 프로젝트입니다. 패키징·레이아웃 참고용이며, 의존이나 공식 연동을 의미하지 않습니다.

- 참고 구조: [obra/superpowers](https://github.com/obra/superpowers) — 멀티 하네스 플러그인 패키징

---

## 라이선스

MIT
