# 📦 GitHub 패키지 배포 가이드

## 🎯 배포 방법 종류

### 1. 📦 PyPI (Python Package Index) 배포
- **장점**: `pip install starwargez-comment-collector`로 간편 설치
- **사용자**: Python 개발자, 명령줄 사용자
- **설치 후 사용법**: 
  ```bash
  pip install starwargez-comment-collector
  starwargez-gui  # GUI 버전 실행
  starwargez-cli  # CLI 버전 실행
  ```

### 2. 🚀 GitHub Releases (실행 파일 배포)
- **장점**: Python 설치 불필요, 일반 사용자 친화적
- **사용자**: 모든 사용자 (Windows, macOS, Linux)
- **사용법**: 다운로드 후 바로 실행

### 3. 📱 GitHub Packages (Docker/npm 등)
- **장점**: 다양한 패키지 형태 지원
- **사용자**: 고급 사용자, 개발자

## 🔧 PyPI 배포 설정

### 1. PyPI 계정 설정
1. [PyPI](https://pypi.org/) 계정 생성
2. [Test PyPI](https://test.pypi.org/) 계정도 생성 (테스트용)
3. API 토큰 생성:
   - PyPI > Account Settings > API tokens > Add API token
   - Test PyPI에서도 동일하게 진행

### 2. GitHub Secrets 설정
GitHub 리포지토리에서 Settings > Secrets and variables > Actions에 추가:

```
PYPI_API_TOKEN: pypi-AgE... (PyPI API 토큰)
TEST_PYPI_API_TOKEN: pypi-AgE... (Test PyPI API 토큰)
```

### 3. 수동 배포 방법

```bash
# 1. 빌드 도구 설치
pip install build twine wheel

# 2. 패키지 빌드
python -m build

# 3. Test PyPI에 업로드 (테스트)
python -m twine upload --repository testpypi dist/*

# 4. PyPI에 업로드 (실제 배포)
python -m twine upload dist/*
```

### 4. 자동 배포 (GitHub Actions)
- 태그 푸시 시 자동 배포: `git tag v1.0.0 && git push origin v1.0.0`
- Release 생성 시 자동 배포: GitHub에서 Release 생성

## 🚀 GitHub Releases 배포

### 1. 자동 빌드 설정
- GitHub Actions가 자동으로 Windows, macOS, Linux용 실행 파일 생성
- Release 생성 시 자동으로 업로드

### 2. 수동 Release 생성
1. GitHub 리포지토리 > Releases > Create a new release
2. Tag version: `v1.0.0` (새 태그 생성)
3. Release title: `빛이왔다 스타워게즈 댓글 자동 수집기 v1.0.0`
4. Description 작성
5. Publish release 클릭

### 3. 실행 파일 직접 업로드
```bash
# 로컬에서 빌드
./build.sh  # 또는 build.bat

# 생성된 파일을 Release에 수동 업로드
# dist/ 폴더의 실행 파일들을 GitHub Release에 업로드
```

## 📱 GitHub Packages 배포

### 1. GitHub Container Registry (Docker)
```dockerfile
# Dockerfile 예시
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "gui_main.py"]
```

### 2. npm 패키지로 배포
```json
{
  "name": "@pepe-made-it/starwargez-comment-collector",
  "version": "1.0.0",
  "description": "빛이왔다 스타워게즈 댓글 자동 수집기",
  "repository": "github:pepe-made-it/star"
}
```

## 🎨 버전 관리 전략

### 1. 시맨틱 버저닝 (Semantic Versioning)
- `MAJOR.MINOR.PATCH` (예: 1.2.3)
- **MAJOR**: 호환되지 않는 API 변경
- **MINOR**: 기능 추가 (하위 호환)
- **PATCH**: 버그 수정

### 2. 태그 규칙
```bash
git tag v1.0.0    # 메이저 릴리스
git tag v1.0.1    # 패치 릴리스
git tag v1.1.0    # 마이너 릴리스
```

### 3. 브랜치 전략
- `main`: 안정된 릴리스 브랜치
- `develop`: 개발 브랜치
- `feature/기능명`: 새 기능 개발
- `hotfix/버그명`: 긴급 버그 수정

## 🔄 배포 프로세스

### 완전 자동화 배포
1. **코드 개발** → develop 브랜치에서 작업
2. **Pull Request** → main 브랜치로 병합
3. **태그 생성** → `git tag v1.0.0 && git push origin v1.0.0`
4. **자동 배포** → GitHub Actions가 모든 플랫폼에 배포

### 수동 배포
1. **로컬 빌드**: `./build.sh` 실행
2. **PyPI 업로드**: `twine upload dist/*`
3. **GitHub Release**: 웹에서 Release 생성
4. **실행 파일 업로드**: Release에 파일 첨부

## 📊 배포 상태 확인

### PyPI 패키지 상태
- [PyPI 프로젝트 페이지](https://pypi.org/project/starwargez-comment-collector/)
- 다운로드 통계 확인
- 버전 히스토리 확인

### GitHub Releases 상태
- [Releases 페이지](https://github.com/pepe-made-it/star/releases)
- 다운로드 횟수 확인
- Assets 파일 확인

### GitHub Actions 상태
- [Actions 탭](https://github.com/pepe-made-it/star/actions)
- 빌드 성공/실패 확인
- 로그 확인

## 🛠️ 문제 해결

### PyPI 업로드 실패
```bash
# 캐시 정리
rm -rf dist/ build/ *.egg-info/

# 다시 빌드
python -m build

# 토큰 확인
twine check dist/*
```

### GitHub Actions 실패
1. Actions 탭에서 실패 로그 확인
2. 의존성 버전 충돌 확인
3. Secret 토큰 유효성 확인

### 실행 파일 빌드 실패
```bash
# 가상환경 재생성
python -m venv build_env
source build_env/bin/activate  # Windows: build_env\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
```

## 📈 마케팅 및 홍보

### 1. GitHub 리포지토리 최적화
- **README.md**: 명확한 설명과 예시
- **스크린샷**: GUI 실행 화면
- **배지**: PyPI 다운로드, 빌드 상태
- **토픽**: 관련 키워드 태그

### 2. 외부 플랫폼 홍보
- **Reddit**: r/Python, r/Korea 등
- **블로그**: 개발 과정 포스팅
- **YouTube**: 사용법 동영상
- **카페 커뮤니티**: 실제 사용 사례

### 3. SEO 최적화
- **키워드**: "네이버 카페 댓글 수집", "Python 웹 스크래핑"
- **메타데이터**: setup.py의 keywords 최적화
- **문서화**: 상세한 사용법 가이드

## 🎉 성공 지표

### 다운로드 목표
- **PyPI**: 월 100회 다운로드
- **GitHub Releases**: 월 50회 다운로드
- **Star**: 10개 이상

### 사용자 피드백
- **Issues**: 버그 리포트 및 기능 요청
- **Discussions**: 사용자 질문 및 의견
- **Pull Requests**: 커뮤니티 기여

이제 이 파일들을 GitHub에 커밋하고 Release를 생성하면 자동으로 배포가 시작됩니다! 🚀 