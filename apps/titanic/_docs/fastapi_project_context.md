# FastAPI 프로젝트 컨텍스트

관련 문서: [[_docs/CLAUDE]] · [[TITANIC_ERD]] · [[FORMA_ERD]]

## 프로젝트 개요
이 프로젝트는 **FastAPI** 기반의 Titanic 데이터 API 서버입니다.
메인 파일명은 **`james.py`** 입니다.

## 기술 스택
- **Framework**: FastAPI
- **Custom Module**: `walter` (Walter 클래스 포함)
- **언어**: Python

---

## 현재 앱 초기화 상태

```python
from fastapi import FastAPI
from walter import Walter

app = FastAPI(title="Titanic API")


class James:
    def __init__(self):
        pass
```

- `app` 은 `FastAPI` 인스턴스이며, 타이틀은 `"Titanic API"` 입니다.
- `Walter` 는 `walter` 모듈에서 임포트하며, 각 엔드포인트 내에서 인스턴스화합니다.
- `James` 클래스는 현재 프로젝트 내에 정의된 커스텀 클래스입니다. (현재 내부 로직 없음)

---

## 등록된 엔드포인트

### `GET /`
- **역할**: 서버 헬스체크 / 루트 응답
- **반환값**:
  ```json
  { "message": "FAST API 초기화 성공" }
  ```

### `GET /data`
- **역할**: Titanic 데이터셋 반환
- **동작**: `Walter()` 인스턴스를 생성하고 `get_data()` 메서드를 호출
- **반환값**:
  ```json
  { "items": [ /* Walter.get_data() 결과 */ ] }
  ```

---

## 코드 전체 (현재 상태)

```python
from fastapi import FastAPI
from walter import Walter

app = FastAPI(title="Titanic API")


class James:
    def __init__(self):
        pass


@app.get("/")
def root():
    return {"message": "FAST API 초기화 성공"}


@app.get("/data")
def data():
    w = Walter()
    return {"items": w.get_data()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("james:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 서버 실행 방법

```bash
# 방법 1 — 직접 실행
python james.py

# 방법 2 — uvicorn CLI
uvicorn james:app --reload --host 127.0.0.1 --port 8000
```

- 진입점 모듈명은 반드시 **`james`** 입니다. (`james:app`)
- 포트는 **8000**, 호스트는 **127.0.0.1** 로 고정되어 있습니다.

---

## Cursor AI를 위한 작업 규칙

1. **파일명은 `james.py`** 입니다. `uvicorn.run()` 의 첫 번째 인자 `"james:app"` 을 변경하지 마세요.
2. **`app` 변수명을 유지**하세요. 다른 이름으로 변경하지 마세요.
3. **`James` 클래스**는 이 파일 안에 정의된 클래스입니다. 삭제하거나 외부 파일로 이동하지 마세요.
4. **`Walter` 클래스**는 `walter` 모듈에서 임포트합니다. 임포트 경로를 변경하지 마세요.
5. **새 엔드포인트 추가** 시 `@app.get()` / `@app.post()` 데코레이터를 사용하고, `if __name__ == "__main__":` 블록 **위에** 작성하세요.
6. **응답 형식**은 딕셔너리(`dict`) 기반 JSON을 기본으로 합니다.
7. 기존 `root()` 와 `data()` 함수는 **수정하지 마세요**.
8. **FastAPI 앱 타이틀**은 `"Titanic API"` 로 고정합니다.

---

## 참고사항
- 이 파일은 `.cursor/rules/fastapi_project_context.md` 경로에 저장하면 Cursor가 자동으로 인식합니다.
- Cursor Rules 기능을 통해 AI가 이 컨텍스트를 항상 참조하게 됩니다.
