---
name: workflow-skeleton
description: Design 다음 단계. 패키지 구조와 인터페이스 파일을 생성한다. 비즈니스 로직은 아직 X.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Skeleton

## 언제 쓰나
Design이 끝났을 때. Implement 이전.
**패키지 구조 + 빈 클래스/인터페이스**만 만든다.

## 체크리스트
- [ ] 헥사고날 레이어 폴더 생성 (domain, application, infrastructure, interfaces)
- [ ] 애그리거트 클래스 골격 생성 (필드 + 빈 메서드)
- [ ] 값 객체 클래스 골격
- [ ] 포트 인터페이스 정의 (구현체 X)
- [ ] 유스케이스 클래스 골격 (빈 execute 메서드)
- [ ] 빌드 도구 파일 (pom.xml, pyproject.toml) 의존성만
- [ ] 테스트 폴더 미러링

## 표준 헥사고날 레이아웃

### Java (Spring)
```
src/main/java/com/example/order/
├── domain/                  ← 프레임워크 import 0
│   ├── model/               ← Aggregate, Entity, ValueObject
│   ├── event/               ← Domain events
│   └── port/                ← Repository 등 outbound port 인터페이스
├── application/             ← Use case orchestration
│   └── usecase/
├── infrastructure/          ← 어댑터 구현
│   ├── persistence/         ← JPA, MyBatis 등
│   └── external/            ← HTTP client, MQ 등
└── interfaces/              ← inbound 어댑터
    └── rest/                ← Controller
```

### Python (FastAPI)
```
src/order/
├── domain/
│   ├── model.py
│   ├── event.py
│   └── port.py
├── application/
│   └── usecase.py
├── infrastructure/
│   ├── persistence/
│   └── external/
└── interfaces/
    └── api.py
```

## 산출물

- 빈 메서드 시그니처만 있는 파일들
- 컴파일/실행은 가능 (NotImplementedError 또는 TODO)
- 테스트 폴더 구조 (테스트는 비어 있어도 됨)

## 금지
- **메서드 본문 작성 금지** — `throw new UnsupportedOperationException()` 또는 `raise NotImplementedError`
- **`if`, `for` 등 로직 금지**
- **데이터베이스 스키마 정의 금지** — Implement 단계로 미룸
- **레이어 위반 금지** — domain은 다른 어느 레이어도 import 하지 않음

## 다음 단계
사용자 승인 후 → `workflow-implement` (유스케이스 단위로)
