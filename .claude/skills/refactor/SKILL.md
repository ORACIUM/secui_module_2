---
name: refactor
description: 코드 리팩토링을 체계적으로 계획하고 실행합니다
version: 1.0.0
---

# Refactor Skill

코드의 기능은 유지하면서 구조, 가독성, 성능을 개선하는 리팩토링을 체계적으로 수행합니다.

## When to Use

- 사용자가 "리팩토링해줘", "refactor", "코드 개선" 등을 요청할 때
- 코드 리뷰에서 개선이 필요한 부분 발견 시
- 중복 코드가 많거나 복잡도가 높을 때
- 새로운 기능 추가 전 코드 정리 필요 시
- 기술 부채 해소가 필요할 때

## What It Does

1. 현재 코드 분석 (문제점 파악)
2. 리팩토링 계획 수립
3. 테스트 확인 (리팩토링 전 테스트 통과 확인)
4. 점진적 리팩토링 실행
5. 각 단계마다 테스트 실행
6. 최종 검증 및 문서화

## Steps

### Step 1: 현재 코드 분석
```python
# 분석 항목:
# 1. 코드 복잡도 (Cyclomatic Complexity)
# 2. 중복 코드 (Code Duplication)
# 3. 긴 함수/클래스 (Long Method/Class)
# 4. 큰 파라미터 목록 (Long Parameter List)
# 5. 데이터 뭉치 (Data Clumps)
# 6. 기능 편애 (Feature Envy)
# 7. 부적절한 이름 (Inappropriate Names)
```

### Step 2: 리팩토링 계획
- **목표**: 무엇을 개선할 것인가
- **범위**: 어디까지 리팩토링할 것인가
- **순서**: 어떤 순서로 진행할 것인가
- **테스트**: 어떻게 검증할 것인가
- **리스크**: 어떤 위험이 있는가

### Step 3: 테스트 확인
```bash
# 리팩토링 전 모든 테스트가 통과해야 함
pytest -v

# 테스트가 없다면 먼저 테스트 작성
```

### Step 4: 점진적 리팩토링
**중요**: 한 번에 하나의 리팩토링만 수행
- 작은 단위로 변경
- 각 변경 후 테스트 실행
- 실패하면 롤백하고 다시 시도

### Step 5: 테스트 재실행
```bash
# 각 리팩토링 후 테스트
pytest -v

# 모든 테스트 통과 확인
```

### Step 6: 문서 업데이트
- 변경된 API가 있다면 문서 업데이트
- 주요 변경사항 기록
- 코드 리뷰 요청

## Common Refactoring Patterns

### 1. Extract Method (메서드 추출)
**언제**: 함수가 너무 길거나 복잡할 때

**Before**:
```python
def process_user_data(user_data):
    # Validate
    if not user_data.get('name'):
        raise ValueError("Name is required")
    if not user_data.get('email'):
        raise ValueError("Email is required")
    if '@' not in user_data.get('email', ''):
        raise ValueError("Invalid email")

    # Transform
    name = user_data['name'].strip().title()
    email = user_data['email'].strip().lower()
    age = int(user_data.get('age', 0))

    # Save
    db.execute(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        (name, email, age)
    )
    return {'name': name, 'email': email, 'age': age}
```

**After**:
```python
def process_user_data(user_data):
    validate_user_data(user_data)
    normalized_data = normalize_user_data(user_data)
    save_user(normalized_data)
    return normalized_data

def validate_user_data(user_data):
    if not user_data.get('name'):
        raise ValueError("Name is required")
    if not user_data.get('email'):
        raise ValueError("Email is required")
    if '@' not in user_data.get('email', ''):
        raise ValueError("Invalid email")

def normalize_user_data(user_data):
    return {
        'name': user_data['name'].strip().title(),
        'email': user_data['email'].strip().lower(),
        'age': int(user_data.get('age', 0))
    }

def save_user(user_data):
    db.execute(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        (user_data['name'], user_data['email'], user_data['age'])
    )
```

### 2. Replace Magic Numbers (매직 넘버 제거)
**언제**: 코드에 의미 없는 숫자가 하드코딩되어 있을 때

**Before**:
```python
def calculate_price(base_price, quantity):
    if quantity > 100:
        discount = base_price * 0.1
    elif quantity > 50:
        discount = base_price * 0.05
    else:
        discount = 0
    return base_price - discount
```

**After**:
```python
LARGE_ORDER_THRESHOLD = 100
MEDIUM_ORDER_THRESHOLD = 50
LARGE_ORDER_DISCOUNT = 0.1
MEDIUM_ORDER_DISCOUNT = 0.05

def calculate_price(base_price, quantity):
    if quantity > LARGE_ORDER_THRESHOLD:
        discount = base_price * LARGE_ORDER_DISCOUNT
    elif quantity > MEDIUM_ORDER_THRESHOLD:
        discount = base_price * MEDIUM_ORDER_DISCOUNT
    else:
        discount = 0
    return base_price - discount
```

### 3. Introduce Explaining Variable (설명 변수 도입)
**언제**: 복잡한 표현식을 이해하기 어려울 때

**Before**:
```python
if (platform.platform().startswith('Darwin') and
    platform.release().split('.')[0] >= '20'):
    # macOS Big Sur or later
    use_new_api()
```

**After**:
```python
is_macos = platform.platform().startswith('Darwin')
major_version = int(platform.release().split('.')[0])
is_big_sur_or_later = major_version >= 20

if is_macos and is_big_sur_or_later:
    use_new_api()
```

### 4. Replace Conditional with Polymorphism (조건문을 다형성으로)
**언제**: 타입에 따른 분기가 많을 때

**Before**:
```python
def get_metric_value(metric_type, data):
    if metric_type == 'cpu':
        return data['cpu_percent']
    elif metric_type == 'memory':
        return data['memory_percent']
    elif metric_type == 'disk':
        return data['disk_percent']
    else:
        raise ValueError(f"Unknown metric: {metric_type}")
```

**After**:
```python
class MetricCollector(ABC):
    @abstractmethod
    def get_value(self, data):
        pass

class CPUCollector(MetricCollector):
    def get_value(self, data):
        return data['cpu_percent']

class MemoryCollector(MetricCollector):
    def get_value(self, data):
        return data['memory_percent']

class DiskCollector(MetricCollector):
    def get_value(self, data):
        return data['disk_percent']

# Usage
collectors = {
    'cpu': CPUCollector(),
    'memory': MemoryCollector(),
    'disk': DiskCollector()
}
value = collectors[metric_type].get_value(data)
```

### 5. Simplify Conditional Logic (조건문 단순화)
**언제**: 중첩된 조건문이 복잡할 때

**Before**:
```python
def check_access(user, resource):
    if user is not None:
        if user.is_active:
            if user.has_permission(resource):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
```

**After (Early Return)**:
```python
def check_access(user, resource):
    if user is None:
        return False
    if not user.is_active:
        return False
    if not user.has_permission(resource):
        return False
    return True

# Or even better
def check_access(user, resource):
    return (
        user is not None and
        user.is_active and
        user.has_permission(resource)
    )
```

### 6. Extract Class (클래스 추출)
**언제**: 클래스가 너무 많은 책임을 가질 때

**Before**:
```python
class Agent:
    def __init__(self):
        self.metrics = {}
        self.server_url = ""
        self.retry_count = 3

    def collect_cpu(self):
        # CPU collection logic
        pass

    def collect_memory(self):
        # Memory collection logic
        pass

    def send_metrics(self):
        # Sending logic with retry
        pass

    def retry_with_backoff(self):
        # Retry logic
        pass
```

**After**:
```python
class MetricCollector:
    def collect_cpu(self):
        pass

    def collect_memory(self):
        pass

class MetricSender:
    def __init__(self, server_url, retry_count=3):
        self.server_url = server_url
        self.retry_count = retry_count

    def send(self, metrics):
        pass

    def retry_with_backoff(self):
        pass

class Agent:
    def __init__(self, server_url):
        self.collector = MetricCollector()
        self.sender = MetricSender(server_url)

    def run(self):
        metrics = self.collector.collect_all()
        self.sender.send(metrics)
```

### 7. Replace Loop with Comprehension (루프를 컴프리헨션으로)
**언제**: 단순한 리스트 생성 루프

**Before**:
```python
result = []
for item in items:
    if item.is_valid():
        result.append(item.value * 2)
```

**After**:
```python
result = [item.value * 2 for item in items if item.is_valid()]
```

### 8. Introduce Parameter Object (파라미터 객체 도입)
**언제**: 함수가 많은 파라미터를 받을 때

**Before**:
```python
def create_user(name, email, age, city, country, phone, address):
    # Implementation
    pass
```

**After**:
```python
@dataclass
class UserData:
    name: str
    email: str
    age: int
    city: str
    country: str
    phone: str
    address: str

def create_user(user_data: UserData):
    # Implementation
    pass
```

## Refactoring Checklist

### Before Refactoring
- [ ] 모든 테스트가 통과하는가?
- [ ] 리팩토링 목표가 명확한가?
- [ ] 변경 범위를 정의했는가?
- [ ] 백업 또는 브랜치를 생성했는가?

### During Refactoring
- [ ] 한 번에 하나의 변경만 수행
- [ ] 각 단계 후 테스트 실행
- [ ] 커밋을 작은 단위로 자주
- [ ] 코드 리뷰 준비

### After Refactoring
- [ ] 모든 테스트가 통과하는가?
- [ ] 코드가 더 읽기 쉬워졌는가?
- [ ] 복잡도가 감소했는가?
- [ ] 문서를 업데이트했는가?
- [ ] 팀에게 공유했는가?

## Code Smells to Refactor

### 1. 🚨 Duplicated Code
중복된 코드는 Extract Method 또는 Extract Class로 해결

### 2. 🚨 Long Method
긴 함수는 Extract Method로 분리

### 3. 🚨 Large Class
큰 클래스는 Extract Class로 책임 분리

### 4. 🚨 Long Parameter List
긴 파라미터 목록은 Parameter Object로 해결

### 5. 🚨 Divergent Change
하나의 클래스가 여러 이유로 변경되면 Extract Class

### 6. 🚨 Shotgun Surgery
하나의 변경이 여러 클래스 수정을 요구하면 Move Method

### 7. 🚨 Feature Envy
메서드가 다른 클래스 데이터에 과도하게 접근하면 Move Method

### 8. 🚨 Data Clumps
항상 함께 다니는 데이터는 Extract Class

### 9. 🚨 Primitive Obsession
원시 타입 과다 사용은 Introduce Value Object

### 10. 🚨 Switch Statements
switch/if-elif 과다 사용은 Replace with Polymorphism

## Best Practices

### DO:
- ✅ 작은 단계로 진행
- ✅ 각 단계마다 테스트
- ✅ 의미 있는 커밋
- ✅ 코드 리뷰 요청
- ✅ 문서 업데이트

### DON'T:
- ❌ 기능 변경과 리팩토링 동시 진행
- ❌ 테스트 없이 리팩토링
- ❌ 한 번에 모든 것 변경
- ❌ 리팩토링만을 위한 리팩토링
- ❌ 동작하는 코드를 망가뜨림

## When NOT to Refactor

- 🛑 **데드라인 임박**: 긴급한 배포 전
- 🛑 **불안정한 코드**: 버그가 많고 테스트가 없을 때
- 🛑 **레거시 시스템**: 전체 재작성이 더 나을 때
- 🛑 **임시 코드**: 곧 삭제될 코드
- 🛑 **이해 부족**: 코드를 완전히 이해하지 못했을 때

## Tools

### Python Refactoring Tools
- **Rope**: Python 리팩토링 라이브러리
- **PyCharm**: 강력한 리팩토링 도구 내장
- **VS Code**: 기본 리팩토링 기능 제공

### Analysis Tools
- **radon**: 복잡도 측정
- **pylint**: 코드 스멜 탐지
- **SonarQube**: 종합 코드 품질 분석

## Notes

- 리팩토링은 기능을 변경하지 않음 (behavior-preserving)
- 테스트는 리팩토링의 안전망
- 작은 단계로 자주 커밋
- 팀과 소통하며 진행
- 성능 최적화는 별도로 (premature optimization 지양)
- 레거시 코드는 점진적으로 개선
- 리팩토링 후 성능이 저하되었다면 롤백 고려
