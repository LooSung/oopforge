---
name: skill-template
description: OOPforge의 모든 스킬은 이 형식을 따른다. 새 스킬을 추가하기 전에 반드시 읽는다.
tags: [meta]
stability: stable
---

# Skill Template

> OOPforge의 모든 스킬은 이 형식을 따른다.
> 새 스킬을 추가하기 전에 반드시 이 파일을 읽고 형식을 복사한다.

---

## 1. 작성 원칙 (위반 금지)

1. **한 스킬 = 한 개념** — Aggregate와 Repository를 한 파일에 두지 않는다.
2. **200줄 이하** — 넘어가면 분할.
3. **Checklist-first** — 산문보다 체크리스트가 우선.
4. **예제 필수** — AI는 prose보다 example에서 더 잘 학습한다.
5. **금지 사항 명시** — "이건 절대 하지 마"가 가장 가치 있는 정보.

---

## 2. Frontmatter

```yaml
---
name: <kebab-case-name>            # 파일명과 일치
description: <한 문장. 언제 쓰는 스킬인지>
tags: [oop, java, ...]             # 검색용 (선택)
stability: stable | experimental | deprecated
---
```

---

## 3. 본문 구조

각 스킬은 다음 섹션을 가진다 (순서 고정):

```markdown
# <Skill Name>

## 언제 쓰나
한두 문장. 어떤 상황에서 이 스킬을 끌어쓸 것인가.

## 체크리스트
- [ ] 가장 중요한 규칙부터
- [ ] 측정 가능한 항목으로
- [ ] 5~10개

## 템플릿
\`\`\`<language>
// 그대로 쓸 수 있는 최소 예제
\`\`\`

## 금지
- 절대 하지 말아야 할 것들
- 명시적으로 적어야 AI가 회피한다

## 변형 (선택)
다른 흔한 변종 또는 컨텍스트별 차이
```

---

## 4. 새 스킬 추가 절차

```bash
cp skills/_meta/skill-template.md skills/<category>/<new-skill>.md
# 편집
git add . && git commit -m "feat(<category>): add <new-skill>"
```

스킬 추가 후 `CHANGELOG.md` 의 `[Unreleased]` 섹션에 한 줄 추가.

---

## 5. 카테고리 가이드

| 카테고리 | 들어가는 것 |
|---|---|
| `skills/_meta/` | 메타 규칙, 템플릿 |
| `skills/workflow/` | 단계별 프로세스 (Discovery, Design, ...) |
| `skills/oop/` | 언어 무관 OOP 개념 (Aggregate, Value Object, ...) |
| `skills/lang/<lang>/` | 특정 언어/프레임워크 구체화 |

---

## 6. 금지

- **Mega skill** — 한 파일에 5개 개념 묶는 것
- **산문만 있는 스킬** — 체크리스트, 예제 없이 설명만
- **모호한 description** — "OOP를 잘 합니다" 같은 거 금지
- **버전 없는 파괴적 변경** — 기존 스킬 의미가 바뀌면 deprecated로 표시 후 새 버전 생성
