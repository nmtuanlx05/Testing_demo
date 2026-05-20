import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestInfiniteScroll:
    def setup_method(self):
        # Bùa hộ mệnh chống treo RAM trên Linux
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/infinite_scroll'

    def teardown_method(self):
        time.sleep(4) # [DEMO] Chờ 4s để khán giả ngắm kết quả trước khi tắt
        self.driver.quit()

    # --- HÀM HỖ TRỢ (HELPER) ---
    def helper_get_paragraph_count(self):
        """Đếm số lượng khối văn bản (div.jscroll-added) đang tồn tại trên trang"""
        return len(self.driver.find_elements(By.CLASS_NAME, "jscroll-added"))

    # ─────────────────────────────────────────────────────────────────
    # CÁC KỊCH BẢN KIỂM THỬ
    # ─────────────────────────────────────────────────────────────────

    def test_tc1_kiem_tra_giao_dien_goc(self):
        """TC1: Static Test - Kiểm tra tiêu đề trang"""
        self.driver.get(self.url)
        time.sleep(4) # [DEMO]
        
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Infinite Scroll" == header

    def test_tc2_initial_content_load(self):
        """TC2: Đảm bảo có ít nhất 1 khối nội dung được load lúc mới mở web"""
        self.driver.get(self.url)
        time.sleep(2)
        
        # Đợi cho cái khối dữ liệu đầu tiên xuất hiện trong DOM
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jscroll-added")))
        count = self.helper_get_paragraph_count()
        
        # Khẳng định số đếm được phải >= 1
        assert count >= 1, "Lỗi: Vừa vào web màn hình bị trắng, không có text"

    def test_tc3_scroll_loads_more_content(self):
        """TC3: Cuộn chuột xuống đáy 3 lần và xác nhận DOM phình to ra"""
        self.driver.get(self.url)
        time.sleep(4) # [DEMO] Để khán giả nhìn độ dài trang web ban đầu
        
        # 1. Chụp lại số lượng thẻ div lúc chưa cuộn
        initial_count = self.helper_get_paragraph_count()
        
        # 2. Thực hiện vòng lặp cuộn chuột 3 lần
        for i in range(3):
            # Ép trình duyệt cuộn thẳng xuống đáy màn hình hiện tại
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # [QUAN TRỌNG] Phải đợi 4s để API gọi dữ liệu mới về và render ra HTML
            time.sleep(4) # [DEMO] Khán giả sẽ thấy text mới nhảy ra liên tục
            
        # 3. Đếm lại số lượng thẻ div sau khi đã cuộn 3 lần
        final_count = self.helper_get_paragraph_count()
        
        # 4. Xác nhận sự tăng trưởng dữ liệu
        assert final_count > initial_count, f"Lỗi: Cuộn rồi nhưng số block vẫn là {initial_count}"