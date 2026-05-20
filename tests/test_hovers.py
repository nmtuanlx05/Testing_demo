import pytest
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Cấu hình bộ ghi log cơ bản
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestHovers:
    def setup_method(self):
        # 1. Cấu hình chống treo RAM trên Linux
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/hovers'
        self.driver.get(self.url) # Chuyển URL lên đây cho gọn

    def teardown_method(self):
        time.sleep(3)
        self.driver.quit()

    # --- HÀM HỖ TRỢ (HELPER) ---
    def helper_hover_figure(self, index):
        """
        Di chuột vào một bức ảnh (dựa trên vị trí index) và lấy thông tin bên trong.
        """
        logger.info(f"Đang tìm tất cả các bức ảnh trên trang...")
        # Lấy danh sách cả 3 bức ảnh (class = 'figure')
        figures = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "figure")))
        target_figure = figures[index]
        
        # Cuộn màn hình đến đúng bức ảnh đó cho dễ nhìn
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_figure)
        time.sleep(1) # [DEMO]
        
        logger.info(f"Tiến hành di chuột (Hover) vào bức ảnh số {index + 1}...")
        actions = ActionChains(self.driver)
        actions.move_to_element(target_figure).perform()
        time.sleep(3) # [DEMO] Dừng 3s để khán giả nhìn rõ giao diện khi bị Hover
        
        # Lấy thông tin hiện ra sau khi hover (Chữ H5 và Link)
        logger.info("Thu thập Tên user và Link profile...")
        caption = target_figure.find_element(By.CLASS_NAME, "figcaption")
        
        # Vì đã hover thật, ta lấy dữ liệu bình thường, không cần tiêm JS ép hiển thị nữa
        caption_header = caption.find_element(By.TAG_NAME, "h5").text
        profile_link = caption.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        return caption_header, profile_link

    # --- CÁC KỊCH BẢN KIỂM THỬ CỐT LÕI ---

    def test_tc1_kiem_tra_giao_dien(self):
        """TC1: Kiểm tra giao diện - Đảm bảo tiêu đề và câu hướng dẫn đúng chính tả"""
        time.sleep(3) # [DEMO] Chờ web load xong để lớp cùng xem
        
        # 1. Quét tìm thẻ Tiêu đề (h3)
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Hovers" == header
        
        # 2. Quét tìm thẻ Văn bản (p) chứa câu hướng dẫn
        instruction = self.driver.find_element(By.TAG_NAME, "p").text
        assert "Hover over the image for additional information" == instruction

    def test_tc2_hover_user1(self):
        """TC1: Hover vào User 1 và kiểm tra Tên + Link profile"""
        # Gọi helper và nhận về 2 kết quả
        user_name, profile_link = self.helper_hover_figure(0)
        
        # Xác nhận kết quả
        assert "name: user1" == user_name
        assert "/users/1" in profile_link

    def test_tc3_hover_user2(self):
        """TC2: Hover vào User 2 và kiểm tra Tên + Link profile"""
        user_name, profile_link = self.helper_hover_figure(1)
        
        assert "name: user2" == user_name
        assert "/users/2" in profile_link

    def test_tc4_hover_user3(self):
        """TC3: Hover vào User 3 và kiểm tra Tên + Link profile"""
        user_name, profile_link = self.helper_hover_figure(2)
        
        assert "name: user3" == user_name
        assert "/users/3" in profile_link