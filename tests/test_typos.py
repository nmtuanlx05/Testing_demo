import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestTypos:
    def setup_method(self):
        # Cấu hình chống treo RAM trên Linux Ubuntu
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/typos'

    def teardown_method(self):
        time.sleep(4) # [DEMO] Chờ 4s trước khi tắt để khán giả kịp nhìn
        self.driver.quit()

    # --- HÀM HỖ TRỢ (HELPER) ---
    def helper_get_paragraphs(self):
        """Lấy danh sách tất cả các đoạn văn bản (thẻ p) trên web"""
        return self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.example p")))

    # ─────────────────────────────────────────────────────────────────
    # CÁC KỊCH BẢN KIỂM THỬ
    # ─────────────────────────────────────────────────────────────────

    def test_tc1_kiem_tra_giao_dien_tinh(self):
        """TC1: Kiểm tra Giao diện - Đảm bảo tiêu đề và câu giới thiệu không bị sai"""
        self.driver.get(self.url)
        time.sleep(4) # [DEMO] Chờ web load xong
        
        # 1. Quét tìm thẻ Tiêu đề (h3)
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Typos" == header
        
        # 2. Quét thẻ đoạn văn số 1 (Nội dung này luôn cố định, không bị chập chờn)
        paragraphs = self.helper_get_paragraphs()
        first_paragraph = paragraphs[0].text.strip()
        expected_text = "This example demonstrates a typo being introduced. It does it randomly on each page load."
        
        assert expected_text == first_paragraph

    def test_tc2_tim_phien_ban_dung(self):
        """TC2: Logic - F5 liên tục đến khi tìm được đoạn văn đúng chính tả (won't)"""
        found_correct = False
        
        # Cho phép con bot F5 tối đa 10 lần
        for attempt in range(1, 11):
            self.driver.get(self.url)
            paragraphs = self.helper_get_paragraphs()
            second_paragraph = paragraphs[1].text.strip()
            
            # Nếu tìm thấy chữ đúng, đánh dấu là True và THOÁT vòng lặp
            if "won't" in second_paragraph:
                found_correct = True
                time.sleep(4) # [DEMO] Đóng băng 4s ngay tại khoảnh khắc tìm thấy chữ ĐÚNG
                break
                
        # Xác nhận cuối cùng
        assert found_correct == True, "F5 10 lần nhưng không ra được bản đúng"

    def test_tc3_bat_loi_typo(self):
        """TC3: Bug Hunting - F5 liên tục để cố tình tóm bằng được cái lỗi (won,t)"""
        found_typo = False
        
        for attempt in range(1, 11):
            self.driver.get(self.url)
            paragraphs = self.helper_get_paragraphs()
            second_paragraph = paragraphs[1].text.strip()
            
            # Cố tình rình bắt lỗi sai dấy phẩy
            if "won,t" in second_paragraph:
                found_typo = True
                time.sleep(4) # [DEMO] Đóng băng 4s ngay tại khoảnh khắc bắt được LỖI
                break
                
        # Khẳng định trang web này CÓ CHỨA LỖI 
        assert found_typo == True, "Web đã được Dev sửa xong, không còn lỗi won,t nữa"

