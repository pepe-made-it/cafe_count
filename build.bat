@echo off
chcp 65001 >nul

REM 빛이왔다 스타워게즈 댓글 자동 수집기 자동 빌드 스크립트
REM Windows용

echo 🌟 빛이왔다 스타워게즈 댓글 자동 수집기 빌드 시작...
echo ========================================

REM 필요한 패키지 확인
echo 📦 필요한 패키지 확인 중...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ PyInstaller가 설치되어 있지 않습니다.
    echo 📥 PyInstaller 설치 중...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller 설치 실패!
        pause
        exit /b 1
    )
)

REM 기존 빌드 파일 정리
echo 🧹 기존 빌드 파일 정리 중...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

REM GUI 버전 빌드
echo 🎨 GUI 버전 빌드 중...
pyinstaller --onefile --windowed --name "네이버카페댓글수집기" gui_main.py

if errorlevel 1 (
    echo ❌ GUI 버전 빌드 실패!
    pause
    exit /b 1
) else (
    echo ✅ GUI 버전 빌드 성공!
)

REM 터미널 버전 빌드
echo 💻 터미널 버전 빌드 중...
pyinstaller --onefile --name "네이버카페댓글수집기_터미널" main.py

if errorlevel 1 (
    echo ❌ 터미널 버전 빌드 실패!
    pause
    exit /b 1
) else (
    echo ✅ 터미널 버전 빌드 성공!
)

REM 결과 확인
echo.
echo 🎉 빌드 완료!
echo ========================================
echo 📁 생성된 파일들:
dir dist\

echo.
echo ✅ 모든 빌드가 완료되었습니다!
echo 📂 dist\ 폴더에서 실행 파일을 확인하세요.
echo.
echo 🚀 테스트 방법:
echo    GUI 버전: dist\네이버카페댓글수집기.exe
echo    터미널 버전: dist\네이버카페댓글수집기_터미널.exe
echo.
pause 