#!/bin/bash

# 빛이왔다 스타워게즈 댓글 자동 수집기 자동 빌드 스크립트
# macOS/Linux용

echo "🌟 빛이왔다 스타워게즈 댓글 자동 수집기 빌드 시작..."
echo "========================================"

# 필요한 패키지 확인
echo "📦 필요한 패키지 확인 중..."
if ! command -v pyinstaller &> /dev/null; then
    echo "⚠️ PyInstaller가 설치되어 있지 않습니다."
    echo "📥 PyInstaller 설치 중..."
    pip install pyinstaller
fi

# 기존 빌드 파일 정리
echo "🧹 기존 빌드 파일 정리 중..."
rm -rf build/
rm -rf dist/
rm -f *.spec

# GUI 버전 빌드
echo "🎨 GUI 버전 빌드 중..."
pyinstaller --onefile --windowed --name "네이버카페댓글수집기" gui_main.py

if [ $? -eq 0 ]; then
    echo "✅ GUI 버전 빌드 성공!"
else
    echo "❌ GUI 버전 빌드 실패!"
    exit 1
fi

# 터미널 버전 빌드
echo "💻 터미널 버전 빌드 중..."
pyinstaller --onefile --name "네이버카페댓글수집기_터미널" main.py

if [ $? -eq 0 ]; then
    echo "✅ 터미널 버전 빌드 성공!"
else
    echo "❌ 터미널 버전 빌드 실패!"
    exit 1
fi

# 결과 확인
echo ""
echo "🎉 빌드 완료!"
echo "========================================"
echo "📁 생성된 파일들:"
ls -la dist/

echo ""
echo "📊 파일 크기:"
du -h dist/*

echo ""
echo "✅ 모든 빌드가 완료되었습니다!"
echo "📂 dist/ 폴더에서 실행 파일을 확인하세요."
echo ""
echo "🚀 테스트 방법:"
echo "   GUI 버전: ./dist/네이버카페댓글수집기"
echo "   터미널 버전: ./dist/네이버카페댓글수집기_터미널" 