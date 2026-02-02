---
name: git-commit
description: 변경사항을 체계적으로 커밋하고 문서를 업데이트합니다
version: 2.0.0
---

# Git Commit Skill

이 스킬은 코드 변경사항을 커밋할 때 문서 업데이트, staging, 커밋 메시지 작성, push까지 체계적으로 수행합니다.

## When to Use

- 사용자가 "커밋해줘", "commit", "git commit" 등을 요청할 때
- 의미 있는 작업 단위가 완료되었을 때
- 문서와 코드를 함께 커밋해야 할 때

## What It Does

1. 변경된 파일 확인
2. 문서 업데이트 (plan.md, progress.md)
3. 적절한 파일만 staging
4. 의미있는 커밋 메시지 작성
5. 커밋 생성 및 확인

## Steps

### Step 1: 현재 상태 확인
```bash
git status
git diff
git log --oneline -5
```

### Step 2: 문서 업데이트
- `docs/progress.md`: 완료된 작업의 체크박스 업데이트, 작업 로그 추가
- `docs/plan.md`: 완료된 작업의 체크박스 업데이트
- 진행률 계산 및 업데이트

### Step 3: 파일 Staging
- 변경된 파일 중 커밋할 파일만 선택적으로 add
- 민감한 정보 (.env, credentials 등)는 제외
- 임시 파일이나 빌드 산출물은 제외

```bash
git add [선택한 파일들]
```

### Step 4: 커밋 메시지 작성
프로젝트의 커밋 컨벤션을 따르며, 다음 형식을 사용:

```
<type>: <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Type 종류:**
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포매팅 (기능 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드/설정 파일 수정

**Subject 규칙:**
- 50자 이내
- 명령형 동사로 시작
- 마침표 없음
- 한글 또는 영문 사용

**Body:**
- 무엇을, 왜 변경했는지 설명
- 각 라인은 72자 이내
- 여러 변경사항이 있으면 bullet point 사용

### Step 5: 커밋 실행
```bash
git commit -m "$(cat <<'EOF'
커밋 메시지 내용
EOF
)"
```

### Step 6: 커밋 확인
```bash
git status
git log -1 --stat
```

## Commit Message Examples

### Example 1: 기능 추가
```
feat: CPU 메트릭 수집기 구현

- psutil을 사용한 CPU 사용률 수집
- 코어별 사용률 및 로드 평균 추가
- 상위 CPU 사용 프로세스 정보 포함

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Example 2: 문서 업데이트
```
docs: Phase 1 진행 상황 업데이트 (95% 완료)

메트릭 수집 에이전트 구현 완료에 따른 문서 업데이트:
- progress.md: Phase 1 체크박스 업데이트 및 작업 로그 추가
- plan.md: Phase 1 체크박스 업데이트
- 전체 진행률: 0% → 19%

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Example 3: 버그 수정
```
fix: 메모리 수집기에서 스왑 메모리 계산 오류 수정

스왑 메모리 퍼센트 계산 시 0으로 나누기 오류 발생 가능성 수정
- 스왑 메모리가 0일 때 예외 처리 추가
- 단위 테스트 추가

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Important Rules

### DO:
- ✅ 의미있는 단위로 커밋 분리
- ✅ 명확하고 구체적인 커밋 메시지 작성
- ✅ 관련 파일만 함께 커밋
- ✅ 커밋 전 문서 업데이트
- ✅ 커밋 후 상태 확인

### DON'T:
- ❌ 여러 기능을 한 커밋에 포함
- ❌ "WIP", "test", "fix" 같은 모호한 메시지
- ❌ 민감한 정보 (.env, credentials) 커밋
- ❌ 불필요한 파일 (node_modules, __pycache__) 커밋
- ❌ 테스트 실패 상태로 커밋

## Git Safety Protocol

- **절대 실행 금지**: `git reset --hard`, `git push --force` (사용자 명시적 요청 제외)
- **Hook 존중**: pre-commit hook 실패 시 문제 해결 후 새 커밋 생성 (--no-verify 사용 금지)
- **브랜치 확인**: main/master에 직접 커밋 전 사용자에게 확인
- **변경사항 확인**: 커밋 전 반드시 git diff로 변경 내용 검토

## Notes

- push는 별도로 요청받았을 때만 수행
- 커밋 메시지는 heredoc을 사용하여 올바른 포매팅 보장
- 프로젝트의 기존 커밋 메시지 스타일 참고 (git log 확인)
- 대규모 변경사항은 여러 개의 논리적 커밋으로 분리
