# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![Examples](https://github.com/LooSung/oopforge/actions/workflows/examples.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **AI는 기능을 만든다. OOPforge는 구조를 지킨다.**
>
> *바이브 코딩이 백엔드를 망치지 않게 하는 하네스 엔지니어링.*

**Forge small. Compose forever.** OOPforge는 이식 가능한 OOP/DDD 방법론
팩이자 에이전트 하네스다. 스킬은 문법을 가르치고, 하드 룰은 린트처럼
작동하며, 실행 가능한 예제는 기준을 제공하고, Craft는 작업에 필요한 가장
작은 워크플로를 고른다.

**Java(Spring)** 또는 **Python(FastAPI)** 백엔드에서 명시적인 도메인 모델,
유스케이스 경계, 리뷰 가능한 아키텍처가 필요할 때 사용한다. 범용 에이전트
프레임워크, UI 도구, 자동 코드 생성기는 아니다.

[포지셔닝과 비-목표](docs/positioning.md) ·
[재현 가능한 Proof 프로토콜](docs/proof/README.md)

[English](./README.md) · [한국어](./README.ko.md)

## 빠른 시작

### 1. 최신 `main` 설치

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

bootstrap은 `~/.oopforge`를 clone 또는 갱신하고 감지된 Claude Code·Codex
링크를 설치한다. Cursor는 자동 설정하지 않는다.

### 2. 팩과 설치 링크 확인

```bash
~/.oopforge/scripts/setup/doctor.sh
```

`doctor.sh`는 팩 구조와 사용 가능한 symlink를 검사한다. 성공 결과가 실행
중인 에이전트의 Craft 로드를 증명하지는 않으므로 4단계에서 하네스별
진입점을 확인한다. 선택한 Claude·Codex 링크가 없다는 경고가 나오면
`INSTALL_CLAUDE=1 ~/.oopforge/scripts/setup/install.sh` 또는 Codex 대응
변수로 다시 설치한다.

### 3. 백엔드 프로젝트로 이동

OOPforge 팩은 `~/.oopforge`에 있고 앱 코드는 **백엔드 저장소**에 있다.
에이전트는 항상 대상 프로젝트에서 시작한다:

```bash
cd /path/to/your-backend-project
```

### 4. Craft를 로드하고 한 번 요청

| 하네스 | Craft 로드와 호출 |
|---|---|
| **Claude Code** | Claude Code 재시작 후 `/oopforge:craft <요청>` |
| **Codex CLI** | Codex 재시작 후 `/skills`에서 **oopforge**를 고르고 `/` 없이 요청 |
| **Cursor Agent CLI** | 로컬 플러그인을 등록·명시 로드한 뒤 `Use OOPforge craft: …` |

Claude Code:

```text
/oopforge:craft Email 값 객체 하나 추가해줘
```

Codex CLI:

```text
Use OOPforge craft: Email 값 객체 하나 추가해줘
```

Cursor Agent CLI는 등록 단계가 하나 더 필요하다:

```bash
mkdir -p ~/.cursor/plugins/local
ln -s ~/.oopforge ~/.cursor/plugins/local/oopforge
cd /path/to/your-backend-project
cursor-agent --plugin-dir ~/.cursor/plugins/local/oopforge
```

```text
Use OOPforge craft: Email 값 객체 하나 추가해줘
```

새 실행 작업에서 Craft가 로드되면 가장 작은 경로를 고르고 비즈니스 로직 전에
Assumptions와 OOP Contract를 제시한다. 자문 요청은 구현하지 않고 경로만
추천한다. [예시 Craft 세션](docs/assets/craft-demo.cast)과
[Claude Code](./docs/claude-code.md) · [Codex](./docs/codex.md) ·
[Cursor](./docs/cursor.md) 설정을 참고한다.

## 기본 워크플로

Craft가 단일 진입점이다. 작은 작업은 집중 경로를 고르고, 새 도메인이나 큰
기능은 전체 순서를 유지한다:

```text
Discovery → Design → Delivery Plan → Skeleton → Implement → Test
```

| 단계 | 산출물 | 금지 |
|---|---|---|
| **Discovery** | 용어집, 컨텍스트, 액터, 질문 | 코드 |
| **Design** | 유스케이스 시그니처, 애그리거트 윤곽, 포트 | 구현 |
| **Delivery Plan** | 범위, 순서, 테스트, 릴리스 위험 | 코딩 |
| **Skeleton** | 패키지, 인터페이스, 빈 클래스 | 비즈니스 로직 |
| **Implement** | 테스트된 유스케이스 하나씩 | 여러 유스케이스 동시 작업 |
| **Test** | 단위·통합·E2E 근거 | 테스트 없는 도메인 로직 |

각 단계 끝에는 사람 확인이 있다. 앞선 결정이 이미 있을 때만 Craft에 특정
단계부터 시작하라고 요청한다. 리팩토링은 동작을 보존해야 하므로 기능
워크플로 밖에서 진행한다.

지원 스택 식별자는 `java-spring-layered`, `java-spring-hexagonal`,
`python-fastapi-layered`, `python-fastapi-clean`이다. 백엔드 스켈레톤에는
OpenAPI/Swagger UI가 포함된다.
Domain Events와 transactional outbox 전달은 핵심 패턴이다. Production
Readiness gate는 명시적 배포 요청에만 선택한다.

### 세션 사이 작업 이어가기

실행 작업은 `.craft/` 아래에 가벼운 기록을 남긴다. 미완료 작업이 있으면
Craft가 편집 전에 Resume 블록을 제시한다. 세션이 끝났는데 일이 남으면
`.craft/next-session-prompt.md`가 다음 결정을 기록한다.

## 예제로 배우기

**처음이면 여기부터:** **[도서관 대출 가이드 →](docs/guides/library-loan/README.ko.md)**

| 자료 | 용도 |
|---|---|
| [도서관 대출 가이드](docs/guides/library-loan/README.ko.md) | 전체 워크플로 튜토리얼 |
| [Examples index](examples/README.md) | 실행 가능한 계산기 예제 6종 |
| [Reviewer checklist](docs/reviewer-checklist.md) | 구현 후 규칙 점검 |

## 왜 OOPforge인가

| 원칙 | 의미 |
|---|---|
| **Small** | 한 스킬 = 한 개념, 스킬 200줄 이하 |
| **Measurable** | 파일 300줄, 메서드 20줄 |
| **Workflow-first** | Discovery → Test, 사람 확인 유지 |
| **Proof over philosophy** | 실행 가능한 Java/Python 예제 |
| **Domain-first** | 도메인 레이어 프레임워크 import 0 |

요약하면 **구조가 기본값**이 되도록 해서 God Service 생성을 막는다.

## Before / After

팀은 DDD 다이어그램은 알지만 실제로는 `@Service` 하나에 로직이 몰리는 경우가
많다. OOPforge는 **그 구조를 기본값**으로 만든다.

### Before

```java
@Service
public class CalculatorService {
    public CalculationResponse calculate(CalculateRequest req) {
        repository.save(toEntity(req));
        eventPublisher.publish(...);
    }
}
```

**문제:** God Service · 도메인 모델 없음 · 비즈니스 규칙 분산 · 단위 테스트
어려움 · 에이전트가 같은 패턴 반복 생성

### After

```java
Calculation calc = Calculation.perform(id, operandA, operator, operandB);
calculate.handle(command);
calculationRepository.save(calc);
calc.popEvents();
```

**효과:** 도메인 중심 · 책임 분리 · Spring 없이 도메인 테스트 · 반복 가능한
레이아웃. 실행 가능한 참고 구현은 [examples/README.md](examples/README.md)에 있다.

### 증거와 한계

[Proof 프로토콜](docs/proof/README.md)은 과제, 대조군, OOPforge 적용군,
평가 규칙과 공개 기준을 고정한다. Cursor `gpt-5.6-sol-high`의 유효한 세 짝
중 [1](docs/proof/results/2026-08-20-cursor-gpt-5.6-sol-high.md)은 중립,
[2](docs/proof/results/2026-08-20-cursor-gpt-5.6-sol-high-2.md)와
[3](docs/proof/results/2026-08-20-cursor-gpt-5.6-sol-high-3.md)은 메서드
길이에서 유리했다. 세 짝 모두 공개 mutable 불변 상태 유출이 남았다.
[반복 짝 요약](docs/proof/README.md#repeated-pair-summary)을 참고한다.
이는 일반적인 효과 주장이 아니다.

## 설치, 업데이트, 제거

빠른 시작 bootstrap은 최신 `main`을 추적한다. 특정 릴리스를 설치하려면:

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
git checkout v0.15.0
chmod +x scripts/setup/*.sh
./scripts/setup/install.sh
./scripts/setup/doctor.sh
```

### 설치 대상

| 하네스 | 설치 또는 등록 경로 |
|---|---|
| **Claude Code** | `~/.claude/skills/oopforge`, `~/.claude/commands/oopforge` |
| **Codex CLI** | `~/.codex/skills/oopforge` |
| **Cursor Agent CLI** | 수동 로컬 플러그인 또는 프로젝트 로컬 skill |

`install.sh`는 Claude·Codex 설정 디렉터리가 있을 때만 링크를 만든다.
대상이 없으면 `INSTALL_CLAUDE=1` 또는 `INSTALL_CODEX=1`로 명시한다.
Cursor는 `install.sh`가 설정하지 않는다.

### 업데이트

GitHub Release는 기존 clone을 자동 갱신하지 않는다:

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

이 명령은 `main` 추적 clone용이다. 릴리스 태그에 고정한 clone은
`git fetch --tags` 후 선택한 새 태그를 checkout하고
`./scripts/setup/install.sh update`를 실행한다.

Claude·Codex는 에이전트를 재시작한다. Cursor의 수동 등록 링크는
`install.sh`가 관리하지 않으므로 pull 뒤 `cursor-agent`를 다시 시작한다.

### 검증과 문제 해결

아래 명령은 `~/.oopforge`에서 실행한다:

```bash
./scripts/setup/doctor.sh              # 팩 구조와 설치 링크
./scripts/setup/install.sh --dry-run   # 예정된 링크 변경
./scripts/setup/install.sh --force     # 충돌 symlink 교체
./scripts/ci/smoke-test.sh             # 격리된 Claude/Codex 설치 수명주기
```

이 검사는 실제 Craft 응답을 실행하지 않는다. 활성화는 사용하는 하네스의
진입점으로 확인한다: [Claude Code](./docs/claude-code.md) ·
[Codex](./docs/codex.md) · [Cursor](./docs/cursor.md).

### 제거

```bash
./scripts/setup/uninstall.sh
```

이 명령은 OOPforge가 관리하는 Claude·Codex 링크만 제거한다.
`~/.oopforge`, Cursor의 `~/.cursor/plugins/local/oopforge`, 프로젝트의
`.cursor/skills/oopforge`는 유지한다. 완전히 제거하려면 직접 삭제한다.

## 포함된 구성

- `skills/` — 워크플로, OOP/DDD, 스택, 스켈레톤, 리뷰 지침
- `commands/` — Claude Code 커맨드 진입점
- `examples/` — 실행 가능한 Java/Python 계산기 예제 6종
- `docs/` — 하네스 가이드, Proof, 로드맵, 튜토리얼
- `scripts/` — 설치, lint, 아키텍처 검사, smoke test
- `templates/github/` — 대상 프로젝트용 도메인 리뷰

에이전트 규칙의 정본은 [`AGENTS.md`](./AGENTS.md)이며
[`CLAUDE.md`](./CLAUDE.md)는 Claude Code 어댑터다.

## 프로젝트 정책

skill, script, CI, agent instruction은 영어를 정본으로 사용한다. 한국어
독자는 skill별 복제본 대신
[`docs/methodology.ko.md`](./docs/methodology.ko.md)를 사용한다.
필수 미래 작업과 비-목표는 [로드맵](./docs/roadmap.md), 완료된 릴리스는
[변경 이력](./CHANGELOG.md)에서 확인한다.

## 라이선스

MIT
