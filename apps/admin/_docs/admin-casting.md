# 📺 Admin App: Schema DTO Architecture Specification
### (종목 · 연습 · 광고 운영 부서 구조)

본 문서는 `admin` 애플리케이션의 `adapter/inbound/api/schemas` 패키지 내 **5개 테이블 기반 Schema 명세서**입니다.  
스포츠 미디어 그룹 내부 운영 구조를 직관적으로 파악할 수 있도록  
**[콘텐츠·편성팀]**, **[광고·영업팀]**, **[성과·데이터팀]** 3대 부서 구도로 분류했습니다.

*(참고: 각 테이블당 Schema 클래스 하나로 통합한다. Request/Response 분리 없이 단일 Schema 로 운영한다.)*

---

## ERD 기반 테이블 (admin 모듈 관할)

| 테이블 | 역할 | 현재 schema 파일 | schema 클래스 수 |
|--------|------|-----------------|----------------|
| `sports` | 스포츠 종목 마스터 | `sports_schema.py` | 2 |
| `practices` | 종목별 권장 자세 카탈로그 | `practice_schema.py` | 2 |
| `ads` | 광고·상품 메타데이터 | `ads_schema.py` | 2 |
| `users_ad` | 유저별 광고 계약·집행 (`UK: user_id, ad_id`) | `users_ad_schema.py` | 2 |
| `ad_stats_daily` | 일별 광고 노출·클릭 집계 (`UK: ad_id, stat_date`) | `ad_stats_daily_schema.py` | 3 |

---

## 1. Content & Programming 그룹 (`content`)
> **Description:** 종목 마스터와 연습 카탈로그를 관리하는 카테고리입니다.  
> 스포츠 플랫폼이 어떤 종목을 다루고 어떤 훈련 콘텐츠를 제공할지 정의하는 **편성 부서**에 해당합니다.

### **content_harris_registrar_schema.py**

- **캐릭터:** 해리스 국장 (Director Harris)
- **현재 클래스:** `SportCreateRequest` in `sports_schema.py`
- **역할 (`keyword`):** `registrar` (신규 등록)
- **ERD 대상 테이블:** `sports`
- **드라마 설정 및 시스템 기능:** 스포츠 네트워크의 종목 등록 총괄 국장. 새로운 종목이 플랫폼에 편입되려면 해리스의 서명이 필요하듯, 유효성 검증(`name`, `description`, `is_active`)을 거쳐 `sports` 카탈로그에 신규 항목을 생성합니다.

### **content_victoria_showcase_schema.py**

- **캐릭터:** 빅토리아 앵커 (Anchor Victoria)
- **현재 클래스:** `SportResponse` in `sports_schema.py`
- **역할 (`keyword`):** `showcase` (편성 목록 제공)
- **ERD 대상 테이블:** `sports`
- **드라마 설정 및 시스템 기능:** 방송국 간판 앵커. 시청자에게 오늘의 종목 편성표를 전달하듯, 등록된 스포츠 데이터(`id`, `name`, `description`, `is_active`, `created_at`)를 API 클라이언트에게 정형화된 형태로 반환합니다.

### **content_diana_curriculum_schema.py**

- **캐릭터:** 다이아나 코디네이터 (Coach Coordinator Diana)
- **현재 클래스:** `PracticeCreateRequest` in `practice_schema.py`
- **역할 (`keyword`):** `curriculum` (훈련 과목 등록)
- **ERD 대상 테이블:** `practices`
- **드라마 설정 및 시스템 기능:** 훈련 커리큘럼 설계자. 어떤 종목(`sports_id`)에서 어떤 자세(`guide_json`)를 가르칠지 커리큘럼을 설계하듯, 연습 항목 신규 등록 데이터(`title`, `description`, `guide_json`, `is_active`)를 검증합니다.

### **content_chen_coach_schema.py**

- **캐릭터:** 천 수석 코치 (Head Coach Chen)
- **현재 클래스:** `PracticeResponse` in `practice_schema.py`
- **역할 (`keyword`):** `coach` (자세 가이드 응답)
- **ERD 대상 테이블:** `practices`
- **드라마 설정 및 시스템 기능:** 현장 해설 수석 코치. 선수에게 가이드를 전달하듯, 연습 항목의 전체 속성(`id`, `sports_id`, `title`, `description`, `guide_json`, `is_active`, `created_at`)을 조회 응답으로 전달합니다.

---

## 2. Commercial & Sales 그룹 (`commercial`)
> **Description:** 광고 상품 메타데이터와 유저별 광고 계약을 관리하는 카테고리입니다.  
> 광고 상품을 기획·발행하고 광고주와의 계약을 체결·관리하는 **광고 영업 부서**에 해당합니다.

### **commercial_draper_creative_schema.py**

- **캐릭터:** 드레이퍼 크리에이티브 디렉터 (Creative Director Draper)
- **현재 클래스:** `AdCreateRequest` in `ads_schema.py`
- **역할 (`keyword`):** `creative` (광고 상품 기획)
- **ERD 대상 테이블:** `ads`
- **드라마 설정 및 시스템 기능:** 광고 캠페인 기획의 거장. 광고 소재와 예산을 정의하듯, 신규 광고 항목(`title`, `target_url`, `image_url`, `budget`, `status`)의 입력 데이터를 검증하여 광고 인벤토리에 등록합니다.

### **commercial_sterling_publisher_schema.py**

- **캐릭터:** 스털링 광고 국장 (Ad Publisher Sterling)
- **현재 클래스:** `AdResponse` in `ads_schema.py`
- **역할 (`keyword`):** `publisher` (광고 상품 조회)
- **ERD 대상 테이블:** `ads`
- **드라마 설정 및 시스템 기능:** 광고 인벤토리 관리 국장. 어떤 광고 상품이 현재 운영 중인지 전달하듯, 광고 상세 정보(`id`, `title`, `image_url`, `target_url`, `budget`, `status`, `created_at`)를 API 응답으로 반환합니다.

### **commercial_grace_broker_schema.py**

- **캐릭터:** 그레이스 계약 브로커 (Contract Broker Grace)
- **현재 클래스:** `UsersAdNestedCreateRequest` in `users_ad_schema.py`
- **역할 (`keyword`):** `broker` (광고 계약 생성 — 중첩 입력)
- **ERD 대상 테이블:** `users_ad` (`UK: user_id, ad_id`)
- **드라마 설정 및 시스템 기능:** 광고주와 플랫폼 사이를 중개하는 브로커. `user_id`는 URL Path 상위 컨텍스트에서 결정되므로, 계약 대상 광고(`ad_id`), 계약 상태, 배정 예산, 기간만 전달하는 **중첩 생성 DTO**입니다.

### **commercial_morgan_account_schema.py**

- **캐릭터:** 모건 어카운트 매니저 (Account Manager Morgan)
- **현재 클래스:** `UsersAdResponse` in `users_ad_schema.py`
- **역할 (`keyword`):** `account` (광고 계약 조회)
- **ERD 대상 테이블:** `users_ad`
- **드라마 설정 및 시스템 기능:** 광고주 계정 담당 매니저. 광고주별 집행 현황을 리포팅하듯, 계약 전체 속성(`id`, `user_id`, `ad_id`, `contract_status`, `allocated_budget`, `started_at`, `ended_at`, `created_at`)을 응답으로 반환합니다.

---

## 3. Analytics & Data 그룹 (`analytics`)
> **Description:** 일별 광고 성과 집계 데이터를 처리하는 카테고리입니다.  
> 광고 노출·클릭을 수집·집계·리포팅하는 **성과 분석 부서**에 해당합니다.  
> `ad_stats_daily` 테이블은 **3-DTO 구조** (중첩 생성 · 단독 생성 · 조회)로 분리됩니다.

### **analytics_parker_fieldlog_schema.py**

- **캐릭터:** 파커 현장 리포터 (Field Reporter Parker)
- **현재 클래스:** `AdStatsDailyNestedCreateRequest` in `ad_stats_daily_schema.py`
- **역할 (`keyword`):** `fieldlog` (현장 단독 집계 입력 — 중첩)
- **ERD 대상 테이블:** `ad_stats_daily`
- **드라마 설정 및 시스템 기능:** 광고 현장의 실시간 리포터. `ad_id`는 URL Path 상위 컨텍스트에서 결정되므로, 날짜(`stat_date`)·노출수(`impressions`)·클릭수(`clicks`)만 현장에서 기록하는 **중첩 생성 DTO**입니다.

### **analytics_wayne_recorder_schema.py**

- **캐릭터:** 웨인 통계 집계관 (Stats Recorder Wayne)
- **현재 클래스:** `AdStatsDailyCreateRequest` in `ad_stats_daily_schema.py`
- **역할 (`keyword`):** `recorder` (전체 통계 단독 입력)
- **ERD 대상 테이블:** `ad_stats_daily` (`UK: ad_id, stat_date`)
- **드라마 설정 및 시스템 기능:** 운영 대시보드에서 직접 `ad_id`를 지정하는 단독 생성 경로를 담당합니다. `ad_id`, `stat_date`, `impressions`, `clicks`를 모두 포함한 **완전 자립형 생성 DTO**입니다.

### **analytics_cole_reporter_schema.py**

- **캐릭터:** 콜 성과 분석관 (Performance Analyst Cole)
- **현재 클래스:** `AdStatsDailyResponse` in `ad_stats_daily_schema.py`
- **역할 (`keyword`):** `reporter` (일별 성과 리포트 응답)
- **ERD 대상 테이블:** `ad_stats_daily`
- **드라마 설정 및 시스템 기능:** 일별 광고 성과 리포터. 경영진에게 KPI를 보고하듯, 집계 결과 전체(`id`, `ad_id`, `stat_date`, `impressions`, `clicks`, `created_at`)를 API 응답으로 반환합니다.
