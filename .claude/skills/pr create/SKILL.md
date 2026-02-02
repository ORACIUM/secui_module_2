---
name: pr-create
description: Pull Request를 체계적으로 생성합니다
version: 1.0.0
---

# PR Create Skill

Pull Request를 생성할 때 변경사항을 분석하고, 의미있는 PR 제목과 설명을 작성하여 체계적으로 PR을 생성합니다.

## When to Use

- 사용자가 "PR 만들어줘", "pull request", "pr create" 등을 요청할 때
- 기능 개발 완료 후 메인 브랜치에 머지 필요 시
- 코드 리뷰 요청이 필요할 때
- 팀과 변경사항을 공유할 때

## What It Does

1. 현재 브랜치와 변경사항 확인
2. 베이스 브랜치 대비 전체 변경사항 분석
3. PR 제목 및 설명 작성
4. 테스트 실행 (선택적)
5. PR 생성
6. PR URL 반환

## Steps

### Step 1: 현재 상태 확인
```bash
# 현재 브랜치 확인
git branch --show-current

# 원격 추적 확인
git status

# 변경된 파일 확인
git diff --stat main...HEAD

# 전체 커밋 히스토리 (메인 브랜치 이후)
git log main..HEAD --oneline
```

### Step 2: 변경사항 분석
```bash
# 모든 변경사항 확인 (브랜치가 갈라진 시점부터)
git diff main...HEAD

# 파일별 변경사항
git diff main...HEAD --name-status

# 코드 통계
git diff main...HEAD --stat
```

**분석 항목**:
- 어떤 파일이 변경되었는가?
- 어떤 기능이 추가/수정되었는가?
- 테스트 코드가 포함되어 있는가?
- 문서가 업데이트되었는가?

### Step 3: PR 제목 및 설명 작성

#### PR 제목 (Title)
- **형식**: `<type>: <short description>`
- **길이**: 50-70자 이내
- **명확성**: 무엇이 변경되었는지 한눈에 파악 가능

**Type 종류**:
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `docs`: 문서 수정
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정 등
- `perf`: 성능 개선

**예시**:
- `feat: Add CPU metrics collector with psutil`
- `fix: Handle division by zero in memory percentage calculation`
- `refactor: Extract metric validation logic into separate module`

#### PR 설명 (Body)
```markdown
## Summary
3-5 bullet points로 주요 변경사항 요약

## Changes
- 변경사항 1
- 변경사항 2
- 변경사항 3

## Why
이 변경이 필요한 이유 설명

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests passing

## Screenshots (if applicable)
[Before/After 스크린샷]

## Breaking Changes
[호환성을 깨는 변경사항이 있다면 명시]

## Additional Notes
[추가 고려사항, 알려야 할 사항]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Step 4: 브랜치 Push (필요 시)
```bash
# 원격에 브랜치가 없다면 push
git push -u origin HEAD
```

### Step 5: PR 생성
```bash
# GitHub CLI 사용
gh pr create \
  --title "feat: Add CPU metrics collector" \
  --body "$(cat <<'EOF'
## Summary
- Implement CPU metrics collection using psutil
- Add per-core CPU usage tracking
- Include load average metrics

## Changes
- Add `src/agent/collectors/cpu.py` with CPU collection logic
- Add unit tests in `tests/unit/test_cpu_collector.py`
- Update configuration to enable/disable CPU collector
- Add CPU metrics to README

## Why
Phase 1 requirement: collect system resource metrics including CPU usage

## Testing
- [x] Unit tests added
- [x] All tests passing (pytest -v)
- [x] Manual testing on Windows

## Additional Notes
- Load average is not available on Windows (returns None)
- Requires psutil >= 5.9.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"

# 또는 대화형 모드
gh pr create
```

### Step 6: PR URL 확인
```bash
# 생성된 PR 확인
gh pr view --web
```

## PR Template Example

### 기본 템플릿
```markdown
## 📋 Description
[변경사항 간단 설명]

## 🎯 Motivation and Context
[왜 이 변경이 필요한가?]

## 🔧 Changes
- [ ] 변경사항 1
- [ ] 변경사항 2
- [ ] 변경사항 3

## 🧪 Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] All tests passing

## 📸 Screenshots
[Before/After 스크린샷]

## ⚠️ Breaking Changes
- [ ] No breaking changes
- [ ] Yes, breaking changes (describe below)

[설명]

## 📝 Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing

## 🔗 Related Issues
Closes #[issue number]
Related to #[issue number]

## 🤖 Additional Notes
[기타 참고사항]
```

### Feature PR 템플릿
```markdown
## ✨ New Feature: [Feature Name]

### What
[기능 설명]

### Why
[필요성]

### How
[구현 방법]

### Changes
- Added: [새로 추가된 것]
- Modified: [수정된 것]
- Removed: [제거된 것]

### Testing
```bash
# 테스트 실행 방법
pytest tests/test_new_feature.py
```

### Screenshots
[스크린샷]

### Documentation
- [ ] README updated
- [ ] API docs updated
- [ ] User guide updated

### Migration Guide
[기존 사용자를 위한 마이그레이션 가이드]
```

### Bug Fix PR 템플릿
```markdown
## 🐛 Bug Fix: [Bug Description]

### Problem
[버그 설명 및 재현 방법]

### Root Cause
[근본 원인 분석]

### Solution
[해결 방법]

### Changes
[변경된 코드]

### Testing
- [ ] Bug is fixed
- [ ] Regression tests added
- [ ] No side effects

### Before/After
**Before**: [버그 발생 상황]
**After**: [수정 후 동작]
```

## GitHub CLI Commands

### PR 생성
```bash
# 기본 생성
gh pr create

# 제목과 본문 지정
gh pr create --title "Title" --body "Body"

# 파일에서 본문 읽기
gh pr create --title "Title" --body-file pr-body.md

# 베이스 브랜치 지정
gh pr create --base main --head feature-branch

# 리뷰어 지정
gh pr create --reviewer user1,user2

# 레이블 추가
gh pr create --label bug,high-priority

# 드래프트 PR
gh pr create --draft
```

### PR 조회
```bash
# PR 목록
gh pr list

# 특정 PR 상세
gh pr view 123

# 웹 브라우저에서 열기
gh pr view 123 --web

# PR diff 보기
gh pr diff 123
```

### PR 업데이트
```bash
# PR 체크아웃
gh pr checkout 123

# PR에 코멘트
gh pr comment 123 --body "LGTM"

# PR 승인
gh pr review 123 --approve

# PR 수정 요청
gh pr review 123 --request-changes --body "Please fix..."

# PR 머지
gh pr merge 123

# PR 닫기
gh pr close 123
```

## Best Practices

### PR 크기
- 🎯 **작은 PR**: 300 lines 이하 (이상적)
- ⚠️ **중간 PR**: 300-1000 lines (리뷰 어려움)
- 🚨 **큰 PR**: 1000+ lines (나누기 권장)

**큰 PR을 나누는 방법**:
1. 리팩토링 + 기능 추가 → 분리
2. 여러 기능 → 기능별로 분리
3. 백엔드 + 프론트엔드 → 분리

### PR 제목
- ✅ 명확하고 구체적
- ✅ 커밋 메시지 컨벤션 따르기
- ✅ 이슈 번호 포함 (선택적)
- ❌ "update", "fix" 같은 모호한 제목

### PR 설명
- ✅ **Why**: 왜 필요한가
- ✅ **What**: 무엇이 변경되었는가
- ✅ **How**: 어떻게 구현했는가
- ✅ **Testing**: 어떻게 테스트했는가
- ✅ **Screenshots**: 시각적 변경사항

### 코드 리뷰 준비
- ✅ 모든 테스트 통과
- ✅ 린팅/포매팅 완료
- ✅ 자체 리뷰 완료
- ✅ TODO 제거 또는 이슈 생성
- ✅ 디버그 코드 제거

### PR 태그/레이블
- `feature`: 새 기능
- `bug`: 버그 수정
- `refactor`: 리팩토링
- `docs`: 문서
- `WIP`: 작업 중 (Draft PR 권장)
- `needs-review`: 리뷰 필요
- `breaking-change`: 호환성 깨는 변경

## PR Checklist

### Before Creating PR
- [ ] 브랜치명이 명확한가? (`feature/cpu-collector`, `fix/memory-leak`)
- [ ] 모든 커밋이 의미있는가?
- [ ] 커밋 메시지가 명확한가?
- [ ] 테스트가 모두 통과하는가?
- [ ] 린팅/포매팅이 완료되었는가?
- [ ] 문서가 업데이트되었는가?

### PR Content
- [ ] 제목이 명확한가?
- [ ] 설명이 충분한가?
- [ ] 스크린샷이 필요하면 포함했는가?
- [ ] Breaking changes가 명시되었는가?
- [ ] 관련 이슈가 링크되었는가?

### After Creating PR
- [ ] CI/CD가 통과하는가?
- [ ] 리뷰어를 지정했는가?
- [ ] 적절한 레이블을 추가했는가?
- [ ] 팀에게 알렸는가?

## Integration with Development Workflow

### Feature Branch Workflow
```bash
# 1. 새 브랜치 생성
git checkout -b feature/new-feature

# 2. 작업 및 커밋
git add .
git commit -m "feat: implement new feature"

# 3. Push
git push -u origin feature/new-feature

# 4. PR 생성
gh pr create

# 5. 리뷰 후 머지
gh pr merge --squash
```

### Continuous Integration
PR 생성 시 자동으로 실행되어야 하는 것들:
- ✅ 테스트 실행
- ✅ 린팅/포매팅 체크
- ✅ 빌드 확인
- ✅ 커버리지 체크
- ✅ 보안 스캔

## Common Issues and Solutions

### 1. 충돌 발생
```bash
# 메인 브랜치를 최신으로
git checkout main
git pull

# 기능 브랜치로 돌아와서 rebase
git checkout feature-branch
git rebase main

# 충돌 해결 후
git add .
git rebase --continue

# Force push (주의!)
git push --force-with-lease
```

### 2. PR이 너무 큼
```bash
# 새 브랜치들로 분리
git checkout -b feature/part1
git checkout -b feature/part2

# 각각 PR 생성
```

### 3. 잘못된 브랜치에서 작업
```bash
# 변경사항 저장
git stash

# 올바른 브랜치로 이동
git checkout correct-branch

# 변경사항 적용
git stash pop
```

## Notes

- PR 생성 전 항상 최신 main 브랜치와 동기화
- Draft PR 활용하여 조기 피드백 받기
- 큰 변경사항은 작은 PR로 나누기
- 리뷰어에게 컨텍스트 제공 (왜, 무엇을, 어떻게)
- 리뷰 코멘트에 신속하게 응답
- CI 실패 시 즉시 수정
- 머지 후 브랜치 삭제
- PR은 팀과의 소통 도구
