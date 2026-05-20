import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestContextMenu:
    def setup_method(self):
        # Cấu hình chống treo hệ thống trên Linux
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/context_menu'

    def teardown_method(self):
        time.sleep(4) # [DEMO] Nghỉ 4s để khán giả nhìn kết quả
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # CÁC KỊCH BẢN KIỂM THỬ
    # ─────────────────────────────────────────────────────────────────

    def test_tc1_kiem_tra_giao_dien_goc(self):
        """TC1: Static Test - Kiểm tra Giao diện trang Context Menu"""
        self.driver.get(self.url)
        time.sleep(4) # [DEMO] Chờ web load
        
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Context Menu" == header

    def test_tc2_context_menu_success_and_cleanup(self):
        """TC2: Right-click kích hoạt cảnh báo JS & đảm bảo dọn dẹp trạng thái"""
        self.driver.get(self.url)
        hot_spot = self.wait.until(EC.visibility_of_element_located((By.ID, "hot-spot")))
        time.sleep(2) # [DEMO]
        
        # Dùng ActionChains để Click CHUỘT PHẢI
        actions = ActionChains(self.driver)
        actions.context_click(hot_spot).perform()
        
        # Chờ cái bảng thông báo (Alert) của trình duyệt hiện lên
        self.wait.until(EC.alert_is_present())
        time.sleep(2) # [DEMO] Đóng băng để lớp nhìn thấy Alert bật ra
        
        # Switch focus sang cái Alert đó
        alert = self.driver.switch_to.alert
        
        try:
            # Kiểm tra chữ trên Alert
            assert "You selected a context menu" == alert.text
        finally:
            # [Fail-Safe] Luôn luôn bấm OK để đóng Alert dù code có lỗi hay không
            time.sleep(2) # [DEMO]
            alert.accept()

    def test_tc3_left_click_ignores_menu(self):
        """TC3: Negative - Click chuột TRÁI sẽ KHÔNG kích hoạt cảnh báo"""
        self.driver.get(self.url)
        hot_spot = self.wait.until(EC.visibility_of_element_located((By.ID, "hot-spot")))
        time.sleep(2)
        
        # Click chuột TRÁI bình thường
        actions = ActionChains(self.driver)
        actions.click(hot_spot).perform()
        time.sleep(2) # [DEMO] Chờ để chứng minh không có gì xảy ra
        
        # Khai báo một bộ đếm giờ ngắn gọn (2 giây)
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(EC.alert_is_present())
            pytest.fail("FAILED: Bị lỗi vì click chuột trái mà Alert vẫn hiện lên.")
        except TimeoutException:
            # Mong đợi rơi vào đây (Timeout vì đợi 2s không thấy Alert nào)
            assert True

    def test_tc4_boundary_click_outside_hotspot(self):
        """TC4: Boundary Test - Click chuột phải BÊN NGOÀI hộp KHÔNG ĐƯỢC kích hoạt cảnh báo"""
        self.driver.get(self.url)
        time.sleep(2)
        
        # Lấy tiêu đề trang làm điểm click (nằm ngoài cái hộp hotspot)
        outside_element = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
        
        # Click chuột PHẢI vào tiêu đề trang
        actions = ActionChains(self.driver)
        actions.context_click(outside_element).perform()
        time.sleep(2) # [DEMO]
        
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(EC.alert_is_present())
            self.driver.switch_to.alert.accept() # Dọn dẹp Alert lỡ hiện ra
            pytest.fail("FAILED: Lập trình viên code sai, click ngoài hộp mà vẫn hiện Alert.")
        except TimeoutException:
            assert True