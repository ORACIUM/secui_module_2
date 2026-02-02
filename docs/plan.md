# 시스템 리소스 메트릭 모니터링 - 개발 계획

## Phase 1: 기본 메트릭 수집 (2주)

### 환경 설정
- [ ] 프로젝트 디렉토리 구조 생성
- [ ] Python 가상환경 설정
- [ ] 의존성 패키지 설치 (psutil, pyyaml 등)
- [ ] Git 저장소 초기화 및 .gitignore 설정

### 메트릭 수집 에이전트 개발
- [ ] 기본 에이전트 구조 설계 (`src/agent/main.py`)
- [ ] CPU 메트릭 수집기 구현 (`src/agent/collectors/cpu.py`)
  - [ ] 전체 CPU 사용률
  - [ ] 코어별 CPU 사용률
  - [ ] 로드 평균 (1분, 5분, 15분)
- [ ] 메모리 메트릭 수집기 구현 (`src/agent/collectors/memory.py`)
  - [ ] 물리 메모리 정보
  - [ ] 스왑 메모리 정보
  - [ ] 버퍼/캐시 메모리
- [ ] 디스크 메트릭 수집기 구현 (`src/agent/collectors/disk.py`)
  - [ ] 파티션별 디스크 사용량
  - [ ] inode 사용률
  - [ ] 디스크 I/O 통계
- [ ] 네트워크 메트릭 수집기 구현 (`src/agent/collectors/network.py`)
  - [ ] 인터페이스별 트래픽
  - [ ] 에러 및 드롭 패킷
  - [ ] 연결 상태

### 설정 및 출력
- [ ] YAML 설정 파일 로더 구현 (`config/agent.yml`)
- [ ] CLI 출력 포맷 구현
- [ ] 로깅 시스템 구현

### 테스트
- [ ] 단위 테스트 작성 (각 수집기별)
- [ ] 크로스 플랫폼 테스트 (Linux, Windows, macOS)

---

## Phase 2: 데이터 저장 및 API (2주)

### 데이터베이스 설정
- [ ] SQLite 데이터베이스 스키마 설계
- [ ] SQLAlchemy 모델 정의 (`src/server/models/`)
- [ ] Alembic 마이그레이션 설정
- [ ] 데이터베이스 초기화 스크립트

### FastAPI 서버 구현
- [ ] FastAPI 앱 구조 설계 (`src/server/main.py`)
- [ ] 설정 관리 모듈 구현 (`src/server/config.py`)
- [ ] 데이터베이스 연결 관리
- [ ] 비동기 처리 구현

### API 엔드포인트
- [ ] 메트릭 수신 API (`POST /api/metrics`)
- [ ] 현재 메트릭 조회 API (`GET /api/metrics/current`)
- [ ] 히스토리컬 데이터 조회 API (`GET /api/metrics/history`)
  - [ ] 시간 범위 필터링
  - [ ] 메트릭 타입 필터링
  - [ ] 페이지네이션
- [ ] 서버 목록 조회 API (`GET /api/servers`)
- [ ] API 문서 자동 생성 (Swagger UI, ReDoc)

### Protocol Buffers
- [ ] 메트릭 메시지 정의 (`proto/metrics.proto`)
- [ ] protobuf 컴파일 스크립트
- [ ] Python 코드 생성
- [ ] 직렬화/역직렬화 유틸리티

### 에이전트-서버 통신
- [ ] 에이전트에서 서버로 메트릭 전송
- [ ] 재시도 로직 구현
- [ ] 에러 핸들링
- [ ] 네트워크 장애 시 로컬 버퍼링 (`src/agent/buffer.py`)

### 데이터 관리
- [ ] 데이터 집계 로직 (1분, 1시간)
- [ ] 데이터 보관 정책 구현
  - [ ] 원본 데이터: 7일
  - [ ] 1분 집계: 30일
  - [ ] 1시간 집계: 1년
- [ ] 오래된 데이터 자동 삭제 배치 작업

### 테스트
- [ ] API 엔드포인트 통합 테스트
- [ ] 데이터베이스 CRUD 테스트
- [ ] protobuf 직렬화 테스트

---

## Phase 3: 알림 시스템 (1주)

### 알림 엔진 구현
- [ ] 알림 엔진 핵심 로직 (`src/alerts/engine.py`)
- [ ] 임계값 설정 구조 정의
- [ ] 임계값 위반 감지 로직
- [ ] 알림 중복 제거 (5분 윈도우)
- [ ] 알림 우선순위 관리

### 알림 채널
- [ ] 이메일 알림 구현 (`src/alerts/channels/email.py`)
  - [ ] SMTP 설정
  - [ ] HTML 템플릿
- [ ] Slack 웹훅 알림 (`src/alerts/channels/slack.py`)
- [ ] Discord 웹훅 알림 (`src/alerts/channels/discord.py`)
- [ ] SMS 알림 (선택적)

### 알림 설정
- [ ] 알림 설정 파일 (`config/alerts.yml`)
- [ ] 알림 규칙 CRUD API
  - [ ] `GET /api/alerts/rules`
  - [ ] `POST /api/alerts/rules`
  - [ ] `PUT /api/alerts/rules/{id}`
  - [ ] `DELETE /api/alerts/rules/{id}`
- [ ] 알림 히스토리 저장
- [ ] 알림 히스토리 조회 API (`GET /api/alerts/history`)

### 테스트
- [ ] 임계값 감지 로직 테스트
- [ ] 알림 채널 통합 테스트
- [ ] 중복 제거 로직 테스트

---

## Phase 4: 웹 대시보드 (2주)

### Nuxt 3 프로젝트 설정
- [ ] Nuxt 3 프로젝트 초기화 (`frontend/`)
- [ ] TypeScript 설정
- [ ] Pinia 상태 관리 설정
- [ ] UI 라이브러리 선택 및 설치
- [ ] 차트 라이브러리 설치 (Chart.js, ApexCharts 등)

### 페이지 구현
- [ ] 레이아웃 컴포넌트 (`layouts/default.vue`)
- [ ] 대시보드 홈 페이지 (`pages/index.vue`)
  - [ ] 실시간 메트릭 카드
  - [ ] 서버 상태 개요
  - [ ] 최근 알림 목록
- [ ] 메트릭 상세 페이지 (`pages/metrics.vue`)
  - [ ] 시간 범위 선택기
  - [ ] 메트릭 타입 필터
  - [ ] 히스토리컬 차트
- [ ] 알림 관리 페이지 (`pages/alerts.vue`)
  - [ ] 알림 규칙 목록
  - [ ] 알림 규칙 생성/수정
  - [ ] 알림 히스토리

### 컴포넌트 개발
- [ ] 메트릭 카드 컴포넌트 (`components/MetricCard.vue`)
- [ ] 라인 차트 컴포넌트 (`components/charts/LineChart.vue`)
- [ ] 게이지 차트 컴포넌트 (`components/charts/GaugeChart.vue`)
- [ ] 알림 목록 컴포넌트 (`components/AlertList.vue`)
- [ ] 서버 선택 드롭다운 컴포넌트

### Composables
- [ ] 메트릭 데이터 관리 (`composables/useMetrics.ts`)
- [ ] API 호출 유틸리티 (`composables/useApi.ts`)
- [ ] 알림 관리 (`composables/useAlerts.ts`)

### Pinia 스토어
- [ ] 메트릭 스토어 (`stores/metrics.ts`)
- [ ] 알림 스토어 (`stores/alerts.ts`)
- [ ] 서버 스토어 (`stores/servers.ts`)

### API 통합
- [ ] Axios 설정
- [ ] API 클라이언트 구현
- [ ] 에러 핸들링
- [ ] 로딩 상태 관리

### 스타일링
- [ ] 반응형 디자인
- [ ] 다크 모드 지원 (선택적)
- [ ] 애니메이션 및 트랜지션

### 테스트
- [ ] 컴포넌트 단위 테스트 (Vitest)
- [ ] E2E 테스트 (선택적)

---

## Phase 5: 고급 기능 (2주)

### WebSocket 실시간 스트리밍
- [ ] FastAPI WebSocket 엔드포인트 (`src/server/websocket.py`)
- [ ] 메트릭 브로드캐스트 로직
- [ ] 클라이언트 연결 관리
- [ ] Heartbeat 메커니즘
- [ ] protobuf를 사용한 메시지 직렬화

### Frontend WebSocket
- [ ] WebSocket 연결 composable (`composables/useWebSocket.ts`)
- [ ] 자동 재연결 로직
- [ ] 실시간 메트릭 업데이트
- [ ] 연결 상태 표시

### 커스텀 대시보드
- [ ] 위젯 시스템 설계
- [ ] 드래그 앤 드롭 레이아웃
- [ ] 대시보드 템플릿 저장
- [ ] 대시보드 공유 기능

### 성능 최적화
- [ ] 데이터베이스 인덱스 최적화
- [ ] API 응답 캐싱
- [ ] Frontend 코드 스플리팅
- [ ] 이미지 및 에셋 최적화
- [ ] 에이전트 메모리 사용량 최적화

### 보안
- [ ] JWT 기반 인증 구현
- [ ] RBAC (역할 기반 접근 제어)
- [ ] HTTPS/TLS 설정
- [ ] API Rate Limiting
- [ ] CORS 설정

### 배포 준비
- [ ] Docker 이미지 생성
  - [ ] Backend Dockerfile
  - [ ] Frontend Dockerfile
  - [ ] Agent Dockerfile
- [ ] Docker Compose 설정
- [ ] 환경 변수 관리
- [ ] 프로덕션 설정 파일
- [ ] 로깅 및 모니터링 설정

### 문서화
- [ ] API 문서 완성
- [ ] 설치 가이드
- [ ] 사용자 매뉴얼
- [ ] 개발자 가이드
- [ ] 트러블슈팅 가이드

### 최종 테스트
- [ ] 전체 시스템 통합 테스트
- [ ] 성능 테스트 (10,000 메트릭/초)
- [ ] 부하 테스트 (1,000대 서버 시뮬레이션)
- [ ] 보안 테스트
- [ ] 사용자 수용 테스트 (UAT)

---

## 향후 확장 계획

- [ ] 컨테이너 메트릭 (Docker, Kubernetes)
- [ ] 클라우드 리소스 메트릭 (AWS, Azure, GCP)
- [ ] 애플리케이션 성능 메트릭 통합
- [ ] 머신러닝 기반 이상 탐지
- [ ] 자동 스케일링 연동
- [ ] 다국어 지원
- [ ] 모바일 앱 개발
