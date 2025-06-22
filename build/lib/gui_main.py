#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import subprocess
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
from collections import Counter

class CafeCommentCollectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 빛이왔다 스타워게즈 댓글 자동 수집기")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 변수들
        self.post_id = tk.StringVar()
        self.save_path = tk.StringVar(value=os.getcwd())  # 기본값: 현재 폴더
        self.output_filename = ""
        self.is_collecting = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 제목
        title_label = ttk.Label(main_frame, text="🌟 빛이왔다 스타워게즈 댓글 자동 수집기", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 게시글 번호/URL 입력
        ttk.Label(main_frame, text="📝 게시글 번호 또는 URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.post_input_entry = ttk.Entry(main_frame, textvariable=self.post_id, width=50)
        self.post_input_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(5, 0))
        
        # 붙여넣기 기능 추가 (macOS와 Windows/Linux 모두 지원)
        self.setup_paste_functionality()
        
        # 입력 검증 제거 (URL도 입력 가능하도록)
        # vcmd = (self.root.register(self.validate_number), '%P')
        # post_id_entry.config(validate='key', validatecommand=vcmd)
        
        # 예시 라벨
        ttk.Label(main_frame, text="예: 17568 또는 https://cafe.naver.com/herecamelight/17568", 
                 foreground="gray").grid(row=2, column=1, sticky=tk.W, pady=(0, 10))
        
        # 저장 경로 선택
        ttk.Label(main_frame, text="💾 저장 경로:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=3, column=1, columnspan=2, sticky="ew", pady=5)
        path_frame.columnconfigure(0, weight=1)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.save_path, state="readonly")
        self.path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        browse_btn = ttk.Button(path_frame, text="찾아보기", command=self.browse_folder)
        browse_btn.grid(row=0, column=1)
        
        # 시작 버튼
        self.start_btn = ttk.Button(main_frame, text="🚀 댓글 수집 시작", 
                                   command=self.start_collection, style="Accent.TButton")
        self.start_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # 진행상황 표시
        progress_frame = ttk.LabelFrame(main_frame, text="📊 진행상황", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        
        # 프로그레스 바
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # 로그 텍스트 영역
        log_frame = ttk.Frame(progress_frame)
        log_frame.grid(row=1, column=0, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 결과 버튼 프레임
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.open_file_btn = ttk.Button(result_frame, text="📂 엑셀 파일 열기", 
                                       command=self.open_excel_file, state=tk.DISABLED)
        self.open_file_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.open_folder_btn = ttk.Button(result_frame, text="📁 폴더 열기", 
                                         command=self.open_folder, state=tk.DISABLED)
        self.open_folder_btn.grid(row=0, column=1)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def setup_paste_functionality(self):
        """붙여넣기 기능 설정 (macOS와 Windows/Linux 지원)"""
        def paste_text(event):
            try:
                # 클립보드에서 텍스트 가져오기
                clipboard_text = self.root.clipboard_get()
                
                # 현재 선택된 텍스트 삭제 후 붙여넣기
                if self.post_input_entry.selection_present():
                    self.post_input_entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
                
                # 커서 위치에 텍스트 삽입
                cursor_pos = self.post_input_entry.index(tk.INSERT)
                self.post_input_entry.insert(cursor_pos, clipboard_text)
                
                return 'break'  # 기본 이벤트 처리 방지
            except tk.TclError:
                # 클립보드가 비어있거나 텍스트가 아닌 경우
                pass
            return 'break'
        
        def paste_all_text(event):
            """전체 선택 후 붙여넣기"""
            try:
                clipboard_text = self.root.clipboard_get()
                self.post_id.set(clipboard_text)  # StringVar에 직접 설정
                return 'break'
            except tk.TclError:
                pass
            return 'break'
        
        # 다양한 붙여넣기 방법 바인딩
        # macOS: Cmd+V
        self.post_input_entry.bind('<Command-v>', paste_text)
        # Windows/Linux: Ctrl+V  
        self.post_input_entry.bind('<Control-v>', paste_text)
        # 마우스 가운데 버튼 (Linux/Unix 전통적 방식)
        self.post_input_entry.bind('<Button-2>', paste_text)
        # Shift+Insert (Windows 전통적 방식)
        self.post_input_entry.bind('<Shift-Insert>', paste_text)
        
        # 전체 선택 기능도 추가
        self.post_input_entry.bind('<Command-a>', lambda e: (self.post_input_entry.select_range(0, tk.END), 'break')[-1])
        self.post_input_entry.bind('<Control-a>', lambda e: (self.post_input_entry.select_range(0, tk.END), 'break')[-1])
        
        # 우클릭 컨텍스트 메뉴 추가 (선택사항)
        self.setup_context_menu()
    
    def setup_context_menu(self):
        """우클릭 컨텍스트 메뉴 설정"""
        def show_context_menu(event):
            try:
                context_menu = tk.Menu(self.root, tearoff=0)
                
                # 잘라내기
                context_menu.add_command(
                    label="잘라내기 ⌘X", 
                    command=lambda: self.context_cut()
                )
                
                # 복사
                context_menu.add_command(
                    label="복사 ⌘C", 
                    command=lambda: self.context_copy()
                )
                
                # 붙여넣기
                context_menu.add_command(
                    label="붙여넣기 ⌘V", 
                    command=lambda: self.context_paste()
                )
                
                context_menu.add_separator()
                
                # 전체 선택
                context_menu.add_command(
                    label="전체 선택 ⌘A", 
                    command=lambda: self.post_input_entry.select_range(0, tk.END)
                )
                
                # 메뉴 표시
                context_menu.post(event.x_root, event.y_root)
            except Exception:
                pass
        
        # 우클릭 바인딩 (macOS와 Windows/Linux)
        self.post_input_entry.bind('<Button-3>', show_context_menu)  # 우클릭
        self.post_input_entry.bind('<Control-Button-1>', show_context_menu)  # macOS Control+클릭
    
    def context_cut(self):
        """컨텍스트 메뉴 - 잘라내기"""
        try:
            if self.post_input_entry.selection_present():
                selected_text = self.post_input_entry.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                self.post_input_entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass
    
    def context_copy(self):
        """컨텍스트 메뉴 - 복사"""
        try:
            if self.post_input_entry.selection_present():
                selected_text = self.post_input_entry.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
        except tk.TclError:
            pass
    
    def context_paste(self):
        """컨텍스트 메뉴 - 붙여넣기"""
        try:
            clipboard_text = self.root.clipboard_get()
            if self.post_input_entry.selection_present():
                self.post_input_entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
            cursor_pos = self.post_input_entry.index(tk.INSERT)
            self.post_input_entry.insert(cursor_pos, clipboard_text)
        except tk.TclError:
            pass
        
    def extract_post_id(self, input_text):
        """입력된 텍스트에서 게시글 번호 추출"""
        input_text = input_text.strip()
        
        # URL 형태인 경우 (https://cafe.naver.com/herecamelight/12345)
        if "cafe.naver.com" in input_text:
            import re
            match = re.search(r'/(\d+)/?$', input_text)
            if match:
                return int(match.group(1))
            else:
                raise ValueError("URL에서 게시글 번호를 찾을 수 없습니다.")
        
        # 숫자만 입력된 경우
        elif input_text.isdigit():
            return int(input_text)
        
        else:
            raise ValueError("올바른 게시글 번호 또는 URL을 입력해주세요.")
    
    def browse_folder(self):
        """저장 폴더 선택"""
        folder = filedialog.askdirectory(initialdir=self.save_path.get())
        if folder:
            self.save_path.set(folder)
    
    def log_message(self, message):
        """로그 메시지 추가"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def start_collection(self):
        """댓글 수집 시작"""
        if not self.post_id.get().strip():
            messagebox.showerror("오류", "게시글 번호 또는 URL을 입력해주세요.")
            return
        
        # 입력값에서 게시글 번호 추출
        try:
            post_id = self.extract_post_id(self.post_id.get())
            self.current_post_id = post_id
        except ValueError as e:
            messagebox.showerror("입력 오류", str(e))
            return
        
        if self.is_collecting:
            messagebox.showwarning("알림", "이미 수집이 진행 중입니다.")
            return
        
        # UI 상태 변경
        self.is_collecting = True
        self.start_btn.config(state=tk.DISABLED, text="수집 중...")
        self.open_file_btn.config(state=tk.DISABLED)
        self.open_folder_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        # 로그 초기화
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # 백그라운드에서 수집 시작
        thread = threading.Thread(target=self.collect_comments, daemon=True)
        thread.start()
    
    def collect_comments(self):
        """실제 댓글 수집 작업 (백그라운드)"""
        try:
            post_id = self.current_post_id  # 이미 추출된 게시글 번호 사용
            post_url = f"https://cafe.naver.com/herecamelight/{post_id}"
            cafe_url = "https://cafe.naver.com/herecamelight"
            
            self.log_message(f"🎯 대상 게시글: {post_url}")
            self.log_message("🚀 댓글 수집을 시작합니다...")
            
            # 파일명 설정
            self.output_filename = os.path.join(self.save_path.get(), f"output_{post_id}_complete.xlsx")
            
            # 웹드라이버 설정
            self.log_message("🔧 크롬 브라우저를 준비 중...")
            
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            try:
                # 네이버 로그인
                self.log_message("🔐 네이버 로그인 페이지로 이동 중...")
                driver.get("https://nid.naver.com/nidlogin.login")
                
                self.log_message("👉 크롬 창에서 네이버에 로그인하세요.")
                self.log_message("⏳ 로그인 완료 후 확인 버튼을 눌러주세요...")
                
                # 사용자 로그인 완료 확인 대화상자
                login_confirmed = self.show_login_confirmation_dialog()
                
                if not login_confirmed:
                    self.log_message("❌ 사용자가 로그인을 취소했습니다.")
                    return
                
                self.log_message("✅ 로그인 완료 확인!")
                
                # 카페로 이동
                self.log_message("🏠 카페로 이동 중...")
                driver.get(cafe_url)
                time.sleep(3)
                
                # 게시글로 이동
                self.log_message(f"📄 게시글 {post_id}로 이동 중...")
                driver.get(post_url)
                time.sleep(3)
                
                # iframe 전환
                self.log_message("🔄 댓글 영역으로 전환 중...")
                self.switch_to_article_frame(driver)
                
                # 페이지 정보 확인
                self.log_message("🔍 페이지 상태 확인 중...")
                try:
                    # 게시글 제목 확인
                    title_elem = driver.find_element(By.CSS_SELECTOR, ".title_text")
                    self.log_message(f"📄 게시글 제목: {title_elem.text[:50]}...")
                except:
                    self.log_message("⚠️ 게시글 제목을 찾을 수 없습니다.")
                
                # 댓글 수집
                self.log_message("📝 댓글 수집 시작!")
                comments = self.parse_comments_reverse(driver)
                
                if not comments:
                    self.log_message("⚠️ 댓글이 없습니다.")
                    team_counts = {}
                    user_counts = {}
                else:
                    self.log_message(f"✅ 총 {len(comments)}개 댓글 수집 완료!")
                    
                    # 통계 계산
                    self.log_message("📊 통계 계산 중...")
                    team_counts, user_counts = self.count_prefix_and_users(comments)
                
                # Excel 저장
                self.log_message("💾 Excel 파일 저장 중...")
                self.output_to_excel(team_counts, user_counts, self.output_filename)
                
                self.log_message(f"🎉 완료! 파일 저장: {self.output_filename}")
                
            finally:
                driver.quit()
                
        except Exception as e:
            self.log_message(f"❌ 오류 발생: {str(e)}")
            messagebox.showerror("오류", f"수집 중 오류가 발생했습니다:\n{str(e)}")
        finally:
            # UI 상태 복원
            self.root.after(0, self.collection_finished)
    
    def collection_finished(self):
        """수집 완료 후 UI 상태 복원"""
        self.is_collecting = False
        self.start_btn.config(state=tk.NORMAL, text="🚀 댓글 수집 시작")
        self.progress.stop()
        
        # 파일이 생성되었으면 버튼 활성화
        if self.output_filename and os.path.exists(self.output_filename):
            self.open_file_btn.config(state=tk.NORMAL)
            self.open_folder_btn.config(state=tk.NORMAL)
    
    def open_excel_file(self):
        """Excel 파일 열기"""
        if self.output_filename and os.path.exists(self.output_filename):
            try:
                if platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", self.output_filename])
                elif platform.system() == "Windows":  # Windows
                    os.startfile(self.output_filename)
                else:  # Linux
                    subprocess.run(["xdg-open", self.output_filename])
            except Exception as e:
                messagebox.showerror("오류", f"파일을 열 수 없습니다:\n{str(e)}")
        else:
            messagebox.showwarning("알림", "열 수 있는 파일이 없습니다.")
    
    def open_folder(self):
        """저장 폴더 열기"""
        try:
            folder_path = self.save_path.get()
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            elif platform.system() == "Windows":  # Windows
                os.startfile(folder_path)
            else:  # Linux
                subprocess.run(["xdg-open", folder_path])
        except Exception as e:
            messagebox.showerror("오류", f"폴더를 열 수 없습니다:\n{str(e)}")
    
    def show_login_confirmation_dialog(self):
        """로그인 완료 확인 대화상자"""
        # 대화상자 결과를 저장할 변수
        result = [False]  # 리스트로 감싸서 클로저에서 수정 가능하게 함
        dialog_closed = [False]
        
        def show_dialog():
            # 커스텀 대화상자 생성
            dialog = tk.Toplevel(self.root)
            dialog.title("🔐 로그인 확인")
            dialog.geometry("450x250")
            dialog.resizable(False, False)
            
            # 항상 맨 앞에 표시
            dialog.transient(self.root)
            dialog.grab_set()
            
            # 중앙 정렬
            dialog.geometry("+{}+{}".format(
                self.root.winfo_rootx() + 100,
                self.root.winfo_rooty() + 100
            ))
            
            # 메시지 프레임
            msg_frame = ttk.Frame(dialog, padding="30")
            msg_frame.pack(fill=tk.BOTH, expand=True)
            
            # 아이콘과 메시지
            ttk.Label(msg_frame, text="🔐", font=("Arial", 32)).pack(pady=(0, 15))
            ttk.Label(msg_frame, text="네이버 로그인이 완료되었나요?", 
                     font=("Arial", 14, "bold")).pack(pady=(0, 10))
            ttk.Label(msg_frame, text="1. 크롬 창에서 네이버에 로그인하세요\n2. 로그인이 완료되면 아래 버튼을 클릭하세요", 
                     font=("Arial", 11), foreground="gray", justify=tk.CENTER).pack(pady=(0, 25))
            
            # 버튼 프레임
            btn_frame = ttk.Frame(msg_frame)
            btn_frame.pack()
            
            def on_confirm():
                result[0] = True
                dialog_closed[0] = True
                dialog.destroy()
            
            def on_cancel():
                result[0] = False
                dialog_closed[0] = True
                dialog.destroy()
            
            # 버튼들
            confirm_btn = ttk.Button(btn_frame, text="✅ 로그인 완료", command=on_confirm)
            confirm_btn.pack(side=tk.LEFT, padx=(0, 15), ipadx=10, ipady=5)
            
            cancel_btn = ttk.Button(btn_frame, text="❌ 취소", command=on_cancel)
            cancel_btn.pack(side=tk.LEFT, ipadx=10, ipady=5)
            
            # 기본 포커스를 확인 버튼에
            confirm_btn.focus_set()
            
            # Enter 키로 확인, Escape 키로 취소
            dialog.bind('<Return>', lambda e: on_confirm())
            dialog.bind('<Escape>', lambda e: on_cancel())
            
            # 창 닫기 버튼 처리
            dialog.protocol("WM_DELETE_WINDOW", on_cancel)
        
        # 메인 스레드에서 대화상자 표시
        self.root.after(0, show_dialog)
        
        # 대화상자가 닫힐 때까지 대기
        while not dialog_closed[0]:
            try:
                self.root.update()
                time.sleep(0.1)
            except tk.TclError:
                # 윈도우가 파괴된 경우
                break
        
        return result[0]

    # 기존 main.py의 함수들을 여기에 복사
    def switch_to_article_frame(self, driver):
        """게시글 iframe으로 전환 - main.py와 동일한 방식"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # 최상위에서 모든 iframe을 뒤져서, 게시글 ID가 src에 포함된 iframe으로 전환
                driver.switch_to.default_content()  # 최상위 프레임으로 전환
                
                for f in driver.find_elements(By.TAG_NAME, "iframe"):
                    src = f.get_attribute("src") or ""
                    self.log_message(f"[DEBUG] iframe src 확인: {src}")
                    if str(self.current_post_id) in src:
                        self.log_message(f"[DEBUG] 목표 게시글 {self.current_post_id} iframe 찾음!")
                        driver.switch_to.frame(f)
                        return True
                return False
            except (StaleElementReferenceException, WebDriverException) as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(3)
        return False

    def parse_comments_reverse(self, driver):
        """역순으로 댓글 수집 - main.py와 동일한 방식"""
        all_comments = []
        max_retries = 3

        self.log_message("🚀 역순 댓글 수집을 시작합니다...")

        # 1) 게시글 iframe으로 전환
        if not self.switch_to_article_frame(driver):
            raise RuntimeError("▶︎ 게시글 iframe을 찾을 수 없습니다.")

        # 2) 맨 뒤 버튼 클릭하여 마지막 페이지로 이동
        self.log_message("🔚 마지막 페이지로 이동 중...")
        
        # 클릭 전 현재 상태 확인
        self.log_message("[DEBUG] 클릭 전 페이지 상태 확인...")
        current_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
        self.log_message(f"[DEBUG] 클릭 전 페이지 버튼들: {[btn.text for btn in current_buttons]}")
        
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
                self.log_message(f"[DEBUG] 맨 뒤 버튼 찾음: {selector}")
                self.log_message(f"[DEBUG] 버튼 텍스트: '{last_btn[0].text}'")
                self.log_message(f"[DEBUG] 버튼 활성화 상태: {last_btn[0].is_enabled()}")
                
                # 클릭 실행
                last_btn[0].click()
                self.log_message("[DEBUG] 맨 뒤 버튼 클릭 완료")
                
                # 충분한 로딩 대기
                time.sleep(3)
                self.log_message("[DEBUG] 3초 대기 완료")
                
                # 클릭 후 상태 확인
                after_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
                self.log_message(f"[DEBUG] 클릭 후 페이지 버튼들: {[btn.text for btn in after_buttons]}")
                
                last_page_clicked = True
                break
        
        if not last_page_clicked:
            self.log_message("⚠️ 맨 뒤 버튼을 찾을 수 없습니다. 1페이지부터 시작합니다.")
            # 모든 버튼 확인해보기
            all_buttons = driver.find_elements(By.CSS_SELECTOR, "button, a")
            self.log_message(f"[DEBUG] 사용 가능한 모든 버튼들:")
            for i, btn in enumerate(all_buttons[:20]):  # 처음 20개만
                try:
                    self.log_message(f"[DEBUG] {i}: {btn.tag_name} - '{btn.text}' - class: {btn.get_attribute('class')}")
                except:
                    pass
        
        # 3) 현재 페이지 번호 확인 - 맨 뒤 버튼 클릭 후 또는 직접 감지
        self.log_message("[DEBUG] 마지막 페이지 번호 감지 중...")
        
        # 먼저 페이지 버튼들을 모두 확인해서 가장 큰 번호 찾기 (가장 확실한 방법)
        all_page_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
        page_numbers = []
        for btn in all_page_buttons:
            try:
                page_num = int(btn.text.strip())
                page_numbers.append(page_num)
                self.log_message(f"[DEBUG] 발견된 페이지 번호: {page_num}")
            except (ValueError, AttributeError):
                continue
        
        if page_numbers:
            current_page = max(page_numbers)
            self.log_message(f"🎯 감지된 마지막 페이지: {current_page}페이지 (버튼 분석)")
            
            # 맨 뒤 버튼이 없었지만 여러 페이지가 있는 경우 처리
            if not last_page_clicked and current_page > 1:
                self.log_message(f"[DEBUG] 맨 뒤 버튼 없이 {current_page}페이지 감지됨. 직접 이동합니다.")
                # 가장 큰 페이지 번호 버튼 클릭
                for btn in all_page_buttons:
                    try:
                        if int(btn.text.strip()) == current_page:
                            self.log_message(f"[DEBUG] 마지막 페이지 {current_page} 직접 클릭")
                            btn.click()
                            time.sleep(2)
                            break
                    except (ValueError, AttributeError):
                        continue
        else:
            # 페이지 버튼이 아예 없는 경우 (댓글이 매우 적음)
            self.log_message("[DEBUG] 페이지 버튼이 없음. 단일 페이지로 추정.")
            
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
                        self.log_message(f"🎯 활성 페이지로 감지: {current_page}페이지 (셀렉터: {selector})")
                        break
                    except (ValueError, AttributeError):
                        continue
            
            if current_page == 1:
                # 댓글이 있는지 확인
                comment_check = driver.find_elements(By.CSS_SELECTOR, "span.text_comment")
                if comment_check:
                    self.log_message("🎯 1페이지에 댓글이 있음을 확인했습니다.")
                else:
                    self.log_message("⚠️ 댓글을 찾을 수 없습니다. 빈 게시글일 수 있습니다.")

        # 4) 역순으로 댓글 수집 (마지막 → 첫 페이지)
        while current_page >= 1:
            for attempt in range(max_retries):
                try:
                    # iframe 재전환 (안전성)
                    if not self.switch_to_article_frame(driver):
                        raise RuntimeError("▶︎ 게시글 iframe을 찾을 수 없습니다.")

                    # 댓글 로딩 대기
                    time.sleep(1)
                    
                    # 댓글 요소 확인
                    comment_elements = driver.find_elements(By.CSS_SELECTOR, "span.text_comment")
                    if not comment_elements:
                        raise TimeoutException("댓글을 찾을 수 없습니다.")

                    # 댓글 수집 (main.py와 동일한 방식)
                    authors = driver.find_elements(By.CSS_SELECTOR, "a.comment_nickname")
                    texts = driver.find_elements(By.CSS_SELECTOR, "span.text_comment")
                    
                    if not authors or not texts:
                        self.log_message(f"[DEBUG] 페이지 {current_page}: 댓글 없음")
                        # 첫 페이지에서 댓글이 없으면 빈 게시글
                        if current_page == 1:
                            self.log_message("📝 이 게시글에는 댓글이 없습니다.")
                            return all_comments
                        break

                    self.log_message(f"[DEBUG] 페이지 {current_page} → {len(authors)}개 댓글 수집")
                    
                    # 텍스트 즉시 추출 (main.py와 동일한 방식)
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
                    self.log_message(f"⚠️ 오류 발생 (페이지 {current_page}): {str(e)}")
                    if attempt == max_retries - 1:
                        self.log_message(f"❌ 페이지 {current_page} 수집 실패")
                        break
                    time.sleep(1)

            # 5) 다음 페이지로 이동 (역순: current_page-1)
            if current_page > 1:
                next_page = current_page - 1
                self.log_message(f"⬅️ {next_page}페이지로 이동 중...")
                
                # 현재 보이는 페이지 버튼들 확인
                page_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
                self.log_message(f"[DEBUG] 현재 페이지 버튼들: {[btn.text for btn in page_buttons]}")
                
                # 목표 페이지 번호 버튼 찾아서 클릭
                target_clicked = False
                for btn in page_buttons:
                    try:
                        if int(btn.text.strip()) == next_page:
                            self.log_message(f"[DEBUG] 페이지 번호 직접 클릭: {btn.text}")
                            btn.click()
                            target_clicked = True
                            time.sleep(1.5)
                            break
                    except (ValueError, AttributeError):
                        continue
                
                # 목표 페이지가 현재 블록에 없으면 이전 블록으로 이동
                if not target_clicked:
                    self.log_message(f"[DEBUG] {next_page}페이지가 현재 블록에 없음. 이전 블록으로 이동...")
                    prev_block_btn = driver.find_elements(By.CSS_SELECTOR, "button.btn.type_prev")
                    if prev_block_btn and prev_block_btn[0].is_enabled():
                        self.log_message(f"[DEBUG] 이전 블록 버튼 클릭")
                        prev_block_btn[0].click()
                        time.sleep(1.5)
                        
                        # 블록 이동 후 다시 페이지 번호 클릭 시도
                        new_page_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.number")
                        self.log_message(f"[DEBUG] 이전 블록 이동 후 페이지 버튼들: {[btn.text for btn in new_page_buttons]}")
                        
                        for btn in new_page_buttons:
                            try:
                                if int(btn.text.strip()) == next_page:
                                    self.log_message(f"[DEBUG] 블록 이동 후 페이지 클릭: {btn.text}")
                                    btn.click()
                                    target_clicked = True
                                    time.sleep(1.5)
                                    break
                            except (ValueError, AttributeError):
                                continue
                    else:
                        self.log_message("⚠️ 이전 블록 버튼이 비활성화되어 있습니다.")
                
                if not target_clicked:
                    self.log_message(f"⚠️ {next_page}페이지로 이동할 수 없습니다.")
                    self.log_message(f"📋 현재까지 {len(all_comments)}개 댓글을 수집했습니다.")
                    break
            
            current_page -= 1
            
            # 1페이지 도달 시 종료
            if current_page < 1:
                self.log_message("✅ 모든 댓글 수집 완료! (1페이지 도달)")
                break

        return all_comments

    def navigate_to_page(self, driver, target_page):
        """특정 페이지로 이동 - 사용하지 않음 (main.py 방식 사용)"""
        pass

    def collect_page_comments(self, driver):
        """현재 페이지의 댓글 수집 - 사용하지 않음 (main.py 방식 사용)"""
        pass

    def count_prefix_and_users(self, comments):
        """[팀명] 형식 댓글 통계 - main.py와 동일한 방식"""
        from collections import defaultdict
        import re
        
        team_counts = defaultdict(int)
        user_counts = defaultdict(int)
        prefix_pattern = re.compile(r"^\[(.*?)\]")

        total_comments = len(comments)
        team_format_comments = 0

        for author, text in comments:  # 튜플 형태로 처리
            m = prefix_pattern.match(text)
            if m:  # [팀이름] 형식의 댓글만 처리
                team_counts[m.group(1)] += 1
                user_counts[author] += 1  # 사용자별 카운트도 [팀이름] 댓글만
                team_format_comments += 1

        self.log_message(f"\n📊 댓글 분석 결과:")
        self.log_message(f"   총 댓글 수: {total_comments:,}개")
        self.log_message(f"   [팀이름] 형식 댓글: {team_format_comments:,}개")
        self.log_message(f"   일반 댓글: {total_comments - team_format_comments:,}개")
        self.log_message(f"   팀별 댓글 합계: {sum(team_counts.values()):,}개")
        self.log_message(f"   사용자별 댓글 합계: {sum(user_counts.values()):,}개")
        self.log_message(f"   ✅ 합계 일치: {sum(team_counts.values()) == sum(user_counts.values())}")
        self.log_message(f"   발견된 팀 수: {len(team_counts)}개")
        self.log_message(f"   참여 사용자 수: {len(user_counts)}명")

        return dict(team_counts), dict(user_counts)

    def output_to_excel(self, team_counts, user_counts, filename):
        """Excel 파일로 저장"""
        # 팀별 댓글수 DataFrame 생성
        if team_counts:
            team_data = [(name, count) for name, count in team_counts.items()]
            team_df = pd.DataFrame(team_data)
            team_df.columns = ['팀이름', '댓글수']  # 컬럼명 별도 설정
            team_df = team_df.sort_values('댓글수', ascending=False)
        else:
            team_df = pd.DataFrame({'팀이름': [], '댓글수': []})
        
        # 사용자별 댓글수 DataFrame 생성
        if user_counts:
            user_data = [(name, count) for name, count in user_counts.items()]
            user_df = pd.DataFrame(user_data)
            user_df.columns = ['사용자이름', '댓글수']  # 컬럼명 별도 설정
            user_df = user_df.sort_values('댓글수', ascending=False)
        else:
            user_df = pd.DataFrame({'사용자이름': [], '댓글수': []})
        
        # Excel 파일로 저장
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            team_df.to_excel(writer, sheet_name='팀별댓글수', index=False)
            user_df.to_excel(writer, sheet_name='사용자별댓글수', index=False)


def main():
    root = tk.Tk()
    app = CafeCommentCollectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main() 