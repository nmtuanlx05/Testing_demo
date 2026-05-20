import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestKeyPresses:
    def setup_method(self):
        # Cấu hình chống treo RAM trên Linux
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/key_presses'

    def teardown_method(self):
        time.sleep(2)
        self.driver.quit()

    # --- HÀM HỖ TRỢ ---
    def get_result(self):
        """Hàm phụ tá: Chờ và cào dòng chữ kết quả màu xanh lá cây trả về"""
        return self.wait.until(EC.visibility_of_element_located((By.ID, "result"))).text

    # --- CÁC KỊCH BẢN KIỂM THỬ ---

    def test_tc1_kiem_tra_giao_dien(self):
        """TC1: Kiểm tra giao diện xem trang đã load đúng chưa"""
        self.driver.get(self.url)
        time.sleep(4)
        
        # Kiểm tra tiêu đề trang
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Key Presses" == header

    def test_tc2_special_keyboard_keys(self):
        """TC2: Gõ các phím đặc biệt (Space, Enter, Escape) vào không gian web"""
        self.driver.get(self.url)
        time.sleep(4) # [DEMO] Chờ load trang
        actions = ActionChains(self.driver)
        
        # Tạo danh sách các phím cần test
        test_payloads = [
            (Keys.SPACE, "SPACE"),
            (Keys.RETURN, "ENTER"),
            (Keys.ESCAPE, "ESCAPE")
        ]
        
        for key_obj, expected_str in test_payloads:
            actions.send_keys(key_obj).perform() # Bot thực hiện gõ phím
            time.sleep(4) # [DEMO] Dừng 2s để lớp kịp nhìn chữ hiện ra
            
            # Khẳng định chữ hiện ra phải đúng với phím vừa gõ
            assert f"You entered: {expected_str}" == self.get_result()

    def test_tc3_alphanumeric_keyboard_keys(self):
        """TC3: Gõ các phím chữ cái và số thông thường"""
        self.driver.get(self.url)
        time.sleep(4)
        actions = ActionChains(self.driver)
        
        test_payloads = [
            ("a", "A"), # Gõ a thường, web sẽ tự in hoa thành A
            ("7", "7")
        ]
        
        for char, expected in test_payloads:
            actions.send_keys(char).perform()
            time.sleep(4) # [DEMO] 
            assert f"You entered: {expected}" == self.get_result()

    