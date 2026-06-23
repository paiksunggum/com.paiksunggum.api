상위: [[CLAUDE]]

# 백엔드 (paik) — Claude 작업 지침

> 이 파일은 `vault/paik/CLAUDE.md` ↔ `paik/CLAUDE.md` 심볼릭 링크로 동기화됩니다.
> Obsidian에서 편집하면 Claude Code도 같은 내용을 읽습니다.

---

## 모듈 목록 및 아키텍처 패턴

| 모듈 | 패턴 | 비고 |
|------|------|------|
| `titanic` | 헥사고날 + SOLID | **레퍼런스 구현** |
| `friday13th` | 헥사고날 + SOLID | 인증 모듈, 적용 중 |
| `sports` | 계층형 (Controller→Service→Repo) | |
| `admin` | 계층형 | |
| `chat` | 계층형 | Gemini 연동 |
| `agora`, `inception`, `imitation_game` | 계층형 | |
| `weather`, `vision`, `social_network` | 계층형 | |

새 모듈 작성 시 **titanic을 레퍼런스**로 쓴다. → [[paik/apps/titanic/_docs/CLAUDE]]

---

## 헥사고날 아키텍처 — 디렉터리 구조

```
apps/{domain}/
├── adapter/
│   ├── inbound/
│   │   └── api/
│   │       ├── schemas/     ← Pydantic 요청/응답 스키마
│   │       └── v1/          ← FastAPI 라우터 (HTTP 파싱만)
│   └── outbound/
│       ├── mappers/         ← ORM ↔ Entity 변환
│       ├── orm/             ← SQLAlchemy ORM 모델
│       └── pg/              ← output port 구현 (DB I/O)
├── app/
│   ├── dtos/                ← 레이어 간 전달 객체
│   ├── ports/
│   │   ├── input/           ← ABC UseCase 계약
│   │   └── output/          ← ABC Repository 계약
│   └── use_cases/           ← 비즈니스 로직 (Interactor)
├── dependencies/            ← DI 조립 (FastAPI Depends)
└── domain/
    ├── entities/            ← 도메인 엔티티 (순수 Python)
    └── value_objects/       ← 값 객체
```

---

## 레이어 규칙 (금지/허용)

| 레이어 | 허용 | 금지 |
|--------|------|------|
| `app/ports/input/` | `ABC` + `@abstractmethod`만 | 구현, 로깅, `*Impl` 클래스 |
| `app/ports/output/` | `ABC` + `@abstractmethod`만 | 구현, 로깅 |
| `app/use_cases/` | input port 상속, output port 호출 | 직접 DB 접근 |
| `adapter/inbound/` | HTTP 파싱, DI로 use case 주입 | PgRepository 직접 호출 |
| `adapter/outbound/pg/` | output port ABC 상속, DB I/O | 비즈니스 로직 |

**포트 규칙:**
- 포트 ABC 추상 메서드에는 `self` 없음; use_cases·adapter 구현에는 `self` 유지
- `Protocol` 사용 안 함 — `ABC` 사용

---

## 흐름 요약

```
HTTP Request
  ↓
adapter/inbound/api/v1/{domain}_router.py     ← HTTP만, UseCase DI 주입
  ↓ (추상 input port)
app/ports/input/{domain}_use_case.py          ← ABC 계약
  ↓
app/use_cases/{domain}_interactor.py          ← 비즈니스 로직
  ↓ (추상 output port)
app/ports/output/{domain}_repository.py       ← ABC 계약
  ↓
adapter/outbound/pg/{domain}_pg_repository.py ← DB 구현
  ↓
adapter/outbound/orm/{entity}_orm.py          ← ORM 모델
```

---

## DI 조립 패턴

```python
# dependencies/{domain}_command_provider.py
def get_{domain}_command_use_case(
    db: AsyncSession = Depends(get_db),
) -> {Domain}CommandUseCase:
    repository: {Domain}Repository = {Domain}PgRepository(session=db)
    return {Domain}CommandInteractor(repository=repository)
```

---

## SOLID 대응

| 원칙 | 이 프로젝트에서 |
|------|----------------|
| **S** 단일 책임 | 라우터=HTTP, 인터랙터=오케스트레이션, 어댑터=I/O |
| **O** 개방-폐쇄 | DB 변경 시 `adapter/outbound`만 교체 |
| **L** 리스코프 | 어댑터 구현이 포트 계약을 그대로 이행 |
| **I** 인터페이스 분리 | command/query 포트 분리 (James=쓰기, Walter=읽기) |
| **D** 의존성 역전 | 상위 레이어는 추상 포트에 의존 |

---

## 엔티티 / DB 규칙

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
- `user_id`, `uuid`, `pk` 등 다른 이름 금지
- 비즈니스 식별자(`user_id`, `email`)는 유니크 컬럼으로 별도 정의
- 외래 키 컬럼명: `{엔티티}_id` (예: `user_id`)
- `Protocol` 사용 안 함 — `ABC` 사용

---

## 로그 규칙

- 로그 prefix는 **구현 클래스명만** (예: `JamesCommandInteractor`, `JamesPgRepository`)
- 포트(ABC) 내부에 로그 금지
- 레이어 간 **데이터를 넘길 때만** 로그 (return 경로 중복 금지)

---

## 파일 네이밍 패턴

```
{persona}_{role}_{type}.py
예) crew_james_command_interactor.py
    passenger_rose_model_pg_repository.py
    crew_james_command_use_case.py
```

---

## 계층형 구조 (sports, admin 등 단순 모듈)

```
Router → Controller → Service → Repository → SQLModel
```

- 라우터: HTTP만, Controller DI
- Controller: `self.service` 보유, 메서드는 service에 한 줄 위임
- Service: 유스케이스당 메서드 하나
- Repository: DB I/O만

---

## 공통 인프라 (core/matrix/)

| 파일 | 역할 |
|------|------|
| `oracle_database.py` | AsyncSession, get_db |
| `keymaker_api.py` | API 키 (Gemini 등) |
| `secret_manager.py` | 환경변수/시크릿 |
| `theone_base.py` | SQLModel Base |

---

## 개발 서버

```bash
conda activate venv
python run.py   # 포트 8000 / Swagger: localhost:8000/docs
```

에이전트는 서버를 자동 실행하지 않는다. 사용자 요청 시에만.

---

## 머신러닝 데이터 분석 원칙

### Categorical — 데이터가 카테고리로 묶일 때 사용

**nominal** : 이름을 바탕으로 하는 척도
순서와는 상관없이 그냥 셀 수 있는 정도의 데이터
예) 청팀, 홍팀, 백팀

**ordinal** : 순서를 바탕으로 하는 척도
자료들 사이에 순서(서열)가 있는 경우
예) 청팀이 이길 가능성 1.매우낮음 2.낮음 3.보통 4.높음 5.매우높음

### Quantitative — 숫자로 셀 수 있을 때 사용

**interval** : 간격을 바탕으로 하는 척도
기준 없이 일정한 측정 구간을 갖는 데이터 (배수 비교 불가)
예) 시간대(11:00~11:05), 온도, pH → "10배 덥다"는 표현 불가

**ratio** : 비율을 바탕으로 하는 척도
임의의 원점을 기준으로 두고 정하는 데이터 (배수 비교 가능)
예) 나이, 돈, 몸무게 → "10배 많다"는 표현 가능

---

## async def vs def 판단 기준

포트 추상 메서드에 `async`를 붙일지 결정할 때:

| 상황 | 선택 |
|------|------|
| DB 읽기/쓰기 (SELECT, INSERT 등) | `async def` |
| 외부 API 호출 (HTTP, Gemini 등) | `async def` |
| CPU 연산만 (형태소 분석, 수식 계산 등) | `def` |

- `async def`는 "이 함수가 I/O를 기다린다"는 신호다. I/O가 없는데 `async`를 붙이면 호출부에 불필요한 `await`가 생기고 의미가 흐려진다.
- 같은 포트 안에서도 메서드마다 다를 수 있다. `introduce_myself`(DB 조회) → `async def`, `analyze_intent`(Kiwi 형태소 분석) → `def`.
