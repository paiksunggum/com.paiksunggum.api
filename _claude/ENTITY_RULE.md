# Entity / Table — 기본 키 `id` (int, 자동 증감)

> **Cursor 사용법**: `backend/**` 의 DB 모델·마이그레이션 작업 시 `@docs/DevOps/Backend/ENTITY_RULE.md`

---

## 에이전트 지시 (자동 적용)

1. **모든 테이블**의 기본 키(PK)는 **`int` 자동 증감**이며, **필드·DB 컬럼명 모두 `id`** 로 통일한다.
2. PK 이름을 `user_id`, `pk`, `uuid` 등 **다른 이름으로 두지 않는다.** (비즈니스 식별자는 별도 컬럼으로 둔다.)
3. SQLModel 엔티티 작성 시 아래 **표준 `id` 필드** 블록을 그대로 사용한다.
4. 외래 키는 참조 대상 테이블의 **`id`** 를 가리키고, 컬럼명은 `{엔티티}_id` 형태(예: `user_id`)로 둔다. PK와 혼동하지 않는다.

---

## 표준 기본 키 — SQLModel

시스템 내부용 자동 증감 고유 번호(기본 키):

```python
from sqlmodel import Field, SQLModel


class Example(SQLModel, table=True):
    __tablename__ = "examples"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},  # DB 컬럼명: id
    )
    # ... 이하 비즈니스 컬럼
```

`typing.Optional[int]` 를 쓰는 경우:

```python
from typing import Optional

from sqlmodel import Field, SQLModel


class Example(SQLModel, table=True):
    __tablename__ = "examples"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},  # DB 컬럼명: id
    )
```

### 규칙 요약

| 항목 | 규칙 |
|------|------|
| 타입 | `int` (DB: `INTEGER` / `SERIAL` 등 자동 증감) |
| PK 필드명 | `id` |
| DB 컬럼명 | `id` (`sa_column_kwargs={"name": "id"}`) |
| 생성 전 | `default=None` — INSERT 시 DB가 값 할당 |
| 비즈니스 키 | `user_id`, `email` 등은 **유니크·인덱스** 컬럼으로 별도 정의 |

---

## 참조 구현

- `backend/apps/secom/app/models/user.py` — `User` 테이블 (`id` PK + `user_id` 비즈니스 키)

---

## 금지·주의

- PK를 **UUID·문자열·복합 키**로 정의하지 않는다 (이 프로젝트 규칙).
- 테이블마다 PK 컬럼명을 다르게 짓지 않는다 (`users.id`, `orders.id` … 모두 `id`).
- `id` 와 동일 의미의 중복 컬럼(`row_id`, `seq` 등)을 추가하지 않는다.
