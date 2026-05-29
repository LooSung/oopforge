---
description: OOPforge Implement 단계 — 유스케이스 1개를 테스트와 함께 구현
---

**OOPforge Implement** 단계를 수행하라. 구현할 유스케이스:

**$ARGUMENTS**

## 스킬 경로

OOPforge 팩 루트: `$OOPFORGE_HOME` → `~/.oopforge` → (개발 시) 이 저장소 루트. 아래 `{pack}` 는 그 루트.

## 사전 조건

- Skeleton이 존재
- 유스케이스 1개만 지정 (여러 개 동시 X)

## 절차

1. `{pack}/skills/workflow/implement.md` 를 먼저 읽는다.
2. 관련 OOP 스킬 참조:
   - `{pack}/skills/oop/application-service.md`
   - 필요 시 `aggregate-root`, `value-object`, `repository-port`
3. **순서대로 구현 (안에서 밖으로):**
   - (1) 도메인 모델 메서드 + 단위 테스트
   - (2) 유스케이스 클래스
   - (3) outbound 어댑터 (Repository 구현 등)
   - (4) inbound 어댑터 (Controller/Router)
   - (5) 통합 테스트 최소 1개
4. 단위 + 통합 테스트 모두 통과 확인
5. 사용자에게:
   - "구현 완료. 코드 리뷰 후 머지 + 다음 유스케이스로 넘어가도 될까요?"

## Definition of Done

- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 도메인 어노테이션 0
- [ ] 한 파일 300줄 이하
- [ ] CHANGELOG 또는 PR 설명에 요약

## 금지

- 여러 유스케이스 동시 구현
- 테스트 없는 도메인 로직 커밋
- 도메인에 프레임워크 어노테이션 추가
- "임시로" 레이어 위반
