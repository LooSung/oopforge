# 图书馆借阅 — OOPforge 完整演练

> 用 Java (Spring Boot) 和 Python (FastAPI) 从零到一实现 **图书馆借阅系统**。  
> 按 Discovery → Design → Delivery Plan → Skeleton → Implement → Test 顺序进行。

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

本指南逐步展示 OOPforge **用法**。最小可运行示例见 [`examples/calculator-java-hexagonal`](../../../examples/calculator-java-hexagonal/) 和 [`examples/calculator-python-hexagonal`](../../../examples/calculator-python-hexagonal/)。

---

## 场景

会员 **借阅** 图书。已借出的图书不能再次借出。借阅时发布 `BookBorrowed` 事件。

---

## 斜杠命令 (Claude Code)

**Java 轨道:**

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in java-spring
/oopforge:craft Test borrow-book
```

**Python 轨道** — Discovery/Design/Delivery Plan 相同；仅 Skeleton 不同:

```text
/oopforge:craft Start Discovery for the library loan domain. No code yet.
/oopforge:craft Implement borrow-book in python-fastapi
/oopforge:craft Test borrow-book
```

每个项目只选 **一种技术栈**。两条轨道实现相同的 `borrow-book` 用例。

也可用自然语言开始:

```text
Follow OOPforge workflow for a library loan domain. Start at Discovery — no code yet.
```

---

## 步骤

| 步骤 | Java | Python |
|---|---|---|
| 1. Discovery | [01-discovery.zh.md](./01-discovery.zh.md) | 相同 |
| 2. Design | [02-design.zh.md](./02-design.zh.md) | 相同 |
| 3. Skeleton | [03-skeleton.zh.md](./03-skeleton.zh.md) § Java | [03-skeleton.zh.md](./03-skeleton.zh.md) § Python |
| 4. Implement | [04-implement-java.zh.md](./04-implement-java.zh.md) | [04-implement-python.zh.md](./04-implement-python.zh.md) |
| 5. Test | [05-test.zh.md](./05-test.zh.md) § Java | [05-test.zh.md](./05-test.zh.md) § Python |
| 6. 分层规则 | [06-layer-rules.zh.md](./06-layer-rules.zh.md) | 相同 |

各步骤文件顶部可切换 EN · KO · JA · ZH。

---

## 短样本 (agent 输出)

仅需 prompt 用的 **Discovery/Design 期望格式**:

| 语言 | Discovery | Design |
|---|---|---|
| English | [discovery-library.md](../../sample-output/discovery-library.md) | [design-library.md](../../sample-output/design-library.md) |
| 한국어 | [discovery-library.ko.md](../../sample-output/discovery-library.ko.md) | [design-library.ko.md](../../sample-output/design-library.ko.md) |
| 日本語 | [discovery-library.ja.md](../../sample-output/discovery-library.ja.md) | [design-library.ja.md](../../sample-output/design-library.ja.md) |
| 中文 | [discovery-library.zh.md](../../sample-output/discovery-library.zh.md) | [design-library.zh.md](../../sample-output/design-library.zh.md) |

---

## 每步之后

OOPforge 要求 **人工检查点**。在批准输出前不要进入下一阶段。

Implement 之后如需检查规则违反，可让 `/oopforge:craft` 按 Hard Rules 审查结果。
