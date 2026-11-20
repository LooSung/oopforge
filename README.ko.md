# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![Examples](https://github.com/LooSung/oopforge/actions/workflows/examples.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **AI는 기능을 만든다. OOPforge는 구조를 지킨다.**

OOPforge는 **Java Spring** 또는 **Python FastAPI** 백엔드(실험적으로 Kotlin Spring,
Next.js 앱의 TypeScript 서버 코드 포함)에서 일하는 코딩
에이전트용 스킬 팩이다. 에이전트가 비즈니스 로직을 쓰기 전에 도메인 모델,
유스케이스 경계, 포트를 먼저 정하게 하고, 결과를 측정 가능한 하드 룰로
검사한다. 하드 룰은 God Service와 도메인 계층의 프레임워크 코드를 금지한다.

**Claude Code**, **Codex CLI**, **Cursor Agent CLI**에서 동작한다.

[English](./README.md) · [한국어](./README.ko.md)

## Forge 패밀리

| 팩 | 대상 | 스택 |
|---|---|---|
| [Compforge](https://github.com/LooSung/compforge) | 프론트엔드 | TypeScript + React |
| **OOPforge** (이 저장소) | 백엔드 | Java Spring · Python FastAPI · Kotlin Spring·TypeScript Next.js (실험적) |
| [FuseForge](https://github.com/LooSung/fuseforge) | 두 쪽에 걸친 기능 하나 | Compforge + OOPforge 조율 (실험적) |

각 팩은 단독으로 쓸 수 있다. Claude Code에서는 `forge` 마켓플레이스 하나로 셋 다 받을 수 있다.

## 설치

**Claude Code**는 플러그인 마켓플레이스로 (실험적):

```text
/plugin marketplace add LooSung/oopforge
/plugin install oopforge@forge
```

다른 Forge 저장소에서 `forge`를 이미 추가했다면 첫 줄은 건너뛴다.
플러그인 파일은 프로젝트 밖에 있으므로 한 번 읽기 허용이 필요하다:
[읽기 권한](docs/setup/claude-code.md#plugin-marketplace-experimental).

**Codex CLI**, 또는 플러그인 없이 Claude Code를 쓸 때는 설치 스크립트로:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

스크립트는 `~/.oopforge`를 clone하고 Claude Code와 Codex에 연결한다. 하니스마다
한 가지 경로만 쓰고, 에이전트를 재시작한다. Cursor는 수동 단계가 하나 있다: [Cursor 설정](docs/setup/cursor.md).
릴리스 고정 설치, 업데이트, 제거: [설치 가이드](docs/setup/install.md).

## 사용

에이전트는 `~/.oopforge`가 아니라 **내 백엔드 프로젝트**에서 시작한다:

```text
/oopforge:craft Email 값 객체 하나 추가
/oopforge:refactor 동작은 그대로 두고 대출 규칙을 컨트롤러 밖으로 이동
/oopforge:review PR 42 리뷰
```

| 하니스 | 호출 방법 |
|---|---|
| Claude Code | `/oopforge:craft <요청>` |
| Codex CLI | `/skills` → **oopforge** 선택 후 `Use OOPforge craft: <요청>` (앞에 `/` 없음) |
| Cursor Agent CLI | `cursor-agent --plugin-dir ~/.oopforge` 후 `Use OOPforge craft: <요청>` |

## 명령

| 명령 | 언제 쓰나 | 절대 하지 않는 것 |
|---|---|---|
| `craft` | **기본값.** 유스케이스, 값 객체, 도메인 버그 | 필요한 단계 생략, 범위를 몰래 넓히기 |
| `refactor` | 동작을 바꾸지 않는 구조 개선 | 기능 추가 |
| `consult` | 질문, 비교, 리뷰, 계획 문서 1개 | 구현·테스트 코드 변경 |
| `test` | 테스트 실행·작성·강화 | 프로덕션 동작 변경. E2E와 인프라는 승인 필요 |
| `crucible` | 변경 하나를 계획 → 구현 → 리팩터 → 테스트까지 한 번에 | 계획 승인 전에 구현 시작 |
| `review` | diff, 브랜치, PR 하나에 대한 P1/P2/P3 지적 | 코드 변경, 요청 없이 PR에 게시 |
| `jira` | Jira 카드 1개, 또는 에픽·스토리 하나의 하위 작업 | 해당 이슈 외의 변경 |

뭘 써야 할지 모르겠다면 `craft`를 쓴다. 가장 작은 경로를 알아서 고른다.

## 동작 방식

1. **계약 먼저.** 비즈니스 로직 전에 Craft가 가정(Assumptions)과 OOP 계약
   (OOP Contract)을 밝힌다: 애그리거트, 불변식, 유스케이스, 포트.
2. **가장 작은 경로.** 값 객체 하나 추가는 작게 끝난다. 새 도메인이나 큰 기능은
   전체 흐름을 거치고, 단계마다 사용자가 승인한다:

   ```text
   Discovery → Design → Delivery Plan → Skeleton → Implement → Test
   ```

3. **검사.** 완료 보고 전에 [하드 룰](AGENTS.md#hard-rules)을 검증한다: 파일당
   300줄, 메서드당 20줄, 도메인 계층 프레임워크 import 0, 트랜잭션당 애그리거트 하나.

스택: `java-spring-layered`, `java-spring-hexagonal`, `python-fastapi-layered`,
`python-fastapi-clean`, 실험적으로 `kotlin-spring-layered`, `kotlin-spring-hexagonal`,
`typescript-next-layered`, `typescript-next-hexagonal`. 스켈레톤에는 OpenAPI/Swagger UI가 포함된다. 도메인
이벤트와 outbox는 기본이고, Production Readiness는 배포 요청에서만 켠다.

### Before → after

```java
// Before: God Service, 도메인 모델 없음, 흩어진 규칙, 테스트하기 어려움
@Service
public class CalculatorService {
    public CalculationResponse calculate(CalculateRequest req) {
        repository.save(toEntity(req));
        eventPublisher.publish(...);
    }
}

// After: 규칙은 도메인이 소유하고, 유스케이스는 조율만 한다
Calculation calc = Calculation.perform(id, operandA, operator, operandB);
calculationRepository.save(calc);
calc.popEvents();
```

## 프로젝트 스위치

내 프로젝트 `AGENTS.md`에 한 줄씩:

| 줄 | 효과 |
|---|---|
| `OOPforge continuity: off` | `.craft/` 작업 노트를 끈다. 기본값은 실행 작업마다 노트를 남기고, 편집 전에 미완료 작업을 이어간다. |
| `OOPforge work dir: <path>` | 작업 노트를 `.craft/`가 아닌 곳에 저장 |
| `OOPforge live run: on` | Craft·Refactor가 앱을 직접 띄워 확인 |
| `OOPforge cleanup pass: on` | 검증 후 Refactor가 `/simplify` 실행 |

백엔드 PR에 비차단 피드백을 받으려면
[`templates/github/oopforge-domain-review.yml`](templates/github/oopforge-domain-review.yml)을
복사한다. 차단 게이트는 선택이다:
[리뷰어 체크리스트](docs/reference/reviewer-checklist.md#enforcement-policy).

## 더 보기

- [도서 대출 워크스루](docs/guides/library-loan/README.ko.md): Discovery → Test 단계별 튜토리얼
- [예제](examples/README.md): 실행 가능한 계산기 12종 (Java, Python, 실험적 Kotlin·TypeScript Next.js × layered, hexagonal, hexagonal-CQRS)
- 설정: [Claude Code](docs/setup/claude-code.md) · [Codex](docs/setup/codex.md) ·
  [Cursor](docs/setup/cursor.md) · [설치·업데이트·제거](docs/setup/install.md)
- [지원 범위](docs/reference/support-scope.md) ·
  [Proof 실행 결과](docs/proof/README.md) (중립 결과 포함, 일반적 효과 주장 아님) ·
  [한국어 방법론 가이드](docs/reference/methodology.ko.md) · [전체 문서](docs/README.md)
- [변경 이력](CHANGELOG.md) · [기여 가이드](.github/CONTRIBUTING.md) ·
  [메인테이너용 에이전트 노트](AGENTS.md)

## 라이선스

MIT
