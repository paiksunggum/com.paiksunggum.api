# 백엔드 아키텍처 규칙

관련 문서: [[ENTITY_RULE]] · [[_docs/CLAUDE]]

## 5-A. 헥사고날 + SOLID (titanic / friday13th 기준)

```
HTTP Request
  ↓
adapter/inbound/api/v1/{domain}_router.py   ← HTTP만, UseCase 주입
  ↓ (추상 포트)
app/ports/input/{domain}_use_case.py        ← ABC 계약만 (구현 없음)
  ↓
app/use_cases/{domain}_interactor.py        ← 비즈니스 로직 구현
  ↓ (추상 포트)
app/ports/output/{domain}_repository.py    ← ABC 계약만 (구현 없음)
  ↓
adapter/outbound/pg/{domain}_pg_repository.py ← DB 구현
  ↓
adapter/outbound/orm/{entity}_orm.py        ← SQLAlchemy ORM 모델
```

**레이어 규칙:**

| 레이어 | 허용 | 금지 |
|--------|------|------|
| `app/ports/input/` | `ABC` + `@abstractmethod`만 | 구현, 로깅, `*Impl` 클래스 |
| `app/ports/output/` | `ABC` + `@abstractmethod`만 | 구현, 로깅 |
| `app/use_cases/` | input port 상속, output port 호출 | 직접 DB 접근 |
| `adapter/inbound/` | HTTP 파싱, DI로 use case 주입 | PgRepository 직접 호출 |
| `adapter/outbound/` | output port ABC 상속, DB I/O | 비즈니스 로직 |

**포트 규칙:**
- 포트 추상 메서드에는 `self` 없음; use_cases·adapter 구현에는 `self` 유지
- `Protocol` 사용 안 함 — `ABC` 사용
- 로그 prefix는 **구현 클래스명만** (`JamesCommand`, `JamesPgRepository`)
- 로그는 레이어 간 **데이터 넘길 때만** (포트 내 로그 금지, return 경로 중복 금지)

**SOLID 대응표:**

| 원칙 | 적용 방식 |
|------|----------|
| **S** (단일 책임) | 라우터=HTTP, 인터랙터=오케스트레이션, 어댑터=I/O |
| **O** (개방-폐쇄) | DB 변경 시 `adapter/outbound`만 교체 |
| **L** (리스코프) | 어댑터 구현이 포트 계약을 그대로 이행 |
| **I** (인터페이스 분리) | command/query 포트 분리 (James=쓰기, Walter=읽기) |
| **D** (의존성 역전) | 상위 레이어는 구체 클래스가 아닌 추상 포트에 의존 |

**의존성 주입 예시:**
```python
# dependencies/{domain}_command.py
def get_james_command_use_case(db: AsyncSession = Depends(get_db)) -> JamesCommandUseCase:
    repository: JamesRepository = JamesPgRepository(session=db)
    return JamesCommandInteractor(repository=repository)
```

---

## 5-B. 계층형 구조 (sports / admin — 단순 모듈)

```
Router → Controller → Service → Repository → SQLModel
```

- 라우터: HTTP만, Controller DI 호출
- Controller: `self.service` 보유, 메서드는 service에 한 줄 위임
- Service: reader·model 조합, 유스케이스당 메서드 하나
- Repository: DB I/O만

---

## 5-C. 엔티티 / DB 규칙

```python
class Example(SQLModel, table=True):
    __tablename__ = "examples"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
```

- **모든 테이블 PK는 `id: int` (자동 증감)**
- PK를 `user_id`, `uuid`, `pk` 등 다른 이름으로 두지 않는다
- 비즈니스 식별자(`user_id`, `email`)는 유니크·인덱스 컬럼으로 별도 정의
- 외래 키 컬럼명: `{엔티티}_id` 형태 (예: `user_id`)
