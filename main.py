# 중복 import 정리
import re, time, random
from collections import defaultdict

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
    NoSuchElementException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def create_driver():
    """웹드라이버 생성 함수"""
    # 랜덤 User-Agent 설정
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument(f"--user-agent={random.choice(user_agents)}")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(20)
    return driver

def human_like_wait(min_seconds=0.2, max_seconds=0.5):
    """인간처럼 랜덤 대기 (안정성 고려 버전)"""
    wait_time = random.uniform(min_seconds, max_seconds)
    print(f"⏰ {wait_time:.1f}초 대기 중...")
    time.sleep(wait_time)

def human_like_click(driver, element):
    """인간처럼 마우스 움직임과 함께 클릭 (안정성 고려 버전)"""
    try:
        element.click()  # 단순 클릭으로 변경
        time.sleep(random.uniform(0.2, 0.4))  # 안정적인 대기
    except:
        element.click()
        time.sleep(random.uniform(0.2, 0.4))  # 안정적인 대기

def wait_for_element(driver, by, selector, timeout=5):
    """요소가 나타날 때까지 대기하는 함수 (극한 최적화 버전)"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        # 대기 시간 완전 제거
        return element
    except TimeoutException:
        return None

def switch_to_article_frame(driver, post_id):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 최상위에서 모든 iframe을 뒤져서, 게시글 ID가 src에 포함된 iframe으로 전환
            driver.switch_to.default_content()  # 최상위 프레임으로 전환
            # 대기 시간 제거
            for f in driver.find_elements(By.TAG_NAME, "iframe"):
                src = f.get_attribute("src") or ""
                print(f"[DEBUG] iframe src 확인: {src}")
                if str(post_id) in src:
                    print(f"[DEBUG] 목표 게시글 {post_id} iframe 찾음!")
                    driver.switch_to.frame(f)
                    # 대기 시간 제거
                    return True
            return False
        except (StaleElementReferenceException, WebDriverException) as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(random.uniform(3, 5))  # 안정적인 랜덤 대기
    return False

def parse_comments_reverse(driver, post_url: str, post_id: int) -> list:
    """역순으로 댓글 수집 (마지막 페이지 → 첫 페이지)"""
    all_comments = []
    max_retries = 3

    print("🚀 역순 댓글 수집을 시작합니다...")

    # 1) 게시글 iframe으로 전환
    if not switch_to_article_frame(driver, post_id):
        raise RuntimeError("▶︎ 게시글 iframe을 찾을 수 없습니다.")

    # 2) 맨 뒤 버튼 클릭하여 마지막 페이지로 이동
    print("🔚 마지막 페이지로 이동 중...")
    
    # 클릭 전 현재 상태 확인
    print("[DEBUG] 클릭 전 페이지 상태 확인...")
    current_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
    print(f"[DEBUG] 클릭 전 페이지 버튼들: {[btn.text for btn in current_buttons]}")
    
    # 맨 뒤 버튼 찾기 (여러 가능한 셀렉터)
    last_page_selectors = [
        "button.btn.type_end",  # 맨 뒤 버튼
        "a.btn_end",
        "button[title='마지막페이지']",
        ".btn.end",
        "a.end"
    ]
    
    last_page_clicked = False
    for selector in last_page_selectors:
        last_btn = driver.find_elements(By.CSS_SELECTOR, selector)
        if last_btn and last_btn[0].is_enabled():
            print(f"[DEBUG] 맨 뒤 버튼 찾음: {selector}")
            print(f"[DEBUG] 버튼 텍스트: '{last_btn[0].text}'")
            print(f"[DEBUG] 버튼 활성화 상태: {last_btn[0].is_enabled()}")
            
            # 클릭 실행
            human_like_click(driver, last_btn[0])
            print("[DEBUG] 맨 뒤 버튼 클릭 완료")
            
            # 충분한 로딩 대기
            time.sleep(3)
            print("[DEBUG] 3초 대기 완료")
            
            # 클릭 후 상태 확인
            after_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
            print(f"[DEBUG] 클릭 후 페이지 버튼들: {[btn.text for btn in after_buttons]}")
            
            last_page_clicked = True
            break
    
    if not last_page_clicked:
        print("⚠️ 맨 뒤 버튼을 찾을 수 없습니다. 1페이지부터 시작합니다.")
        # 모든 버튼 확인해보기
        all_buttons = driver.find_elements(By.CSS_SELECTOR, "button, a")
        print(f"[DEBUG] 사용 가능한 모든 버튼들:")
        for i, btn in enumerate(all_buttons[:20]):  # 처음 20개만
            try:
                print(f"[DEBUG] {i}: {btn.tag_name} - '{btn.text}' - class: {btn.get_attribute('class')}")
            except:
                pass
    
    # 3) 현재 페이지 번호 확인 - 맨 뒤 버튼 클릭 후 또는 직접 감지
    print("[DEBUG] 마지막 페이지 번호 감지 중...")
    
    # 먼저 페이지 버튼들을 모두 확인해서 가장 큰 번호 찾기 (가장 확실한 방법)
    all_page_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
    page_numbers = []
    for btn in all_page_buttons:
        try:
            page_num = int(btn.text.strip())
            page_numbers.append(page_num)
            print(f"[DEBUG] 발견된 페이지 번호: {page_num}")
        except (ValueError, AttributeError):
            continue
    
    if page_numbers:
        current_page = max(page_numbers)
        print(f"🎯 감지된 마지막 페이지: {current_page}페이지 (버튼 분석)")
        
        # 맨 뒤 버튼이 없었지만 여러 페이지가 있는 경우 처리
        if not last_page_clicked and current_page > 1:
            print(f"[DEBUG] 맨 뒤 버튼 없이 {current_page}페이지 감지됨. 직접 이동합니다.")
            # 가장 큰 페이지 번호 버튼 클릭
            for btn in all_page_buttons:
                try:
                    if int(btn.text.strip()) == current_page:
                        print(f"[DEBUG] 마지막 페이지 {current_page} 직접 클릭")
                        human_like_click(driver, btn)
                        time.sleep(2)
                        break
                except (ValueError, AttributeError):
                    continue
    else:
        # 페이지 버튼이 아예 없는 경우 (댓글이 매우 적음)
        print("[DEBUG] 페이지 버튼이 없음. 단일 페이지로 추정.")
        
        # 백업: 활성 페이지 셀렉터로 시도
        page_selectors = [
            "button.btn.number.on",
            "button.btn.number.current", 
            "button.btn.number[class*='active']"
        ]
        
        current_page = 1
        for selector in page_selectors:
            active_pages = driver.find_elements(By.CSS_SELECTOR, selector)
            if active_pages:
                try:
                    current_page = int(active_pages[0].text.strip())
                    print(f"🎯 활성 페이지로 감지: {current_page}페이지 (셀렉터: {selector})")
                    break
                except (ValueError, AttributeError):
                    continue
        
        if current_page == 1:
            # 댓글이 있는지 확인
            comment_check = driver.find_elements(By.CSS_SELECTOR, "span.text_comment")
            if comment_check:
                print("🎯 1페이지에 댓글이 있음을 확인했습니다.")
            else:
                print("⚠️ 댓글을 찾을 수 없습니다. 빈 게시글일 수 있습니다.")

    # 4) 역순으로 댓글 수집 (마지막 → 첫 페이지)
    while current_page >= 1:
        for attempt in range(max_retries):
            try:
                # iframe 재전환 (안전성)
                if not switch_to_article_frame(driver, post_id):
                    raise RuntimeError("▶︎ 게시글 iframe을 찾을 수 없습니다.")

                # 댓글 로딩 대기
                time.sleep(random.uniform(1, 2))
                
                if not wait_for_element(driver, By.CSS_SELECTOR, "span.text_comment"):
                    raise TimeoutException("댓글을 찾을 수 없습니다.")

                # 댓글 수집
                authors = driver.find_elements(By.CSS_SELECTOR, "a.comment_nickname")
                texts = driver.find_elements(By.CSS_SELECTOR, "span.text_comment")
                
                if not authors or not texts:
                    print(f"[DEBUG] 페이지 {current_page}: 댓글 없음")
                    # 첫 페이지에서 댓글이 없으면 빈 게시글
                    if current_page == 1:
                        print("📝 이 게시글에는 댓글이 없습니다.")
                        return all_comments
                    break

                print(f"[DEBUG] 페이지 {current_page} → {len(authors)}개 댓글 수집")
                
                # 텍스트 즉시 추출
                page_comments = []
                for a, t in zip(authors, texts):
                    try:
                        author_text = a.text.strip()
                        comment_text = t.text.strip()
                        page_comments.append((author_text, comment_text))
                    except StaleElementReferenceException:
                        continue
                
                # 역순이므로 앞에 추가 (최종적으로 정순이 됨)
                all_comments = page_comments + all_comments
                break  # 성공하면 재시도 루프 종료

            except (WebDriverException, TimeoutException, NoSuchElementException) as e:
                print(f"⚠️ 오류 발생 (페이지 {current_page}): {str(e)}")
                if attempt == max_retries - 1:
                    print(f"❌ 페이지 {current_page} 수집 실패")
                    break
                time.sleep(random.uniform(1, 2))

        # 5) 다음 페이지로 이동 (역순: current_page-1)
        if current_page > 1:
            next_page = current_page - 1
            print(f"⬅️ {next_page}페이지로 이동 중...")
            
            # 현재 보이는 페이지 버튼들 확인
            page_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
            print(f"[DEBUG] 현재 페이지 버튼들: {[btn.text for btn in page_buttons]}")
            
            # 목표 페이지 번호 버튼 찾아서 클릭
            target_clicked = False
            for btn in page_buttons:
                try:
                    if int(btn.text.strip()) == next_page:
                        print(f"[DEBUG] 페이지 번호 직접 클릭: {btn.text}")
                        human_like_click(driver, btn)
                        target_clicked = True
                        time.sleep(random.uniform(1.0, 1.5))
                        break
                except (ValueError, AttributeError):
                    continue
            
            # 목표 페이지가 현재 블록에 없으면 이전 블록으로 이동
            if not target_clicked:
                print(f"[DEBUG] {next_page}페이지가 현재 블록에 없음. 이전 블록으로 이동...")
                prev_block_btn = driver.find_elements(By.CSS_SELECTOR, "button.btn.type_prev")
                if prev_block_btn and prev_block_btn[0].is_enabled():
                    print(f"[DEBUG] 이전 블록 버튼 클릭")
                    human_like_click(driver, prev_block_btn[0])
                    time.sleep(random.uniform(1.0, 1.5))
                    
                    # 블록 이동 후 다시 페이지 번호 클릭 시도
                    new_page_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
                    print(f"[DEBUG] 이전 블록 이동 후 페이지 버튼들: {[btn.text for btn in new_page_buttons]}")
                    
                    for btn in new_page_buttons:
                        try:
                            if int(btn.text.strip()) == next_page:
                                print(f"[DEBUG] 블록 이동 후 페이지 클릭: {btn.text}")
                                human_like_click(driver, btn)
                                target_clicked = True
                                time.sleep(random.uniform(1.0, 1.5))
                                break
                        except (ValueError, AttributeError):
                            continue
                else:
                    print("⚠️ 이전 블록 버튼이 비활성화되어 있습니다.")
            
            if not target_clicked:
                print(f"⚠️ {next_page}페이지로 이동할 수 없습니다.")
                print(f"📋 현재까지 {len(all_comments)}개 댓글을 수집했습니다.")
                break
        
        current_page -= 1
        
        # 1페이지 도달 시 종료
        if current_page < 1:
            print("✅ 모든 댓글 수집 완료! (1페이지 도달)")
            break

    return all_comments

def count_prefix_and_users(comments):
    """수정된 로직: [팀이름] 형식 댓글만 사용자별로도 카운트"""
    team_counts = defaultdict(int)
    user_counts = defaultdict(int)
    prefix_pattern = re.compile(r"^\[(.*?)\]")

    total_comments = len(comments)
    team_format_comments = 0

    for author, text in comments:
        m = prefix_pattern.match(text)
        if m:  # [팀이름] 형식의 댓글만 처리
            team_counts[m.group(1)] += 1
            user_counts[author] += 1  # 사용자별 카운트도 [팀이름] 댓글만
            team_format_comments += 1

    print(f"\n📊 댓글 분석 결과:")
    print(f"   총 댓글 수: {total_comments:,}개")
    print(f"   [팀이름] 형식 댓글: {team_format_comments:,}개")
    print(f"   일반 댓글: {total_comments - team_format_comments:,}개")
    print(f"   팀별 댓글 합계: {sum(team_counts.values()):,}개")
    print(f"   사용자별 댓글 합계: {sum(user_counts.values()):,}개")
    print(f"   ✅ 합계 일치: {sum(team_counts.values()) == sum(user_counts.values())}")
    print(f"   발견된 팀 수: {len(team_counts)}개")
    print(f"   참여 사용자 수: {len(user_counts)}명")

    return team_counts, user_counts

def output_to_excel(team_counts, user_counts, filename="output.xlsx"):
    # DataFrame 생성 시 컬럼명 별도 설정으로 타입 오류 해결
    df_team = pd.DataFrame(list(team_counts.items()))
    df_team.columns = ["팀이름", "댓글수"]
    
    df_user = pd.DataFrame(list(user_counts.items()))
    df_user.columns = ["사용자이름", "댓글수"]
    
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df_team.to_excel(writer, sheet_name="팀별댓글수", index=False)
        df_user.to_excel(writer, sheet_name="사용자별댓글수", index=False)
    print(f"✅ 결과가 '{filename}'로 저장되었습니다.")

def main():
    # 사용자로부터 게시글 번호 입력받기
    print("🌟 빛이왔다 스타워게즈 댓글 자동 수집기")
    print("=" * 40)
    print("💡 사용법: 카페 게시글 URL에서 숫자 부분을 입력하세요")
    print("   예) https://cafe.naver.com/herecamelight/17568 → 17568")
    print()
    
    while True:
        try:
            post_id_input = input("📝 게시글 번호를 입력하세요: ").strip()
            
            # 빈 입력 처리
            if not post_id_input:
                print("❌ 게시글 번호를 입력해주세요.")
                continue
                
            POST_ID = int(post_id_input)
            if POST_ID <= 0:
                print("❌ 양수를 입력해주세요.")
                continue
            break
        except ValueError:
            print("❌ 숫자만 입력해주세요.")
            continue
        except KeyboardInterrupt:
            print("\n👋 프로그램을 종료합니다.")
            return
    
    POST_URL = f"https://cafe.naver.com/herecamelight/{POST_ID}"
    CAFE_URL = "https://cafe.naver.com/herecamelight"  # 카페 메인 URL
    
    print(f"🎯 대상 게시글: {POST_URL}")
    print(f"📊 댓글 수집을 시작합니다...")
    
    # 1페이지부터 시작하여 전체 3,236개 댓글 수집


    driver = create_driver()

    try:
        # 수동 로그인 유도
        driver.get("https://nid.naver.com/nidlogin.login")
        print("👉 크롬 창에서 네이버에 로그인하세요.")
        print("로그인 완료 후 터미널에서 Enter를 눌러주세요...")
        input()

        # 카페 메인으로 이동
        print("🌐 카페 메인으로 이동 중...")
        driver.get(CAFE_URL)
        human_like_wait()  # 극소 대기

        # 게시글로 이동
        print(f"🌐 게시글로 이동 중... URL: {POST_URL}")
        driver.get(POST_URL)
        human_like_wait()  # 극소 대기
        
        # 현재 URL 확인
        current_url = driver.current_url
        print(f"[DEBUG] 현재 브라우저 URL: {current_url}")
        
        if "17568" not in current_url:
            print(f"⚠️ 경고: 목표 게시글(17568)과 다른 URL에 있습니다!")
            print(f"다시 정확한 URL로 이동합니다...")
            driver.get(POST_URL)
            time.sleep(2)
            print(f"[DEBUG] 재이동 후 URL: {driver.current_url}")

        # 1페이지부터 댓글 수집 시작
        comments = parse_comments_reverse(driver, POST_URL, POST_ID)
        print(f"총 댓글 수 집계: {len(comments)}개")

        team_counts, user_counts = count_prefix_and_users(comments)
        
        # 게시글 전체 댓글 결과 저장
        # 수정된 결과 저장 (게시글 번호에 맞는 파일명)
        output_filename = f"output_{POST_ID}_complete.xlsx"
        output_to_excel(team_counts, user_counts, output_filename)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
