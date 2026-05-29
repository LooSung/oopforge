# 샘플 출력 — Discovery: 도서관 대출 도메인

[English](./discovery-library.md) · [한국어](./discovery-library.ko.md) · [日本語](./discovery-library.ja.md) · [中文](./discovery-library.zh.md)

에이전트 프롬프트용 짧은 참고. 전체 가이드: [도서관 대출 가이드](../guides/library-loan/README.ko.md).

## 비즈니스 목표

회원이 도서를 대출한다. 대출 중인 도서는 재대출 불가. 대출 시 `BookBorrowed` 이벤트 발행.

## 바운디드 컨텍스트

- **Lending** — Loan, 도서 가용 여부, 회원 대출 자격
- **Catalog** — 도서 메타데이터 (제목, 저자) — Lending과 분리

## 핵심 개념

- Book, Member, Loan, LoanId, BookBorrowed

## 애그리게이트 후보

- **Loan** (Lending 컨텍스트 루트)

## 주요 불변식

- 도서에 활성 대출이 있으면 추가 대출 불가
- 반납된 대출은 다시 반납 불가
- Catalog는 ID로만 참조, 객체 임베드 금지

## 열린 질문

- 회원당 최대 대출 권수?
- 연체 정책?
- 고정 vs 가변 대출 기간?
