---
name: antipattern-flat-package
description: layered/3-tier를 골랐는데 레이어를 폴더로 나누지 않고 한 폴더에 파일명 suffix로만 분리한 안티패턴.
tags: [antipattern, layered, structure]
stability: experimental
---

# Anti-pattern — Flat Package

## 증상

layered(3-tier)를 선택했는데 `controller/ service/ repository/ domain/` 폴더가 없고,
한 폴더에 `OrderController`, `OrderService`, `OrderRepository`가 파일명으로만 구분되어 있다.

```text
order/
├── OrderController.java
├── OrderService.java
├── OrderRepository.java
└── Order.java
```

## 왜 나쁜가

- 레이어 경계가 **이름 규칙(convention)**에만 의존해 강제력이 없다. 누구든 곧 깬다.
- 새 파일이 어느 레이어인지 폴더로 드러나지 않아, 의존 방향 위반(Controller → Repository 직접 호출)이 눈에 안 띈다.
- 도메인이 늘면 파일명 prefix가 길어지고(`OrderItemQueryServiceImpl`) 탐색이 무너진다.
- 헥사고날/clean으로 점진 이행할 때 옮길 단위가 불명확하다.

## 왜 생기나

작은 모델·빠른 생성에서 **최소저항경로**다. "3-tier 앱 만들어줘" → 폴더 하나 + 파일명 suffix.
headless 구조 강제가 없으면 항상 이쪽으로 무너진다.

## 올바른 형태

레이어를 **물리적 폴더**로 분리한다.

```text
order/
├── controller/OrderController.java
├── service/OrderService.java
├── repository/OrderRepository.java
└── domain/Order.java
```

자세한 표준 구조는 `skills/skeleton/backend-skeleton.md`를 따른다.

## 탐지

- 스켈레톤 직후 디렉터리 트리에 `controller/ service/ repository/` 폴더가 없다.
- 한 폴더 안에 `*Controller`, `*Service`, `*Repository`가 함께 있다.
- Controller가 Repository를 직접 import/호출한다.

## 교정

1. `controller/ service/ repository/ domain/` 폴더를 만든다.
2. 각 파일을 자기 레이어 폴더로 이동한다 (동작 보존, `workflow/refactor.md`).
3. Controller → Service → Repository 의존 방향을 확인한다.
4. 테스트 폴더도 같은 구조로 미러링한다.

## 관련

- `skills/skeleton/backend-skeleton.md` — 표준 레이아웃 + 셀프 체크
- `AGENTS.md` Hard Rules — Layer layout
- `skills/workflow/refactor.md` — 동작 보존 이동
