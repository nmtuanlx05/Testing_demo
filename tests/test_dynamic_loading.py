import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestDynamicLoading:
    def setup_method(self):
        # Bùa hộ mệnh chống tràn RAM trên Linux Ubuntu
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        
        # Cấp cho bot tối đa 15 giây kiên nhẫn (vì thanh loading load khá lâu)
        self.wait = WebDriverWait(self.driver, 15)
        self.base_url = 'https://the-internet.herokuapp.com/dynamic_loading'

    def teardown_method(self):
        time.sleep(4) # [DEMO] Khán giả ngắm kết quả trước khi trình duyệt tắt
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # CÁC KỊCH BẢN KIỂM THỬ
    # ─────────────────────────────────────────────────────────────────

    def test_tc1_kiem_tra_giao_dien_goc(self):
        """TC1: Kiểm tra Giao diện trang chủ Dynamic Loading"""
        self.driver.get(self.base_url)
        time.sleep(4) # [DEMO]
        
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Dynamically Loaded Page Elements" == header

    def test_tc2_hidden_element(self):
        """TC2: Example 1 - Khởi chạy phần tử bị ẩn (Hidden Element)"""
        self.driver.get(f"{self.base_url}/1")
        time.sleep(2)

        # Bấm nút Start
        self.driver.find_element(By.CSS_SELECTOR, "#start button").click()

        # [TINH HOA SQA] Chờ cho đến khi thanh loading biến mất
        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
        
        # Lấy chữ Hello World và so sánh
        finish_text = self.driver.find_element(By.ID, "finish").text
        assert "Hello World!" == finish_text

    def test_tc3_rendered_element(self):
        """TC3: Example 2 - Khởi chạy phần tử được render mới vào DOM"""
        self.driver.get(f"{self.base_url}/2")
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "#start button").click()

        # [TINH HOA SQA] Phải đợi phần tử thực sự XUẤT HIỆN trong HTML DOM
        finish_element = self.wait.until(EC.presence_of_element_located((By.ID, "finish")))
        
        assert "Hello World!" == finish_element.text

    def test_tc4_robustness_double_click(self):
        """TC4: Robustness - Nháy đúp chuột liên tục vào nút Start xem web có sập không"""
        self.driver.get(f"{self.base_url}/1")
        time.sleep(2)

        start_button = self.driver.find_element(By.CSS_SELECTOR, "#start button")
        
        # Cố tình click 2 lần cực nhanh
        start_button.click()
        try:
            start_button.click()
        except Exception:
            pass # Bỏ qua lỗi văng ra nếu nút Start đã bị ẩn đi sau cú click đầu tiên

        # Hệ thống vẫn phải load bình thường mà không bị crash
        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
        finish_text = self.driver.find_element(By.ID, "finish").text
        
        assert "Hello World!" == finish_text