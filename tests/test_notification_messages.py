import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestNotificationMessages:
    def setup_method(self):
        # Cấu hình chống treo RAM trên Ubuntu
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/notification_message'
        
        # Danh sách các thông báo hợp lệ (Bao gồm cả lỗi sai chính tả của Dev)
        self.valid_messages = [
            "Action successful",
            "Action unsuccessful, please try again",
            "Action unsuccesful, please try again" # Lỗi thiếu chữ 's' từ phía Server
        ]

    def teardown_method(self):
        time.sleep(4) # [DEMO] Khán giả ngắm kết quả trước khi tắt
        self.driver.quit()

    # --- HÀM HỖ TRỢ (HELPER) ---
    def helper_get_flash_text(self):
        """Chờ banner hiện lên, lấy chữ, và GỌT BỎ dấu '×' ở cuối câu"""
        flash = self.wait.until(EC.visibility_of_element_located((By.ID, "flash")))
        # Lấy text, xóa ký tự × và cắt bỏ khoảng trắng thừa
        return flash.text.replace("×", "").strip()

    # ─────────────────────────────────────────────────────────────────
    # CÁC KỊCH BẢN KIỂM THỬ
    # ─────────────────────────────────────────────────────────────────

    def test_tc1_kiem_tra_giao_dien_goc(self):
        """TC1: Static Test - Kiểm tra tiêu đề trang"""
        self.driver.get(self.url)
        time.sleep(4) # [DEMO]
        
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Notification Message" == header

    def test_tc2_single_click(self):
        """TC2: Logic - Click 1 lần và kiểm tra nội dung banner báo về"""
        self.driver.get(self.url)
        time.sleep(2)
        
        # Click vào link
        self.driver.find_element(By.LINK_TEXT, "Click here").click()
        time.sleep(2) # [DEMO] Chờ lớp nhìn thấy banner hiện ra
        
        flash_text = self.helper_get_flash_text()
        
        # Dùng toán tử 'in' để xem câu báo về có nằm trong kho dữ liệu hợp lệ không
        assert flash_text in self.valid_messages

    def test_tc3_multi_click_randomness(self):
        """TC3: Robustness - Click 3 lần liên tục để test tính ngẫu nhiên của API"""
        self.driver.get(self.url)
        time.sleep(2)
        
        # Vòng lặp click 3 lần
        for i in range(3):
            self.driver.find_element(By.LINK_TEXT, "Click here").click()
            time.sleep(4) # [DEMO] Dừng 4s ở mỗi lần click để khán giả đọc được chữ mới
            
            flash_text = self.helper_get_flash_text()
            assert flash_text in self.valid_messages

    def test_tc4_dismiss_notification(self):
        """TC4: UI Interaction - Click nút (×) để đóng banner thông báo"""
        self.driver.get(self.url)
        
        # 1. Kích hoạt cho banner hiện lên
        self.driver.find_element(By.LINK_TEXT, "Click here").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "flash")))
        time.sleep(2) # [DEMO] Banner đang hiện
        
        # 2. Tìm cái nút X (có class là close) và bấm vào nó
        close_button = self.driver.find_element(By.CSS_SELECTOR, "a.close")
        close_button.click()
        
        # 3. [TINH HOA SQA] Chờ cho đến khi banner biến mất hoàn toàn
        self.wait.until(EC.invisibility_of_element_located((By.ID, "flash")))
        time.sleep(2) # [DEMO] Banner đã biến mất
        
        # Nếu code chạy được xuống đến đây mà không bị Timeout, tức là banner đã tắt thành công
        assert True