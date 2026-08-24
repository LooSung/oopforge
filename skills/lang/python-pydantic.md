---
name: python-pydantic
description: Enforce typed FastAPI boundaries with explicit Pydantic validation, mypy, and contract tests.
tags: [python, fastapi, pydantic, typing, validation]
stability: stable
---

# Python Pydantic Boundaries

## When to use

Use this for Python FastAPI request/response models and their build checks.
Pydantic validates untrusted data at runtime; mypy checks source-level type
consistency. Use both. Neither replaces the other.

## Boundary rules

- Keep Pydantic in `presentation/` or `schemas/`; the domain has zero Pydantic
  imports.
- Declare Pydantic as a direct dependency when project code imports it. Do not
  rely on FastAPI's transitive dependency.
- Every request model sets an explicit unknown-field policy. Default to
  `ConfigDict(extra="forbid")` for command inputs.
- Choose coercion deliberately. For IDs, money, quantities, and operands, reject
  representations outside the API contract instead of accepting Pydantic's
  default coercion silently.
- Constrain non-finite numbers (`NaN`, `Infinity`) unless the use case explicitly
  defines them.
- Response models preserve semantic types such as `datetime`, `UUID`, and enums
  so OpenAPI retains their formats.
- Prefer frozen response models when response DTO mutation has no meaning.

Do not set blanket `strict=True` without checking every field. Python-side strict
validation rejects JSON strings for enum fields. Apply strictness to the fields
whose wire representation requires it:

```python
from typing import Annotated

from pydantic import AllowInfNan, BaseModel, ConfigDict, Strict

StrictFiniteFloat = Annotated[float, Strict(), AllowInfNan(False)]


class CalculateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operand_a: StrictFiniteFloat
    operand_b: StrictFiniteFloat
```

## Static type gate

Add mypy and use Pydantic's official plugin:

```toml
[tool.mypy]
python_version = "3.12"
plugins = ["pydantic.mypy"]
strict = true
files = ["app"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
```

Run `python -m mypy` as a blocking CI step before `pytest`. Start with
production code (`app`) so adopting strict mode does not require unrelated test
cleanup; expand to tests once their fixture annotations are ready.

## Boundary tests

For each request model, cover:

- valid JSON values;
- missing and null required fields;
- unknown fields;
- wrong scalar representations, including numeric strings when coercion is off;
- invalid enum values;
- lower/upper bounds and non-finite numbers where applicable.

Assert through the HTTP adapter when possible so the test proves FastAPI,
Pydantic, and error mapping together.

## Prohibited

- No Pydantic model as a domain entity.
- No `Any` or unchecked `dict` added just to silence mypy.
- No `# type: ignore` without a narrow error code and reason.
- No claim of strict input validation without executable boundary tests.
