# CLAUDE.md

이 파일은 Claude Code (claude.ai/code)가 이 저장소의 코드를 작업할 때 참고할 가이드를 제공합니다.

## 프로젝트 개요

이것은 실시간으로 서버 리소스를 수집하고 모니터링하는 시스템 리소스 메트릭 모니터링 시스템입니다. 이 시스템은 CPU, 메모리, 디스크, 네트워크 메트릭을 추적하여 시스템 상태를 파악하고 잠재적 문제를 사전에 감지합니다.

## 아키텍처

시스템은 다층 아키텍처를 따릅니다:

```
[서버]
  └─> [메트릭 수집 에이전트] (경량, <50MB RAM, <5% CPU)
        └─> [데이터 전송] (HTTP/gRPC)
              └─> [메트릭 수집 서버]
                    ├─> [시계열 DB] (InfluxDB/Prometheus/TimescaleDB)
                    ├─> [알림 엔진] (임계값 기반 알림)
                    └─> [API 서버] (REST + WebSocket)
                          └─> [웹 대시보드] (실시간 시각화)
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
# 의존성 설치 (구현에 따라 선택)
npm install         # Node.js용
pip install -r requirements.txt  # Python용
go mod download     # Go용
```

### 에이전트 실행
```bash
# 메트릭 수집 에이전트 시작
npm run agent       # 또는: python src/agent/main.py
# 커스텀 설정으로 시작
npm run agent -- --config config/agent.yml --interval 10
```

### 서버 실행
```bash
# 메트릭 수집 서버 시작
npm run server      # 또는: python src/server/main.py
# 데이터베이스와 함께 시작
docker-compose up -d  # 시계열 DB 시작
npm run server
```

### 대시보드 실행
```bash
# 웹 대시보드 시작
npm run dashboard   # 또는: cd src/dashboard && npm run dev
```

### 테스팅
```bash
# 모든 테스트 실행
npm test            # 또는: pytest
# 유닛 테스트만 실행
npm run test:unit
# 통합 테스트 실행
npm run test:integration
# 성능 테스트 실행
npm run test:perf
# 특정 테스트 파일 실행
npm test -- src/agent/cpu.test.js
```

### 린팅 및 포매팅
```bash
npm run lint        # 또는: flake8 / golangci-lint run
npm run format      # 또는: black . / gofmt
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

에이전트 설정 (`config/agent.yml`):
```yaml
interval: 5           # 수집 간격 (초)
server_url: http://localhost:8080
retry_attempts: 3
buffer_size: 1000     # 오프라인 모드용 로컬 버퍼
```

알림 설정 (`config/alerts.yml`):
```yaml
thresholds:
  cpu: { warning: 80, critical: 90 }
  memory: { warning: 85, critical: 95 }
  disk: { warning: 80, critical: 90 }
channels:
  - type: slack
    webhook: <webhook_url>
  - type: email
    recipients: [admin@example.com]
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

- **크로스 플랫폼 추상화**: 통합 인터페이스를 가진 플랫폼별 수집기 사용
- **데이터 보존 전략**: 스토리지와 쿼리 성능의 균형을 위한 다층 집계
- **알림 중복 제거**: 알림 스팸을 방지하기 위한 5분 윈도우
- **로컬 버퍼링**: 데이터 손실을 방지하기 위해 네트워크 장애 시 에이전트가 메트릭 버퍼링
- **수평 확장**: 로드 밸런서 뒤의 여러 인스턴스를 위해 설계된 서버 계층
