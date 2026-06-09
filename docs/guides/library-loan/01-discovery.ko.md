# Step 1 — Discovery

[English](./01-discovery.md) · [한국어](./01-discovery.ko.md)
> **코드 없음.** 언어, 경계, 용어만 정의합니다.

스킬: `{pack}/skills/workflow/discovery.md`

출력 저장 위치: `docs/library/discovery.md` (프로젝트 내)

---

## 예시 출력

```markdown
# Library — Discovery

## Glossary
- **Book**: 도서관이 소장한 물리적 도서. 고유 ISBN으로 식별.
- **Member**: 대출 권한이 있는 등록 회원.
- **Loan**: 특정 Member가 특정 Book을 빌린 사실. 반납 시 종료.
- **LoanId**: Loan을 식별하는 값 객체.

## Bounded Contexts
1. **Lending** — Loan, Book(가용 여부), Member(대출 자격)
2. **Catalog** — Book 메타데이터 (제목, 저자) ← Lending과 분리

## Aggregate Candidates
- Lending: `Loan` (root)
- Book 가용 여부는 Lending 컨텍스트 내 별도 조회로 처리

## Actors / External
- Member (웹 클라이언트)
- Catalog Service (외부 — 도서 존재 확인용)

## Non-Functional
- 대출 처리는 동기, p99 300ms 이내
- 동일 도서 동시 대출 요청 → 하나만 성공 (낙관적 락 or 유니크 제약)

## Open Questions
- 최대 대출 권수 제한이 있는가?
- 연체 시 대출 차단 정책?
- 반납 기한은 고정인가, 도서 종류별로 다른가?
```

---

## 체크포인트

질문: *"Discovery 결과 검토하고 Design 단계로 넘어가도 될까요?"*

다음: [02-design.ko.md](./02-design.ko.md)
