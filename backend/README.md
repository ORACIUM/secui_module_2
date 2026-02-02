# System Resource Metrics - Backend

## 설치

### 1. Python 가상환경 생성 및 활성화

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

## 실행

### 에이전트 실행 (CLI 모드)

기본 설정으로 실행 (5초 간격으로 메트릭 수집):
```bash
python -m src.agent.main
```

커스텀 설정 파일 사용:
```bash
python -m src.agent.main --config config/agent.yml
```

수집 간격 변경 (10초):
```bash
python -m src.agent.main --interval 10
```

한 번만 수집하고 종료:
```bash
python -m src.agent.main --once
```

JSON 형식으로 출력:
```bash
python -m src.agent.main --once --format json
```

## 테스트

### 모든 테스트 실행

```bash
pytest
```

### 유닛 테스트만 실행

```bash
pytest tests/unit
```

### 특정 테스트 파일 실행

```bash
pytest tests/unit/test_cpu_collector.py -v
```

### 커버리지 포함 테스트

```bash
pytest --cov=src --cov-report=html
```

### 특정 테스트 함수 실행

```bash
pytest tests/unit/test_cpu_collector.py::test_collect_cpu_metrics -v
```

## 코드 품질

### 코드 포매팅 (Black)

```bash
black src tests
```

### 린팅 (Flake8)

```bash
flake8 src tests
```

### 타입 체크 (mypy)

```bash
mypy src
```

## 프로젝트 구조

```
backend/
├── src/
│   └── agent/
│       ├── __init__.py
│       ├── main.py              # 메인 엔트리포인트
│       ├── config_loader.py     # 설정 로더
│       ├── formatter.py         # 출력 포맷터
│       └── collectors/          # 메트릭 수집기
│           ├── __init__.py
│           ├── cpu.py
│           ├── memory.py
│           ├── disk.py
│           └── network.py
├── tests/
│   └── unit/                    # 유닛 테스트
│       ├── test_cpu_collector.py
│       ├── test_memory_collector.py
│       ├── test_disk_collector.py
│       ├── test_network_collector.py
│       └── test_config_loader.py
├── config/
│   └── agent.yml                # 에이전트 설정
├── requirements.txt
├── pytest.ini
└── README.md
```

## 설정 파일 (config/agent.yml)

```yaml
# 메트릭 수집 간격 (초)
interval: 5

# 서버 URL (Phase 2에서 사용)
server_url: http://localhost:8000

# 재시도 설정
retry_attempts: 3
retry_delay: 5

# 로컬 버퍼 크기
buffer_size: 1000

# 로깅 설정
log_level: INFO
log_file: agent.log

# 수집기 활성화/비활성화
collectors:
  cpu: true
  memory: true
  disk: true
  network: true

# 상위 프로세스 개수
top_processes_limit: 5
```

## 수집되는 메트릭

### CPU
- 전체 CPU 사용률
- 코어별 CPU 사용률
- CPU 시간 (user, system, idle, iowait)
- 로드 평균 (1분, 5분, 15분)
- CPU 주파수
- 상위 CPU 사용 프로세스

### Memory
- 물리 메모리 (전체, 사용, 가용, 여유, 퍼센트)
- 버퍼/캐시 메모리
- 스왑 메모리
- 상위 메모리 사용 프로세스

### Disk
- 파티션별 사용량
- 디스크 I/O 통계 (읽기/쓰기 바이트, 작업 수)
- IOPS 계산 기능

### Network
- 인터페이스별 트래픽 (송수신 바이트, 패킷)
- 에러 및 드롭 패킷
- 네트워크 연결 상태
- 대역폭 계산 기능

## 트러블슈팅

### Windows에서 로드 평균이 None으로 표시됨
- Windows는 로드 평균을 지원하지 않습니다. 이는 정상입니다.

### 네트워크 연결 정보가 None으로 표시됨
- 네트워크 연결 정보 수집은 관리자 권한이 필요할 수 있습니다.
- Windows: 관리자 권한으로 실행
- Linux: sudo로 실행하거나 CAP_NET_ADMIN 권한 부여

### 특정 디스크 파티션이 표시되지 않음
- 접근 권한이 없는 파티션은 자동으로 건너뜁니다.
