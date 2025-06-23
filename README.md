# 🌟 빛이왔다 스타워게즈 댓글 자동 수집기

[![GitHub release](https://img.shields.io/github/release/pepe-made-it/cafe_count.svg)](https://github.com/pepe-made-it/cafe_count/releases)
[![Downloads](https://img.shields.io/github/downloads/pepe-made-it/cafe_count/total.svg)](https://github.com/pepe-made-it/cafe_count/releases)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

네이버 카페 "빛이왔다" 스타워게즈 게시글의 댓글을 자동으로 수집하는 도구입니다.

## 📥 다운로드 및 설치

### 방법 1: 실행 파일 다운로드 (추천)
[**GitHub Releases**](https://github.com/pepe-made-it/cafe_count/releases)에서 운영체제에 맞는 파일을 다운로드하세요:

- **Windows**: `빛이왔다_스타워게즈_댓글수집기_Windows.zip`
- **macOS**: `빛이왔다_스타워게즈_댓글수집기.dmg` 또는 `.tar.gz`
- **Linux**: `빛이왔다_스타워게즈_댓글수집기_Linux.tar.gz`

압축을 해제하고 실행 파일을 실행하면 됩니다!

### 방법 2: 소스코드로 실행
```bash
# 저장소 클론
git clone https://github.com/pepe-made-it/cafe_count.git
cd cafe_count

# 의존성 설치
pip install -r requirements.txt

# GUI 버전 실행
python gui_main.py

# 터미널 버전 실행
python main.py
```

## ✨ 주요 기능

- **🔥 자동 댓글 수집**: 지정된 게시글의 모든 댓글을 자동으로 수집
- **📊 엑셀 저장**: 수집된 댓글을 깔끔한 엑셀 파일로 저장
- **🖥️ GUI 지원**: 사용하기 쉬운 그래픽 인터페이스 제공
- **⌨️ 터미널 지원**: 명령줄에서도 사용 가능
- **🔄 실시간 진행률**: 수집 진행 상황을 실시간으로 확인

## 🚀 사용 방법

### GUI 버전
1. `빛이왔다_스타워게즈_댓글수집기` 실행 파일을 더블클릭
2. 게시글 번호 입력 (예: 17568)
3. "댓글 수집 시작" 버튼 클릭
4. 수집 완료 후 엑셀 파일 확인

### 터미널 버전
```bash
./빛이왔다_스타워게즈_댓글수집기_터미널
```

## 📋 입력 형식

다음 형식 중 하나를 사용하세요:
- 게시글 번호만: `17568`
- 전체 URL: `https://cafe.naver.com/herecamelight/17568`

## 📁 출력 파일

수집된 댓글은 다음 형식으로 저장됩니다:
```
빛이왔다_스타워게즈_댓글_[게시글번호]_[날짜시간].xlsx
```

예) `빛이왔다_스타워게즈_댓글_17568_20241120_143022.xlsx`

## 📊 출력 형식

엑셀 파일에는 다음 정보가 포함됩니다:
- **번호**: 댓글 순번
- **작성자**: 댓글 작성자 닉네임
- **댓글 내용**: 댓글 텍스트
- **작성 시간**: 댓글 작성 일시

## 🛠️ 개발자 정보

빛이왔다 스타워게즈 댓글 자동 수집기 v1.1.0
- **GitHub**: https://github.com/pepe-made-it/cafe_count
- **개발자**: pepe-made-it
- **라이선스**: MIT

## ⚠️ 주의사항

- 이 도구는 교육 및 개인 연구 목적으로 제작되었습니다
- 네이버 카페의 이용약관을 준수하여 사용하세요
- 과도한 요청으로 인한 서버 부하를 피하기 위해 적절한 간격을 두고 사용하세요
- 수집된 데이터의 사용에 대한 책임은 사용자에게 있습니다

## 🐛 문제 신고

버그 발견이나 기능 제안이 있으시면 [GitHub Issues](https://github.com/pepe-made-it/cafe_count/issues)에 신고해주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요. 