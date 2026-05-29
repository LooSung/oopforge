---
name: workflow-implement
description: Skeleton 다음 단계. 유스케이스를 하나씩, 테스트와 함께 구현한다.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Implement

## 언제 쓰나
Skeleton이 끝났을 때. **유스케이스 하나 = 한 번의 Implement 사이클**.
여러 유스케이스를 동시에 구현하지 않는다.

## 체크리스트 (유스케이스 1개당)
- [ ] 도메인 모델 메서드 구현 + 단위 테스트
- [ ] 유스케이스 클래스 구현 (orchestration)
- [ ] 포트 어댑터 구현 (필요한 부분만)
- [ ] 인바운드 어댑터 (Controller 등) 구현
- [ ] 통합 테스트 1개 이상
- [ ] 사람의 코드 리뷰 통과

## 구현 순서 (안에서 밖으로)

```
1. Domain model 메서드 + 단위 테스트   ← 여기부터
2. Use case 클래스
3. Outbound port adapter (Repository 구현 등)
4. Inbound adapter (REST Controller 등)
5. 통합 테스트
```

도메인부터 짜야 프레임워크에 새지 않는다.

## 테스트 우선순위

| 종류 | 필수? | 도구 예시 |
|---|---|---|
| 도메인 단위 테스트 | **필수** | JUnit, pytest |
| 유스케이스 테스트 (port mock) | **필수** | Mockito, unittest.mock |
| 통합 테스트 (DB 포함) | **필수** | Testcontainers, pytest-docker |
| E2E | 선택 | RestAssured, httpx |

## 금지
- **여러 유스케이스 동시 구현 금지** — 한 번에 하나, 머지 후 다음.
- **테스트 없는 도메인 로직 커밋 금지**
- **도메인에 어노테이션 추가 금지** — `@Entity`, `@Component` 등은 infrastructure 레이어에서만
- **CRUD 메서드 추가 유혹 저항** — 유스케이스 동사로만
- **TDD 강요 X, 테스트 강요 O** — 순서는 자유, 존재는 필수

## 완료 정의 (Definition of Done)
- 단위 테스트 + 통합 테스트 통과
- 코드 리뷰 1명 이상
- `CHANGELOG` 또는 PR 설명에 변경 요약
- 다음 유스케이스로 넘어가기 전 머지

## 다음 단계
완료된 유스케이스 머지 → 다음 유스케이스로 Implement 사이클 반복.
모든 유스케이스 완료 시 → 도메인 단위 회고.
