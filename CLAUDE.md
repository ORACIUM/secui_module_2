# CLAUDE.md

이 파일은 Claude Code (claude.ai/code)가 이 저장소의 코드를 작업할 때 참고할 가이드를 제공합니다.

## 프로젝트 개요

이것은 실시간으로 서버 리소스를 수집하고 모니터링하는 시스템 리소스 메트릭 모니터링 시스템입니다. 이 시스템은 CPU, 메모리, 디스크, 네트워크 메트릭을 추적하여 시스템 상태를 파악하고 잠재적 문제를 사전에 감지합니다.

## 기술 스택

### Frontend
- **프레임워크**: Vue 3
- **메타 프레임워크**: Nuxt 3
- **상태 관리**: Pinia (Nuxt 3 권장)
- **UI 라이브러리**: 필요에 따라 선택 (예: Vuetify, Element Plus)

### Backend
- **언어**: Python 3.11+
- **웹 프레임워크**: FastAPI
- **ASGI 서버**: Uvicorn
- **비동기 처리**: asyncio, aiohttp
- **데이터 검증**: Pydantic

### Database
- **주 데이터베이스**: SQLite
- **ORM**: SQLAlchemy (비동기 지원)
- **마이그레이션**: Alembic

### 통신 프로토콜
- **API 스타일**: RESTful API
- **직렬화**: Protocol Buffers (protobuf)
- **실시간 통신**: WebSocket (protobuf 메시지 사용)
- **HTTP 클라이언트**: axios (Frontend), httpx (Backend)

### 메트릭 수집
- **시스템 메트릭**: psutil (크로스 플랫폼)
- **네트워크 모니터링**: psutil.net_io_counters

### 추가 도구
- **코드 품질**:
  - Frontend: ESLint, Prettier
  - Backend: Black, Flake8, mypy
- **테스팅**:
  - Frontend: Vitest, Vue Test Utils
  - Backend: pytest, pytest-asyncio
- **API 문서**: FastAPI 자동 생성 (Swagger UI, ReDoc)
- **프로토콜 버퍼 컴파일**: protoc, protobuf-compiler

## 프로젝트 구조

```
module_3/
├── backend/                    # FastAPI 백엔드
│   ├── src/
│   │   ├── agent/             # 메트릭 수집 에이전트
│   │   │   ├── main.py        # 에이전트 엔트리포인트
│   │   │   ├── collectors/    # OS별 메트릭 수집기
│   │   │   │   ├── cpu.py
│   │   │   │   ├── memory.py
│   │   │   │   ├── disk.py
│   │   │   │   └── network.py
│   │   │   └── buffer.py      # 로컬 버퍼링
│   │   ├── server/            # 메트릭 수집 서버
│   │   │   ├── main.py        # FastAPI 앱
│   │   │   ├── api/           # API 라우터
│   │   │   │   ├── metrics.py
│   │   │   │   └── alerts.py
│   │   │   ├── models/        # SQLAlchemy 모델
│   │   │   ├── schemas/       # Pydantic 스키마
│   │   │   └── websocket.py   # WebSocket 핸들러
│   │   ├── alerts/            # 알림 엔진
│   │   │   ├── engine.py
│   │   │   └── channels/      # 알림 채널
│   │   ├── protos/            # 컴파일된 protobuf (생성됨)
│   │   └── database/          # DB 설정 및 마이그레이션
│   ├── tests/                 # pytest 테스트
│   ├── config/                # 설정 파일
│   └── requirements.txt       # Python 의존성
│
├── frontend/                   # Nuxt 3 프론트엔드
│   ├── pages/                 # Nuxt 페이지 (라우팅)
│   │   ├── index.vue          # 대시보드 홈
│   │   ├── metrics.vue        # 메트릭 상세
│   │   └── alerts.vue         # 알림 관리
│   ├── components/            # Vue 컴포넌트
│   │   ├── charts/            # 차트 컴포넌트
│   │   ├── MetricCard.vue
│   │   └── AlertList.vue
│   ├── composables/           # Vue Composables
│   │   ├── useMetrics.ts      # 메트릭 데이터 관리
│   │   └── useWebSocket.ts    # WebSocket 연결
│   ├── stores/                # Pinia 스토어
│   ├── protos/                # 컴파일된 protobuf (생성됨)
│   ├── nuxt.config.ts         # Nuxt 설정
│   └── package.json           # NPM 의존성
│
├── proto/                      # Protocol Buffer 정의
│   ├── metrics.proto          # 메트릭 메시지 정의
│   └── alerts.proto           # 알림 메시지 정의
│
├── config/                     # 공유 설정 파일
│   ├── agent.yml              # 에이전트 설정
│   └── alerts.yml             # 알림 설정
│
├── docs/                       # 문서
└── CLAUDE.md                   # 프로젝트 가이드
```

## 아키텍처

시스템은 다층 아키텍처를 따릅니다:

```
[모니터링 대상 서버]
  └─> [메트릭 수집 에이전트] (Python + psutil)
        ├─ 경량: <50MB RAM, <5% CPU
        └─ 수집: CPU, 메모리, 디스크, 네트워크
              │
              ▼ [RESTful API + Protocol Buffers]
              │
        [FastAPI 백엔드 서버]
              ├─> [SQLite 데이터베이스]
              │     └─ 메트릭 데이터 저장/집계
              ├─> [알림 엔진]
              │     └─ 임계값 기반 알림 (Slack, Email, SMS)
              └─> [REST API]
                    ├─ Protocol Buffers 직렬화
                    └─ WebSocket 실시간 스트리밍
                          │
                          ▼ [HTTP + Protobuf]
                          │
                    [Nuxt 3 웹 대시보드] (Vue 3)
                          └─ 실시간 메트릭 시각화
```

### 주요 컴포넌트

**에이전트 계층** (`src/agent/`):
- 5초마다 시스템 메트릭 수집 (설정 가능)
- 크로스 플랫폼 지원 (Linux, Windows, macOS)
- 메트릭 수집을 위한 OS별 추상화 계층 구현
- 네트워크 장애 시 재시도 로직을 포함한 로컬 버퍼링
- 성능 목표: <5% CPU, <50MB RAM

**서버 계층** (`src/server/`):
- 여러 에이전트로부터 메트릭 수집 처리 (1,000개 이상의 서버)
- 데이터 집계 및 보존 정책 구현:
  - 원시 데이터: 7일
  - 1분 집계: 30일
  - 1시간 집계: 1년
- 수평 확장 가능한 아키텍처

**알림 엔진** (`src/alerts/`):
- 설정 가능한 규칙을 가진 임계값 기반 알림
- 기본 임계값:
  - CPU: 80% 경고, 90% 위험
  - 메모리: 85% 경고, 95% 위험
  - 디스크: 80% 경고, 90% 위험
  - 디스크 I/O 대기: >100ms 경고
- 중복 제거 로직 (5분 윈도우)
- 다중 채널 알림 (이메일, Slack, Discord, SMS)

**API 계층** (`src/api/`):
- 메트릭 쿼리 및 알림 설정을 위한 RESTful 엔드포인트
- 실시간 메트릭 스트리밍을 위한 WebSocket 지원
- RBAC를 포함한 JWT 기반 인증
- 성능 목표: <100ms 응답 시간 (P95)

## 개발 명령어

### 설정
```bash
# Backend 의존성 설치
cd backend
pip install -r requirements.txt

# Frontend 의존성 설치
cd frontend
npm install

# Protocol Buffers 컴파일
protoc --python_out=./backend/src/protos --js_out=import_style=commonjs:./frontend/protos proto/*.proto
```

### 에이전트 실행
```bash
# 메트릭 수집 에이전트 시작
python src/agent/main.py

# 커스텀 설정으로 시작
python src/agent/main.py --config config/agent.yml --interval 10
```

### Backend 서버 실행
```bash
# FastAPI 서버 시작 (개발 모드)
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 또는 프로덕션 모드
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend 대시보드 실행
```bash
# Nuxt 3 개발 서버 시작
cd frontend
npm run dev

# 프로덕션 빌드
npm run build
npm run preview
```

### 전체 스택 실행
```bash
# Backend + Frontend 동시 실행 (개발 모드)
# Terminal 1: Backend
cd backend && uvicorn src.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Agent (선택사항)
python src/agent/main.py
```

### 테스팅
```bash
# Backend 테스트
cd backend
pytest                              # 모든 테스트 실행
pytest tests/unit                   # 유닛 테스트만
pytest tests/integration            # 통합 테스트
pytest tests/test_agent.py -v      # 특정 테스트 파일

# Frontend 테스트
cd frontend
npm run test                        # 모든 테스트 실행
npm run test:unit                   # 유닛 테스트만
npm run test:e2e                    # E2E 테스트
```

### 린팅 및 포매팅
```bash
# Backend
cd backend
black .                             # 코드 포매팅
flake8 src tests                    # 린팅
mypy src                            # 타입 체크

# Frontend
cd frontend
npm run lint                        # ESLint
npm run format                      # Prettier
```

### Protocol Buffers
```bash
# .proto 파일 컴파일
# Backend용 Python 코드 생성
protoc --python_out=./backend/src/protos proto/metrics.proto

# Frontend용 JavaScript 코드 생성
protoc --js_out=import_style=commonjs:./frontend/protos proto/metrics.proto

# 또는 스크립트 사용
npm run proto:compile               # 자동으로 양쪽 컴파일
```

## 메트릭 수집 세부사항

### CPU 메트릭
- 전체 사용량 (user, system, idle, iowait)
- 코어별 사용률
- 로드 평균 (1분, 5분, 15분)
- CPU별 상위 N개 프로세스

### 메모리 메트릭
- 물리 메모리 (전체, 사용, 가용, 퍼센트)
- 스왑 메모리 (전체, 사용, swap in/out 속도)
- 버퍼/캐시 메모리
- 프로세스별 메모리 사용량

### 디스크 메트릭
- 파티션 사용량 (전체, 사용, 여유, 퍼센트)
- Inode 사용량
- I/O 작업 (read/write MB/s, IOPS)
- I/O 대기 시간 및 큐 길이

### 네트워크 메트릭
- 인터페이스별 트래픽 (bytes/s, packets/s)
- 인바운드/아웃바운드 처리량
- 에러 및 드롭된 패킷
- 연결 상태 (established, time_wait)
- 대역폭 사용률 퍼센트

## 설정

### 에이전트 설정 (`config/agent.yml`)
```yaml
interval: 5                              # 수집 간격 (초)
server_url: http://localhost:8000        # FastAPI 서버 URL
retry_attempts: 3
retry_delay: 5                           # 재시도 간격 (초)
buffer_size: 1000                        # 오프라인 모드용 로컬 버퍼
use_protobuf: true                       # Protocol Buffers 사용 여부
timeout: 10                              # 요청 타임아웃 (초)
```

### 알림 설정 (`config/alerts.yml`)
```yaml
thresholds:
  cpu: { warning: 80, critical: 90 }
  memory: { warning: 85, critical: 95 }
  disk: { warning: 80, critical: 90 }
  disk_io_wait: { warning: 100 }         # ms

deduplication_window: 300                # 중복 제거 윈도우 (초)

channels:
  - type: slack
    webhook: <webhook_url>
    enabled: true
  - type: email
    smtp_host: smtp.gmail.com
    smtp_port: 587
    recipients: [admin@example.com]
    enabled: false
  - type: discord
    webhook: <discord_webhook_url>
    enabled: false
```

### Backend 설정 (`backend/src/config.py`)
```python
class Settings:
    # Server
    HOST = "0.0.0.0"
    PORT = 8000

    # Database
    DATABASE_URL = "sqlite:///./metrics.db"

    # Protocol Buffers
    USE_PROTOBUF = True

    # Data Retention (days)
    RAW_DATA_RETENTION = 7
    AGGREGATED_1MIN_RETENTION = 30
    AGGREGATED_1HOUR_RETENTION = 365

    # WebSocket
    WS_HEARTBEAT_INTERVAL = 30
```

### Frontend 설정 (`frontend/nuxt.config.ts`)
```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000',
      wsUrl: process.env.WS_URL || 'ws://localhost:8000/ws',
      useProtobuf: true
    }
  }
})
```

## 성능 요구사항

- 메트릭 수집 주기: ≤5초
- 데이터 수집 성공률: ≥99.9%
- 알림 지연 시간: ≤10초
- 에이전트 오버헤드: <5% CPU
- 서버 처리량: ≥10,000 메트릭/초
- API 응답 시간: <100ms (P95)

## 보안 고려사항

- 모든 API 엔드포인트는 JWT 인증 필요
- 모든 통신에 HTTPS/TLS 사용
- 저장된 메트릭 데이터의 선택적 암호화
- 대시보드 및 API 액세스를 위한 RBAC
- 민감한 데이터는 로깅하거나 저장하지 않음

## 구현 단계

프로젝트는 5단계로 나뉩니다 (자세한 내용은 `docs/system-resource-metrics-prd.md` 참조):
1. **1단계**: CLI 출력을 포함한 기본 메트릭 수집
2. **2단계**: 데이터베이스 통합 및 REST API
3. **3단계**: 알림을 포함한 알림 시스템
4. **4단계**: 시각화를 포함한 웹 대시보드
5. **5단계**: 고급 기능 (WebSocket, 커스텀 대시보드, 최적화)

## 주요 설계 결정사항

### 아키텍처 설계
- **크로스 플랫폼 추상화**: 통합 인터페이스를 가진 플랫폼별 수집기 사용
- **데이터 보존 전략**: 스토리지와 쿼리 성능의 균형을 위한 다층 집계
- **알림 중복 제거**: 알림 스팸을 방지하기 위한 5분 윈도우
- **로컬 버퍼링**: 데이터 손실을 방지하기 위해 네트워크 장애 시 에이전트가 메트릭 버퍼링
- **수평 확장**: 로드 밸런서 뒤의 여러 인스턴스를 위해 설계된 서버 계층

### 기술 스택 선택 이유
- **Vue 3 + Nuxt**: 반응형 UI, SSR 지원, 우수한 개발자 경험, 컴포넌트 기반 아키텍처
- **FastAPI**: 고성능 비동기 처리, 자동 API 문서 생성, Pydantic 기반 데이터 검증, Python 생태계 활용
- **SQLite**: 제로 설정, 임베디드 데이터베이스, 단일 파일 관리, 충분한 성능 (1,000 서버 규모)
- **Protocol Buffers**: 효율적인 바이너리 직렬화, 강력한 타입 시스템, 언어 중립적, JSON 대비 빠른 성능과 작은 페이로드 크기
- **psutil**: 크로스 플랫폼 시스템 모니터링, Python 네이티브, 안정적이고 검증된 라이브러리
