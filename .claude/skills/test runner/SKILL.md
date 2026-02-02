---
name: test-runner
description: 테스트를 실행하고 결과를 분석하여 개선 제안을 제공합니다
version: 1.0.0
---

# Test Runner Skill

프로젝트의 테스트를 실행하고, 실패한 테스트를 분석하여 문제를 진단하고 해결 방안을 제시합니다.

## When to Use

- 사용자가 "테스트 실행해줘", "test", "pytest 실행" 등을 요청할 때
- 새로운 코드 작성 후 테스트 필요 시
- 버그 수정 후 검증이 필요할 때
- Pull Request 생성 전 최종 확인 시
- CI/CD 파이프라인 실패 원인 분석 시

## What It Does

1. 프로젝트의 테스트 프레임워크 감지 (pytest, unittest, etc.)
2. 적절한 테스트 명령 실행
3. 테스트 결과 분석
4. 실패한 테스트에 대한 상세 진단
5. 해결 방안 제안
6. 커버리지 분석 (선택적)

## Steps

### Step 1: 테스트 환경 확인
```bash
# Python 가상환경 활성화 확인
# 테스트 프레임워크 설치 확인
# 테스트 설정 파일 확인 (pytest.ini, setup.cfg, etc.)
```

### Step 2: 테스트 실행
```bash
# 모든 테스트 실행
pytest

# 특정 디렉토리 테스트
pytest tests/unit/

# 특정 파일 테스트
pytest tests/unit/test_cpu_collector.py

# 특정 테스트 함수
pytest tests/unit/test_cpu_collector.py::test_collect_cpu_metrics

# 상세 출력 모드
pytest -v

# 실패 시 즉시 중단
pytest -x

# 커버리지 포함
pytest --cov=src --cov-report=html
```

### Step 3: 결과 분석
테스트 결과를 다음 관점에서 분석:
- **통과율**: 전체 테스트 중 통과한 비율
- **실패 원인**: AssertionError, Exception, Timeout 등
- **실패 패턴**: 특정 모듈이나 함수에서 반복되는 실패
- **커버리지**: 테스트되지 않은 코드 영역

### Step 4: 문제 진단
실패한 테스트에 대해:
1. 에러 메시지 및 스택 트레이스 분석
2. 테스트 코드 검토
3. 대상 코드 검토
4. 실패 원인 파악 (버그, 테스트 오류, 환경 문제 등)

### Step 5: 해결 방안 제안
- 코드 수정이 필요한 경우: 구체적인 수정 방안
- 테스트 수정이 필요한 경우: 테스트 개선 방안
- 환경 문제인 경우: 설정 또는 의존성 수정
- 추가 테스트가 필요한 경우: 테스트 케이스 제안

## Test Types

### 1. Unit Tests (단위 테스트)
- 개별 함수나 메서드 테스트
- 빠른 실행 속도
- 의존성 mock 처리
```bash
pytest tests/unit/
```

### 2. Integration Tests (통합 테스트)
- 여러 컴포넌트 간 상호작용 테스트
- 데이터베이스, API 등 실제 의존성 사용
```bash
pytest tests/integration/
```

### 3. End-to-End Tests (E2E 테스트)
- 전체 시스템 테스트
- 실제 사용자 시나리오 시뮬레이션
```bash
pytest tests/e2e/
```

## Output Format

```markdown
# Test Report

## 📊 Test Summary
- **Total Tests**: X
- **Passed**: ✅ Y (Z%)
- **Failed**: ❌ A (B%)
- **Skipped**: ⏭️ C
- **Duration**: D seconds

## ✅ Passed Tests
[통과한 테스트 목록]

## ❌ Failed Tests

### Test: test_function_name
**File**: `tests/unit/test_module.py::test_function_name`
**Error Type**: AssertionError
**Error Message**:
```
Expected 5, got 3
```

**Stack Trace**:
```
[스택 트레이스]
```

**Analysis**:
- 원인: [실패 원인 분석]
- 영향: [이 실패가 미치는 영향]

**Recommended Fix**:
```python
# 수정 전
def function():
    return calculate(x, y)

# 수정 후
def function():
    return calculate(x, y) + adjustment
```

**Additional Notes**:
- [추가 고려사항]

[추가 실패 테스트들...]

## 📈 Code Coverage

**Overall Coverage**: X%

### Coverage by Module:
- `src/agent/main.py`: 95%
- `src/agent/collectors/cpu.py`: 100%
- `src/agent/collectors/memory.py`: 85% ⚠️
- `src/agent/config_loader.py`: 90%

### Uncovered Lines:
- `src/agent/collectors/memory.py`: lines 45-50 (에러 핸들링)
- `src/agent/config_loader.py`: lines 30-32 (예외 케이스)

**Recommendations**:
- 메모리 수집기의 예외 처리 경로에 대한 테스트 추가 필요
- config_loader의 엣지 케이스 테스트 보완

## 🎯 Action Items

### Critical (즉시 수정)
1. [ ] Fix: test_memory_collector - 스왑 메모리 계산 오류
2. [ ] Fix: test_network_collector - 네트워크 인터페이스 None 처리

### Important (조만간 수정)
1. [ ] Improve: test_cpu_collector - 멀티코어 환경 테스트 추가
2. [ ] Add: test_config_loader - YAML 파싱 에러 케이스

### Nice to Have (개선 고려)
1. [ ] Refactor: 중복된 fixture 함수 통합
2. [ ] Add: 성능 벤치마크 테스트

## 📝 Next Steps

1. [우선순위 높은 액션 아이템]
2. [그 다음 단계]
```

## Common Test Failures and Solutions

### 1. Import Error
**문제**: `ModuleNotFoundError: No module named 'xxx'`
**원인**: 의존성 미설치 또는 경로 문제
**해결**:
```bash
pip install -r requirements.txt
# 또는
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 2. Assertion Error
**문제**: 예상값과 실제값 불일치
**원인**: 로직 오류, 테스트 데이터 문제
**해결**: 코드 또는 테스트 로직 수정

### 3. Fixture Error
**문제**: `fixture 'xxx' not found`
**원인**: fixture 정의 누락 또는 scope 문제
**해결**: conftest.py에 fixture 정의 또는 import 추가

### 4. Timeout Error
**문제**: 테스트 실행 시간 초과
**원인**: 무한 루프, 느린 외부 호출
**해결**:
```python
@pytest.mark.timeout(5)  # 5초 타임아웃
def test_something():
    ...
```

### 5. Mock/Patch Error
**문제**: mock 객체가 예상대로 동작하지 않음
**원인**: 잘못된 패치 경로 또는 설정
**해결**:
```python
# 올바른 패치 경로 사용
@patch('module.where.used.function')  # 사용되는 위치
# not @patch('module.where.defined.function')  # 정의된 위치 (X)
```

## Best Practices

### Writing Tests
- ✅ **AAA 패턴**: Arrange, Act, Assert
- ✅ **독립성**: 각 테스트는 독립적으로 실행 가능
- ✅ **명확한 이름**: `test_function_should_return_value_when_condition`
- ✅ **하나의 개념**: 한 테스트에서 하나의 개념만 검증
- ✅ **적절한 fixture**: 중복 코드 제거

### Test Coverage
- 🎯 **목표**: 80% 이상 (Critical path는 100%)
- ⚠️ **주의**: 커버리지가 높다고 품질이 보장되는 것은 아님
- 💡 **우선순위**: 비즈니스 로직 > 유틸리티 > UI

### Running Tests
- 🚀 **빠른 피드백**: 자주 실행 (코드 변경 시마다)
- 🔄 **CI/CD**: 자동화된 테스트 실행
- 📊 **커버리지 추적**: 시간 경과에 따른 변화 모니터링

## pytest Options Reference

```bash
# 기본 실행
pytest

# 상세 출력
pytest -v

# 매우 상세한 출력
pytest -vv

# 실패 시 즉시 중단
pytest -x

# 마지막 실패 테스트만
pytest --lf

# 실패 및 그 다음 N개 테스트
pytest --maxfail=3

# 특정 마커만 실행
pytest -m "slow"

# 특정 마커 제외
pytest -m "not slow"

# 병렬 실행 (pytest-xdist)
pytest -n auto

# 커버리지
pytest --cov=src --cov-report=html --cov-report=term

# HTML 리포트
pytest --html=report.html

# 표준 출력 표시
pytest -s

# 경고 표시
pytest -W error
```

## Integration with Development Workflow

### 1. Before Commit
```bash
pytest --cov=src --cov-report=term-missing
```
모든 테스트 통과 및 커버리지 확인

### 2. During Development
```bash
pytest tests/unit/test_current_module.py -v
```
작업 중인 모듈만 빠르게 테스트

### 3. Before PR
```bash
pytest --cov=src --cov-report=html --cov-report=term
```
전체 테스트 및 상세 커버리지 리포트

### 4. CI/CD Pipeline
```bash
pytest --junitxml=test-results.xml --cov=src --cov-report=xml
```
CI 도구가 파싱할 수 있는 형식으로 출력

## Notes

- 테스트 실행 전 가상환경이 활성화되어 있는지 확인
- 실패한 테스트가 있어도 모든 테스트를 실행하여 전체 상황 파악
- 플래키 테스트 (간헐적 실패)는 별도로 표시하고 우선 수정
- 테스트 데이터는 fixtures나 factories를 사용하여 관리
- 외부 서비스 의존성은 mock 처리
- 테스트는 빠르게 실행되어야 함 (전체 < 5분 권장)
- 커버리지 100%가 목표가 아님, 중요한 코드 경로 우선
