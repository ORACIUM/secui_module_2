---
name: code-quality
description: 코드 품질 도구를 실행하여 린팅, 포매팅, 타입 체크를 수행합니다
version: 1.0.0
---

# Code Quality Skill

프로젝트의 코드 품질을 자동으로 검사하고 개선합니다. Black, Flake8, mypy 등의 도구를 실행하여 일관된 코드 스타일과 품질을 유지합니다.

## When to Use

- 사용자가 "코드 품질 체크", "린팅", "포매팅" 등을 요청할 때
- 커밋 전 코드 스타일 검증 필요 시
- Pull Request 생성 전 최종 점검 시
- 새로운 코드 작성 후 스타일 통일 필요 시
- CI/CD 파이프라인 실패 원인 확인 시

## What It Does

1. **Black**: 자동 코드 포매팅
2. **Flake8**: 린팅 (PEP 8, 코드 복잡도, 잠재적 오류)
3. **mypy**: 정적 타입 체크
4. **isort**: import 문 정렬 (선택적)
5. 발견된 이슈 분석 및 수정 방안 제시

## Steps

### Step 1: 도구 설치 확인
```bash
# 필요한 도구가 설치되어 있는지 확인
pip list | grep -E "black|flake8|mypy"

# 없다면 설치
pip install black flake8 mypy isort
```

### Step 2: Black (자동 포매팅)
```bash
# 전체 프로젝트 포매팅
black src tests

# 체크만 (변경 없이)
black --check src tests

# diff 보기
black --diff src tests

# 특정 디렉토리만
black src/agent/
```

### Step 3: Flake8 (린팅)
```bash
# 전체 프로젝트 린팅
flake8 src tests

# 특정 규칙 무시
flake8 src tests --ignore=E203,W503

# 최대 라인 길이 설정
flake8 src tests --max-line-length=100

# 복잡도 체크
flake8 src tests --max-complexity=10
```

### Step 4: mypy (타입 체크)
```bash
# 전체 프로젝트 타입 체크
mypy src

# 엄격 모드
mypy --strict src

# HTML 리포트 생성
mypy src --html-report mypy-report
```

### Step 5: isort (import 정렬) - Optional
```bash
# import 정렬
isort src tests

# 체크만
isort --check-only src tests

# diff 보기
isort --diff src tests
```

### Step 6: 결과 분석
모든 도구의 출력을 통합하여 분석하고, 우선순위별로 정리합니다.

## Output Format

```markdown
# Code Quality Report

## 📊 Overall Status
- **Black**: ✅ Formatted (X files changed) / ❌ Needs formatting
- **Flake8**: ✅ Clean / ⚠️ Y issues found
- **mypy**: ✅ Type safe / ⚠️ Z type errors
- **isort**: ✅ Organized / ❌ Needs sorting

## 🎨 Black (Code Formatting)

### Status: ✅ All files formatted

Changed files:
1. `src/agent/main.py` (2 changes)
2. `src/agent/collectors/cpu.py` (5 changes)

### Status: ❌ Formatting needed

Files to format:
1. `src/agent/config_loader.py`
   - Line 23: Long line
   - Line 45: Inconsistent spacing

**Action**: Run `black src tests` to auto-format

## 🔍 Flake8 (Linting)

### Status: ⚠️ 12 issues found

#### Critical Issues (0)
(none)

#### Important Issues (5)

**1. src/agent/main.py:45:1 - E501**
```
Line too long (92 > 88 characters)
```
**Fix**: Break into multiple lines or adjust max-line-length

**2. src/agent/collectors/cpu.py:78:5 - F841**
```
Local variable 'result' is assigned but never used
```
**Fix**: Remove unused variable or use it

**3. src/agent/collectors/memory.py:23:1 - C901**
```
'collect_memory_metrics' is too complex (11)
```
**Fix**: Refactor function to reduce complexity

[더 많은 이슈들...]

#### Minor Issues (7)

**1. src/agent/formatter.py:12:1 - W293**
```
Blank line contains whitespace
```
**Fix**: Remove trailing whitespace

[더 많은 이슈들...]

## 🔤 mypy (Type Checking)

### Status: ⚠️ 8 type errors

**1. src/agent/main.py:34**
```python
error: Argument 1 to "process_metrics" has incompatible type "Dict[str, Any]"; expected "MetricsData"
```
**Fix**:
```python
# Before
def process_metrics(data: MetricsData) -> None:
    ...

metrics: Dict[str, Any] = collect_metrics()
process_metrics(metrics)  # Type error

# After
from typing import cast

metrics: Dict[str, Any] = collect_metrics()
process_metrics(cast(MetricsData, metrics))  # or proper type conversion
```

**2. src/agent/collectors/cpu.py:56**
```python
error: Function is missing a return type annotation
```
**Fix**:
```python
# Before
def get_cpu_usage():
    return psutil.cpu_percent()

# After
def get_cpu_usage() -> float:
    return psutil.cpu_percent()
```

[더 많은 타입 에러들...]

## 📦 isort (Import Organization)

### Status: ❌ Needs sorting

Files with unsorted imports:
1. `src/agent/main.py`
2. `src/agent/config_loader.py`

**Example** (src/agent/main.py):
```python
# Before
import sys
import psutil
from typing import Dict, Any
import yaml
from .collectors import cpu, memory

# After (Standard > Third-party > Local)
import sys
from typing import Dict, Any

import psutil
import yaml

from .collectors import cpu, memory
```

**Action**: Run `isort src tests`

## 🎯 Priority Action Items

### 🔴 Must Fix (Before Commit)
1. [ ] Remove unused variable in `cpu.py:78`
2. [ ] Fix type error in `main.py:34`
3. [ ] Reduce complexity of `memory.py:23` (McCabe complexity: 11 → <10)

### 🟡 Should Fix (This Week)
1. [ ] Add type hints to all public functions
2. [ ] Break long lines (>88 chars)
3. [ ] Sort imports with isort

### 🟢 Nice to Have
1. [ ] Add docstrings to missing functions
2. [ ] Remove trailing whitespaces
3. [ ] Organize imports consistently

## 🔧 Quick Fix Commands

```bash
# Auto-fix formatting issues
black src tests

# Auto-fix import sorting
isort src tests

# Check before commit
black --check src tests && flake8 src tests && mypy src
```

## 📈 Code Quality Metrics

- **PEP 8 Compliance**: 95% (30/32 files)
- **Type Coverage**: 78% (needs improvement)
- **Average Complexity**: 5.2 (good, <10 recommended)
- **Total Issues**: 12 (3 critical, 5 important, 4 minor)

## 📝 Recommendations

1. **Set up pre-commit hooks** to auto-run these checks
2. **Configure CI/CD** to fail on quality issues
3. **Add .flake8 config** to customize rules
4. **Use strict mypy** in new modules
5. **Document exceptions** when ignoring rules

## ⚙️ Configuration Files

### .flake8 (recommended)
```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
max-complexity = 10
exclude =
    .git,
    __pycache__,
    venv,
    build,
    dist
```

### pyproject.toml (Black, isort, mypy)
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
```
```

## Common Issues and Solutions

### 1. Black vs Flake8 Conflicts
**문제**: Black과 Flake8의 규칙 충돌
**해결**: `.flake8`에서 E203, W503 무시
```ini
[flake8]
extend-ignore = E203, W503
```

### 2. Long Lines
**문제**: E501 - Line too long
**해결**:
```python
# Before
result = some_function(argument1, argument2, argument3, argument4, argument5)

# After
result = some_function(
    argument1,
    argument2,
    argument3,
    argument4,
    argument5,
)
```

### 3. Unused Imports
**문제**: F401 - Module imported but unused
**해결**:
- 실제로 사용하지 않으면 삭제
- `__init__.py`에서 re-export 목적이면 `# noqa: F401` 추가

### 4. Type Errors
**문제**: mypy type mismatches
**해결**:
```python
# Use proper type hints
from typing import Optional, List, Dict

def function(param: Optional[str] = None) -> List[Dict[str, Any]]:
    ...
```

### 5. High Complexity
**문제**: C901 - Function too complex
**해결**:
- 함수를 여러 개의 작은 함수로 분리
- Early return 패턴 사용
- 복잡한 조건문 별도 함수로 추출

## Integration with Development Workflow

### 1. Pre-commit Hook
`.git/hooks/pre-commit`:
```bash
#!/bin/bash
black --check src tests
if [ $? -ne 0 ]; then
    echo "❌ Code formatting check failed. Run: black src tests"
    exit 1
fi

flake8 src tests
if [ $? -ne 0 ]; then
    echo "❌ Linting check failed"
    exit 1
fi

mypy src
if [ $? -ne 0 ]; then
    echo "❌ Type check failed"
    exit 1
fi

echo "✅ All code quality checks passed"
```

### 2. VS Code Settings
`.vscode/settings.json`:
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### 3. CI/CD Pipeline
`.github/workflows/quality.yml`:
```yaml
name: Code Quality
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install black flake8 mypy
      - name: Black
        run: black --check src tests
      - name: Flake8
        run: flake8 src tests
      - name: mypy
        run: mypy src
```

## Best Practices

### Code Formatting
- ✅ **Consistent**: 모든 파일에 동일한 스타일 적용
- ✅ **Automated**: Black 자동 실행 (수동 포매팅 X)
- ✅ **Team agreement**: 팀 전체가 동일한 도구 사용

### Linting
- 🎯 **Focus on important**: Critical 이슈 우선 해결
- 📝 **Document exceptions**: 규칙 무시 시 이유 명시
- 🔄 **Regular checks**: 작업 중 자주 실행

### Type Checking
- 📈 **Gradual adoption**: 새 코드부터 타입 힌팅
- 🎯 **Start simple**: 엄격 모드는 점진적으로
- 📚 **Learn types**: Any 남용 지양, 적절한 타입 사용

## Notes

- 모든 도구는 Python 3.11+ 기준
- Black이 먼저 실행되어야 Flake8 충돌 최소화
- mypy는 프로젝트 크기에 따라 느릴 수 있음
- isort는 Black과 호환되도록 profile="black" 설정
- 레거시 코드는 점진적으로 개선 (한번에 모두 수정 X)
- CI/CD에서 실패하면 로컬에서 먼저 확인
- 코드 품질 도구는 도움일 뿐, 맹목적으로 따르지 말 것
