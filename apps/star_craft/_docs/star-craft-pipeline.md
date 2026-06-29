---
type: hub
title: StarCraft 허브 — Graph DB / Vector DB 파이프라인 전략
links: [star_topology, hexagonal_architecture, docker_compose]
---

# StarCraft 허브 파이프라인 전략

## 1. 왜 star_craft가 허브인가

스타 토폴로지에서 허브는 **스포크 간 직접 의존을 차단**하는 교환기다.
`titanic`, `friday13th`, `sports` 등 각 스포크 모듈이 서로 데이터를 주고받으려면
반드시 `star_craft`를 경유해야 한다.

```
spoke A ──→ star_craft (hub) ──→ spoke B   ✅
spoke A ──────────────────────→ spoke B   ❌
```

허브가 두 DB를 소유하는 이유:
- **Graph DB** — 스포크 간 관계(엔티티 연결, 컨텍스트 라우팅)를 저장
- **Vector DB** — 스포크가 생성한 임베딩을 중앙 인덱싱, 의미 검색 제공

---

## 2. DB 선택

| 역할 | 선택 | 이유 |
|------|------|------|
| Graph DB | **Neo4j 5** | Cypher 쿼리, Docker 이미지 안정적, Python 드라이버(`neo4j`) 성숙 |
| Vector DB | **Qdrant** | 경량 Docker, 비동기 Python 클라이언트, REST + gRPC 지원 |

---

## 3. 헥사고날 아키텍처에서의 위치

```
star_craft/
├── domain/
│   ├── entities/          ← KnowledgeNode, Relation, EmbeddingRecord
│   └── value_objects/     ← NodeId, Vector, RelationType
│
├── app/
│   ├── ports/
│   │   ├── input/         ← IKnowledgeQueryUseCase, IIndexUseCase
│   │   └── output/        ← IGraphRepository, IVectorRepository   ← 인터페이스 정의
│   └── use_cases/         ← 검색·라우팅 로직 (DB 구현 모름)
│
└── adapter/
    └── outbound/
        ├── client/        ← Neo4jClient, QdrantClient (연결 설정)
        └── repositories/  ← Neo4jGraphRepository, QdrantVectorRepository
                              (IGraphRepository, IVectorRepository 구현)
```

**핵심 원칙:** use_cases는 포트(인터페이스)만 알고, 실제 Neo4j/Qdrant는 adapter 계층에만 존재한다.
DB를 교체해도 도메인·유스케이스 코드는 변경되지 않는다.

---

## 4. Docker Compose 추가 전략

현재 `docker-compose.yaml`에 `api`, `web`, `n8n`이 있다.
아래 두 서비스를 추가한다.

```yaml
  # Graph DB
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"   # Browser UI
      - "7687:7687"   # Bolt 프로토콜 (Python 드라이버 연결)
    environment:
      - NEO4J_AUTH=neo4j/password   # .env로 분리 권장
    volumes:
      - neo4j_data:/data

  # Vector DB
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  neo4j_data:
  qdrant_data:
```

`api` 서비스의 `depends_on`에 `neo4j`, `qdrant` 추가 필요.

---

## 5. 데이터 파이프라인 흐름

### 5-1. 인덱싱 파이프라인 (스포크 → 허브)

```
Spoke 모듈
  │ 새 엔티티 생성 (예: Titanic 승객 레코드)
  ▼
star_craft IIndexUseCase.index(node)
  ├─→ IGraphRepository.save_node()     → Neo4j (관계 그래프 저장)
  └─→ IVectorRepository.upsert()       → Qdrant (임베딩 저장)
```

임베딩 생성 위치: `star_craft` 유스케이스 내부.
현재는 `core/lol/FakerOrchestrator`(EXAONE) 또는 Ollama embed API 사용 예정.

### 5-2. 검색 파이프라인 (허브 → 스포크 응답)

```
Spoke 모듈 or API 요청
  │ query: "타이타닉 1등실 생존자와 비슷한 사례"
  ▼
star_craft IKnowledgeQueryUseCase.search(query)
  ├─→ IVectorRepository.search()       → Qdrant (의미 유사도 검색)
  └─→ IGraphRepository.find_related()  → Neo4j  (연관 관계 탐색)
  ▼
통합 결과 반환 → 요청 스포크
```

### 5-3. 컨텍스트 라우팅 (허브 고유 역할)

```
외부 쿼리 → star_craft 라우터
  │ Neo4j 그래프로 "어느 스포크가 이 쿼리를 처리할 수 있나" 판단
  ▼
적절한 스포크 UseCase 호출 (star_craft가 fan-out)
```

---

## 6. 연결 설정 전략

### 환경변수 (paik/.env)

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

QDRANT_HOST=localhost
QDRANT_PORT=6333
```

Docker 컨테이너 내부에서는 `localhost` → 서비스명으로 교체:
- `bolt://neo4j:7687`
- `qdrant:6333`

### 클라이언트 위치

```
adapter/outbound/client/
  ├── neo4j_client.py     ← neo4j.AsyncGraphDatabase.driver() 래핑
  └── qdrant_client.py    ← qdrant_client.AsyncQdrantClient() 래핑
```

FastAPI 앱 시작 시 lifespan으로 연결 초기화, 종료 시 close.

---

## 7. 구현 순서 (단계별)

```
1. docker-compose.yaml에 neo4j, qdrant 서비스 추가
   검증: docker compose up → 두 서비스 healthy

2. domain/entities/ — KnowledgeNode, Relation 정의
   검증: import 에러 없음

3. app/ports/output/ — IGraphRepository, IVectorRepository 인터페이스 정의
   검증: 메서드 시그니처 합의

4. adapter/outbound/client/ — Neo4jClient, QdrantClient 구현
   검증: 각 DB에 ping 성공

5. adapter/outbound/repositories/ — 인터페이스 구현체 작성
   검증: 단순 save/find 테스트 통과

6. app/use_cases/ — 인덱싱·검색 유스케이스 구현
   검증: Titanic 샘플 데이터로 end-to-end 파이프라인 동작 확인
```

---

## 8. 의존성 추가 (requirements.txt)

```
neo4j==5.x.x          # Neo4j 공식 비동기 드라이버
qdrant-client==1.x.x  # Qdrant 비동기 클라이언트
```

현재 `ollama==0.6.2`는 임베딩 생성에 재활용 가능 (`ollama.embeddings()`).
외부 임베딩 API 없이 로컬 EXAONE으로 벡터 생성 가능.
