---
name: workflow-test
description: 단위, 통합, E2E 테스트를 설계하고 보강한다. TDD 또는 회귀 검증이 필요할 때 사용한다.
tags: [workflow, test, quality]
stability: stable
---

# Workflow — Test

## 언제 쓰나
도메인 로직, 유스케이스, 어댑터, API/CLI 흐름의 테스트를 작성하거나 보강할 때.
TDD로 먼저 작성해도 되고, 구현 후 회귀 테스트로 작성해도 된다.

## 체크리스트
- [ ] 테스트 대상과 범위 정의
- [ ] 단위/통합/E2E 중 필요한 테스트 유형 선택
- [ ] 기존 테스트 구조와 네이밍 규칙 확인
- [ ] 도메인 규칙은 단위 테스트로 고정
- [ ] 유스케이스는 포트 mock/fake로 검증
- [ ] 어댑터는 실제 통합 또는 계약 테스트로 검증
- [ ] E2E는 핵심 사용자/시스템 흐름만 최소로 검증
- [ ] 실패/경계/권한/중복 실행 케이스 포함
- [ ] 실행 명령과 결과 기록

## 테스트 우선순위

| 테스트 | 목적 | 예시 도구 |
|---|---|---|
| Unit | 도메인 규칙과 순수 로직 고정 | JUnit, pytest |
| Use case | 애플리케이션 서비스 오케스트레이션 검증 | Mockito, unittest.mock |
| Integration | DB, HTTP, queue, filesystem adapter 검증 | Testcontainers, pytest fixtures |
| E2E | 실제 사용자/시스템 흐름 확인 | RestAssured, Playwright, httpx |

## 산출물

`docs/test-plan.md` 또는 `docs/<domain>/test-plan.md` 에 저장:

```markdown
# <Feature> — Test Plan

## Scope
- Target:
- Risk:

## Unit Tests
- 

## Integration Tests
- 

## E2E Checks
- 

## Fixtures / Test Data
- 

## Commands
- `...`

## Result
- 
```

## 금지
- **테스트 없이 도메인 로직 변경 금지**
- **프레임워크 테스트만 믿고 도메인 단위 테스트 생략 금지**
- **외부 서비스 실호출을 기본값으로 두기 금지**
- **불안정한 sleep/time/network 의존 테스트 금지**
- **테스트 이름을 구현 세부사항 중심으로 짓기 금지**

## 다음 단계
테스트 통과 후 → review, commit, push, MR/release note 작성
