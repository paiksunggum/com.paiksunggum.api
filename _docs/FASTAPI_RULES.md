# FastAPI — 계층형 최소 구조

> **Cursor 사용법**: `backend/**` 작업 시 `@docs/DevOps/Backend/FASTAPI_RULES.md`

## 에이전트 지시

1. **라우트(`main` / routers)** — HTTP만. Controller 인스턴스(또는 DI) 호출 후 응답 반환. CSV·joblib·DB 직접 접근 금지.
2. **Controller** — `self.service = ...` 보유. 메서드는 service(또는 reader/model)에 **한 줄 위임**.
3. **Service** — reader·model 조합. 유스케이스당 메서드 하나.
4. **Reader / Model** — I/O·추론만. 경로는 `Path(__file__).resolve().parent` 기준.

## 참조 구현

- `backend/main.py` — 라우트
- `backend/apps/titanic/app/james_controller.py` → `jack_service.py` → `walter_reader.py` / `rose_model.py`

## 스타일

- 짧은 파일, 얇은 메서드. 비슷한 이름의 헬퍼 체인을 쌓지 않는다.
- 데이터 접근 로직을 상위 계층에 복제하지 않는다.

## 로컬 개발 서버

- **에이전트는 `python run.py` / uvicorn을 자동 실행하지 않는다.** 사용자가 `backend`에서 직접 실행한다.
- 기본 포트: **8000** (`backend/run.py`). 프론트 프록시: `frontend/next.config.mjs` → `127.0.0.1:8000`.
