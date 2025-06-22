# 🚀 배포 체크리스트

## ✅ 필수 준비사항

### 1. 계정 및 토큰 설정
- [ ] [PyPI](https://pypi.org/) 계정 생성 및 API 토큰 발급
- [ ] [Test PyPI](https://test.pypi.org/) 계정 생성 및 API 토큰 발급
- [ ] GitHub에서 Settings > Secrets and variables > Actions에 토큰 추가:
  - [ ] `PYPI_API_TOKEN`
  - [ ] `TEST_PYPI_API_TOKEN`

### 2. 패키지 메타데이터 확인
- [ ] `setup.py`의 이메일 주소 수정: `your-email@example.com` → 실제 이메일
- [ ] `pyproject.toml`의 이메일 주소 수정
- [ ] 패키지명 중복 확인: [PyPI에서 starwargez-comment-collector 검색](https://pypi.org/search/?q=starwargez-comment-collector)

### 3. 라이선스 확인
- [ ] `LICENSE` 파일에 올바른 저작권자명 확인
- [ ] MIT 라이선스 사용 동의

## 🔄 배포 단계

### 1단계: 테스트 배포 (Test PyPI)
```bash
# 1. 빌드 도구 설치
pip install build twine wheel

# 2. 패키지 빌드
python -m build

# 3. Test PyPI에 업로드
python -m twine upload --repository testpypi dist/*

# 4. 테스트 설치 확인
pip install --index-url https://test.pypi.org/simple/ starwargez-comment-collector
```

### 2단계: 실제 배포 (PyPI)
```bash
# Test PyPI 테스트 성공 후
python -m twine upload dist/*
```

### 3단계: GitHub Release 배포
1. [ ] GitHub에서 새 Release 생성
2. [ ] 태그: `v1.0.0` (새 태그)
3. [ ] 제목: `빛이왔다 스타워게즈 댓글 자동 수집기 v1.0.0`
4. [ ] Release notes 작성
5. [ ] GitHub Actions가 자동으로 실행 파일 빌드 및 업로드 확인

## ✅ 배포 후 확인사항

### PyPI 배포 확인
- [ ] [PyPI 프로젝트 페이지](https://pypi.org/project/starwargez-comment-collector/) 접속 가능
- [ ] `pip install starwargez-comment-collector` 설치 테스트
- [ ] `starwargez-gui` 명령어 실행 테스트
- [ ] `starwargez-cli` 명령어 실행 테스트

### GitHub Releases 확인
- [ ] [Releases 페이지](https://github.com/pepe-made-it/star/releases)에서 파일 다운로드 가능
- [ ] Windows 실행 파일 테스트
- [ ] macOS 실행 파일 테스트 (가능한 경우)
- [ ] Linux 실행 파일 테스트 (가능한 경우)

### GitHub Actions 확인
- [ ] [Actions 탭](https://github.com/pepe-made-it/star/actions)에서 빌드 성공 확인
- [ ] PyPI 배포 액션 성공 확인
- [ ] 실행 파일 빌드 액션 성공 확인

## 🛠️ 문제 해결 가이드

### 패키지명 중복 오류
```
ERROR: The name 'starwargez-comment-collector' is already in use
```
→ `setup.py`와 `pyproject.toml`에서 다른 이름 사용 (예: `starwargez-collector-pepe`)

### API 토큰 오류
```
ERROR: Invalid authentication credentials
```
→ GitHub Secrets에 올바른 토큰이 설정되어 있는지 확인

### 빌드 실패
```
ERROR: Package 'package-name' not found
```
→ `requirements.txt`의 모든 패키지가 설치 가능한지 확인

## 📈 성공 지표

### 즉시 확인 가능
- [ ] PyPI에서 패키지 검색 가능
- [ ] pip install로 설치 가능
- [ ] 명령줄에서 실행 가능
- [ ] GitHub Releases에서 다운로드 가능

### 중장기 지표
- [ ] PyPI 다운로드 수 (목표: 월 100회)
- [ ] GitHub Stars 수 (목표: 10개)
- [ ] Issues/PR을 통한 사용자 피드백
- [ ] 커뮤니티 성장

## 🎯 다음 단계

### 마케팅 및 홍보
- [ ] 개발 블로그 포스팅
- [ ] Reddit r/Python 커뮤니티 공유
- [ ] 네이버 카페 관련 커뮤니티 공유
- [ ] YouTube 사용법 동영상 제작

### 지속적 개선
- [ ] 사용자 피드백 수집
- [ ] 버그 수정 및 기능 추가
- [ ] 정기적인 업데이트 배포
- [ ] 문서화 개선

---

## 🚀 지금 바로 시작하기!

1. **이메일 주소 수정**: `setup.py`와 `pyproject.toml`에서 실제 이메일로 변경
2. **PyPI 계정 생성**: [pypi.org](https://pypi.org)에서 계정 생성
3. **GitHub Secrets 설정**: API 토큰 추가
4. **테스트 배포**: Test PyPI로 먼저 테스트
5. **실제 배포**: PyPI에 최종 배포

모든 파일이 준비되었으니 이제 배포를 시작하세요! 🎉 