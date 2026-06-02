# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **Forge small. Compose forever.**
>
> OOP 철학을 도구로 벼린다. Claude Code · Codex CLI · Cursor 등 AI 코딩 에이전트에 주입 가능한 skills + workflow 묶음.
>
> **OOPforge는 OOP/DDD를 에이전트가 따르는 방언으로 정의하고**, 스킬·워크플로·예제·설치로 그 방언을 실행하는 **하네스**입니다. 방법론 팩이자 에이전트 하네스이며, 범용 agent framework가 아닙니다.
>
> Java(Spring) · Python(FastAPI)에 특화 — **3계층(Controller/Service/Repository)** 또는 **헥사고날/클린** 중 선택, OpenAPI/Swagger 기본 탑재.

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## 왜 OOPforge인가

OOPforge는 **DDD / OOP 전문 AI 엔지니어링 팩**이다. 범용 에이전트 프레임워크가 아니다. **OOP 방언을 위한 하네스 엔지니어링**으로 보면 된다 — 스킬은 문법, 하드 룰은 린트, `examples/`는 표준 구현, install·커맨드는 런타임이다.

| 원칙                      | 의미                                     |
| ------------------------- | ---------------------------------------- |
| **Small**                 | 한 스킬 = 한 개념, 스킬 200줄 이하       |
| **Measurable**            | 파일 300줄, 메서드 20줄 — 리뷰 가능 단위 |
| **Workflow-first**        | Discovery → Test, 사람 승인 유지         |
| **Proof over philosophy** | 실행 가능한 Java/Python 예제             |
| **Domain-first**          | 도메인 레이어 프레임워크 import 0        |

요약: **구조가 기본값**이 되도록 해서 God Service 생성을 막는다.


### 기본 실행 모드 — `/oopforge:craft`

`/oopforge:craft` 하나로 시작한다. 요청을 보고 가장 작은 경로를 고르며, 추천만 필요한 요청이면 구현하지 않고 경로만 제안한다.

```text
/oopforge:craft Email 값 객체 하나 추가해줘
/oopforge:craft 결제 도메인에 환불 기능 추가해줘
/oopforge:craft OrderService를 동작 변경 없이 정리해줘
```

`/oopforge:craft`는 기존 코드를 확인한 뒤 가장 작은 기존 도메인 workflow를 수행한다.
고급 사용자는 "Discovery부터 시작", "Delivery Plan 작성", "Test workflow 실행"처럼 특정 workflow stage를 Craft에 직접 요청할 수 있다.

---

## OOPforge 사용법

**처음이면 여기부터:** **[도서관 대출 가이드 →](docs/guides/library-loan/README.ko.md)**  
Discovery → Design → Skeleton → Implement (Java + Python) → Test

가이드 목차: [EN](docs/guides/library-loan/README.md) · [KO](docs/guides/library-loan/README.ko.md) · [JA](docs/guides/library-loan/README.ja.md) · [ZH](docs/guides/library-loan/README.zh.md)

| 자료                                                                                 | 용도                                                                                                                                                                     |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [도서관 대출 가이드](docs/guides/library-loan/README.ko.md)                          | 전체 워크플로우 튜토리얼                                                                                                                                                 |
| [Examples index](examples/README.md) | 실행 가능한 증명 — 4종 스택, 동일 place-order |
| [order-java](examples/order-java/) · [order-java-layered](examples/order-java-layered/) | Java hexagonal · Java 3-tier |
| [order-python](examples/order-python/) · [order-python-layered](examples/order-python-layered/) | FastAPI clean · FastAPI 3-tier |
| [Discovery 샘플 (library)](docs/sample-output/discovery-library.ko.md)               | 에이전트 기대 출력 ([EN](docs/sample-output/discovery-library.md) · [JA](docs/sample-output/discovery-library.ja.md) · [ZH](docs/sample-output/discovery-library.zh.md)) |
| [Design 샘플 (library)](docs/sample-output/design-library.ko.md)                     | 에이전트 기대 출력 ([EN](docs/sample-output/design-library.md) · [JA](docs/sample-output/design-library.ja.md) · [ZH](docs/sample-output/design-library.zh.md))          |

각 단계 끝에 **사람 승인** — 다음 단계로 건너뛰지 않는다.

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

실행 가능한 참고 구현: [examples/README.md](examples/README.md) — hexagonal·layered 동일 place-order

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

### 자주 쓰는 명령 (`~/.oopforge` 또는 이 repo 루트)

```bash
./scripts/setup/install.sh          # symlink 설치
./scripts/setup/doctor.sh           # pack·링크 확인
./scripts/setup/install.sh update   # git pull 후 symlink 갱신
```

### 빠르게 (curl 한 줄)

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

### 수동

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x scripts/setup/*.sh
./scripts/setup/install.sh
./scripts/setup/doctor.sh
```

`scripts/setup/install.sh` 는 감지된 Claude Code / Codex CLI 설정 디렉토리에 OOPforge 폴더를 심볼릭 링크한다:

| Agent           | 상태             | 설치 경로                                                |
| --------------- | ---------------- | -------------------------------------------------------- |
| **Claude Code** | 지원             | `~/.claude/{skills,commands}/oopforge`                   |
| **Codex CLI**   | 스킬 진입점으로 지원 | `~/.codex/skills/oopforge`                               |
| **Cursor Agent CLI** | 실험적 | `cursor-agent --plugin-dir ~/.oopforge` |

심볼릭 링크이므로 **`~/.oopforge` 에서 `git pull` 하면 스킬 내용이 즉시 반영** 된다.

### Claude Code

`install.sh`가 skills와 commands를 연결한다. Claude Code를 재시작한 뒤 아래처럼 사용한다:

```text
/oopforge:craft <request>
```

### Codex CLI

`install.sh`가 `skills/SKILL.md`를 Codex 스킬 진입점으로 연결한다. Craft 프롬프트를 일반 텍스트처럼 입력한다:

```text
/oopforge:craft <request>
```

### Cursor Agent CLI

Cursor는 install symlink 대신 `--plugin-dir`로 OOPforge를 로드한다:

```bash
cursor-agent --plugin-dir ~/.oopforge
```

이후 자연어로 요청하거나 Craft 프롬프트를 요청에 포함한다.

설치 경로를 다시 잡아야 할 때 (새 링크 타깃이 추가된 버전 업 등):

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

`./scripts/setup/install.sh update` 는 `scripts/setup/uninstall.sh` 실행 후 symlink를 재설치한다.

자세한 설정: [Claude Code](./docs/claude-code.md) · [Codex](./docs/codex.md) · [Cursor](./docs/cursor.md)

---

## 문제 해결 (Troubleshooting)

```bash
./scripts/setup/doctor.sh                              # 설치 상태 확인
./scripts/setup/uninstall.sh && ./scripts/setup/install.sh           # 재설치
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update   # 업데이트 후 symlink 갱신
./scripts/setup/install.sh --dry-run                   # 실행 계획만 보기
./scripts/setup/install.sh --force                     # 기존 symlink 교체
./scripts/ci/smoke-test.sh               # 로컬 smoke test
```

---

## 사용

### 어디서 시작할지 모르겠다면 — `/oopforge:craft`

전체 워크플로를 강제하지 않고, 사용자의 의도에 맞춰 최소 경로를 고른다.

### 스택 선택 (3계층 vs 헥사고날/클린)

| 스택 | 아키텍처 | 언제 |
|---|---|---|
| `java-spring-layered` | 3계층 (Controller/Service/Repository) | 작은 서비스, MVP |
| `java-spring-hexagonal` | 헥사고날 (domain/application/adapter) | 도메인 복잡, 어댑터 다수 |
| `python-fastapi-layered` | 3계층 (Router/Service/Repository) | 작은 서비스, MVP |
| `python-fastapi-clean` | 클린 (domain/application/infrastructure/presentation) | 도메인 복잡 |

모든 백엔드 스켈레톤은 **OpenAPI/Swagger UI 기본 탑재** (springdoc / FastAPI 내장).

### Codex 슬래시형 프롬프트

Codex에서는 아래를 일반 프롬프트로 입력한다. `skills/SKILL.md`가 해당 워크플로우 파일로 라우팅한다.

```text
/oopforge:craft 주문 도메인 Discovery부터 시작. 아직 코드는 작성하지 마.
/oopforge:craft python-fastapi-layered로 주문 생성 유스케이스 구현
/oopforge:craft 주문 생성 테스트
```

### Claude Code 슬래시 커맨드

```text
/oopforge:craft 결제에 환불 유스케이스 추가
/oopforge:craft 주문 도메인 Discovery부터 시작
/oopforge:craft java-spring-layered로 주문 생성 유스케이스 구현
```

### Cursor Agent CLI

```bash
cursor-agent --plugin-dir ~/.oopforge
```

```text
OOPforge Discovery: 주문 도메인. Discovery부터 — 코드는 아직 작성하지 마.
```

### 다른 에이전트에서

스킬이 자동으로 컨텍스트에 노출된다. 자연스럽게 요청만 하면 됨:

> "Java로 Order 애그리거트를 만들어줘. OOPforge 가이드라인 따라서."

---

## 구조

```
oopforge/
├── examples/
│   ├── README.md                   ← 스택 ↔ 폴더 매핑
│   ├── order-java/                 ← Java Spring hexagonal
│   ├── order-java-layered/         ← Java Spring 3-tier
│   ├── order-python/               ← Python FastAPI hexagonal
│   └── order-python-layered/      ← FastAPI 3-tier
├── docs/                          ← Cursor, Claude Code 가이드
├── .claude-plugin/                ← Claude Code 플러그인 매니페스트 (Phase 2)
├── .codex-plugin/                 ← Codex 플러그인 매니페스트 (Phase 2)
├── .cursor-plugin/                ← Cursor Agent CLI manifest (`--plugin-dir`; marketplace Phase 2)
├── skills/
│   ├── SKILL.md                    ← Codex 스킬 진입점
│   ├── workflow/                   ← 권장 순서: Discovery → Design → Delivery Plan → Skeleton → Implement → Test
│   ├── principles/                 ← OOP 판단 원칙
│   ├── playbooks/                  ← Craft 작업별 체크리스트
│   ├── oop/                        ← Domain model + use-case boundary
│   ├── lang/                       ← 백엔드 스택 선택 (layered vs hexagonal/clean)
│   └── skeleton/                   ← 선택된 스택별 패키지 구조 + 빈 타입
├── commands/                       ← Claude Code slash command entry point + /oopforge:craft
├── docs/roadmap.md                 ← 방향·우선순위·비-목표
├── AGENTS.md                        ← 공통 에이전트 지시 파일
├── CLAUDE.md                        ← Claude Code 진입 지시
└── scripts/
    ├── setup/             bootstrap, install, uninstall, doctor
    ├── ci/                lint-skills, smoke-test
    └── path-convention.md
```

---

## 워크플로우

OOPforge가 강제하는 단계. 절대 합치지 않는다.

| 단계          | 산출물                               | 금지                      |
| ------------- | ------------------------------------ | ------------------------- |
| **Discovery** | 용어집, 바운디드 컨텍스트            | 코드                      |
| **Design**    | 유스케이스 시그니처, 애그리거트 윤곽 | 구현                      |
| **Skeleton**  | 패키지 구조, 인터페이스              | 비즈니스 로직             |
| **Implement** | 유스케이스 단위 구현 + 테스트        | 다음 유스케이스 동시 작업 |

각 단계 끝에서 사람의 승인을 묻는다. 자동화의 함정을 피하기 위함.

**작은 작업**은 전체 파이프라인을 돌리지 말고 `/oopforge:craft`부터 시작한다.

---

## 코딩 룰 (측정 가능한 메트릭으로)

측정 가능한 강제 규칙의 source of truth는 [`AGENTS.md`](./AGENTS.md)다. README는 사용자용 개요만 유지하고, 에이전트는 규칙 검증 시 `AGENTS.md`를 따른다.

---

## 스킬 변경하기

새 파일을 늘리기보다 기존 aggregate skill을 먼저 확장한다. 핵심 OOP 규칙은 `skills/oop/domain-model.md` 또는 `skills/oop/use-case-boundary.md`, 스택 선택은 `skills/lang/backend-stack.md`, 백엔드 구조는 `skills/skeleton/backend-skeleton.md`에 모은다.

---

## 로드맵

패키징 단계:

- **Phase 1 (현재)** — Lightweight portable methodology layer (심볼릭 링크 설치)
- **Phase 2** — Claude Code / Codex / Cursor 플러그인 마켓플레이스 등록 (Cursor CLI는 `--plugin-dir`로 사용 가능; bootstrap symlink + marketplace는 Phase 2)
- **Phase 3** — Standalone CLI (Claude Agent SDK 위)

방향·우선순위·비-목표·언어 확장 계획·린트 강제·안티패턴 카탈로그는: **[docs/roadmap.md](./docs/roadmap.md)**

Phase 1을 충분히 사용한 다음에야 Phase 2로 간다.

---

## 영감

- _Domain-Driven Design_ — Eric Evans
- _Implementing DDD_ — Vaughn Vernon
- _Clean Architecture_ — Robert C. Martin
- _Test-Driven Development: By Example_ — Kent Beck

---

## 참고 (Reference)

OOPforge와 별개 프로젝트입니다. 패키징·레이아웃 참고용이며, 의존이나 공식 연동을 의미하지 않습니다.

- 참고 구조: [obra/superpowers](https://github.com/obra/superpowers) — 멀티 하네스 플러그인 패키징

---

## 라이선스

MIT
