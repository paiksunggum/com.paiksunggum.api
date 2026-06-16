# 타이타닉 모듈 규칙

관련 문서: [[TITANIC_ERD]] · [[FORMA_ERD]] · [[fastapi_project_context]]

타이타닉은 이 프로젝트의 **헥사고날 + SOLID 레퍼런스 구현체**다.
`apps/` 하위에 시블링 구조로 새 앱이 추가될 때 이 모듈을 기준으로 삼는다.

---

## 5-D. 네이밍 컨벤션 (캐릭터 이름 기반)

역할마다 타이타닉 캐릭터 이름을 부여한다:

| 캐릭터         | 역할                         |
| ----------- | -------------------------- |
| **James**   | 쓰기(command) — CSV 업로드 등    |
| **Walter**  | 읽기(query) — 승객 조회 등        |
| **Smith**   | 선장(captain) — 전체 통계·LLM 대화 |
| **Andrew**  | 설계자(blueprint) — 승객 명단 관리  |
| **Rose**    | 모델(model) — ML 예측          |
| **Jack**    | 훈련(trainer) — ML 학습        |
| **Lowe**    | 구명보트(boat) — 생존자 분류        |
| **Hartley** | 바이올린(violin) — 음악/미디어      |
| **Molly**   | 스케일러(scaler) — 데이터 전처리     |

**파일 네이밍 패턴:**

| 레이어 | 파일명 |
|--------|--------|
| 라우터 | `{crew}_{character}_router.py` |
| 스키마 | `{crew}_{character}_schema.py` |
| 인바운드 use case (ABC) | `{crew}_{character}_use_case.py` |
| 아웃바운드 repo (ABC) | `{crew}_{character}_repository.py` |
| 인터랙터 (구현) | `{crew}_{character}_interactor.py` |
| PG 리포지토리 (구현) | `{crew}_{character}_pg_repository.py` |
| ORM | `{entity}_orm.py` |
| DTO | `{crew}_{character}_dto.py` |
| Provider | `{crew}_{character}_provider.py` |

---

## 새 앱 추가 시 체크리스트

`apps/` 하위에 새 모듈을 만들 때:

1. titanic 모듈 구조를 레퍼런스로 복사한다.
2. 헥사고날(복잡 도메인) vs 계층형(단순 CRUD) 중 선택한다.
3. `paik/main.py`에 라우터를 마운트한다 (`prefix` 없이 — titanic_router 자체에 prefix 포함).
4. 캐릭터 이름 네이밍을 새 도메인에 맞게 정한다.

## 타이타닉 도메인 문서 연결 :

*타이타닉 도메인 문서 연결
타이타닉 피처 정리 : [[titanic-features]]
타이타닉 머신러닝 : [[titanic-machine-learning]]
타이타닉 ERD : [[TITANIC-ERD]]
타이타닉 NF : [[titanic-nf]]
타이타닉 알고리즘 : [[titanic-algorithm]]
