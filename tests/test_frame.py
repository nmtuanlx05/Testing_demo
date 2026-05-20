import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestFrames:
    def setup_method(self):
        # Cấu hình chống treo RAM trên Linux
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://the-internet.herokuapp.com"

    def teardown_method(self):
        time.sleep(4) # [DEMO] Chờ 4s để khán giả ngắm kết quả trước khi tắt
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # CÁC KỊCH BẢN KIỂM THỬ (HAPPY PATHS & GUI)
    # ─────────────────────────────────────────────────────────────────

    def test_tc1_kiem_tra_giao_dien_goc(self):
        """TC1: Static Test - Đảm bảo trang IFrame tải đúng tiêu đề"""
        self.driver.get(f"{self.base_url}/iframe")
        time.sleep(4) # [DEMO] 
        
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "An iFrame containing the TinyMCE WYSIWYG Editor" == header

    def test_tc2_iframe_nhap_du_lieu_thanh_cong(self):
        """TC2: Switch vào IFrame, xóa chữ cũ và gõ chữ mới"""
        self.driver.get(f"{self.base_url}/iframe")
        time.sleep(2) # [DEMO] Nhìn giao diện gốc
        
        # 1. Chuyển quyền điều khiển vào bên trong IFrame
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
        
        # 2. Tương tác với vùng soạn thảo (editor)
        editor = self.driver.find_element(By.ID, "tinymce")
        editor.clear() # Xóa dòng chữ mặc định
        time.sleep(2) # [DEMO] Nhìn thấy chữ bị xóa trắng
        
        payload = "Hello từ kịch bản Automation Test!"
        editor.send_keys(payload) # Gõ từng chữ một vào
        time.sleep(4) # [DEMO] Nhìn thấy chữ mới vừa được gõ xong
        
        # 3. Xác nhận và thoát ra ngoài
        assert payload == editor.text
        self.driver.switch_to.default_content() # QUAN TRỌNG: Lùi ra trang gốc

    def test_tc3_nested_frames_di_sau_vao_trong(self):
        """TC3: Khám phá Frame lồng nhau (Root -> Top -> Middle)"""
        self.driver.get(f"{self.base_url}/nested_frames")
        time.sleep(2)
        
        # Đi theo đúng cấu trúc gia phả: Phải vào Frame Cha (Top) rồi mới vào Frame Con (Middle)
        self.driver.switch_to.frame("frame-top")
        self.driver.switch_to.frame("frame-middle")
        time.sleep(2) # [DEMO]
        
        # Cào chữ trong cái Frame ở giữa
        content = self.driver.find_element(By.ID, "content").text
        assert "MIDDLE" == content.strip()
        
        self.driver.switch_to.default_content()

    # ─────────────────────────────────────────────────────────────────
    # CÁC KỊCH BẢN BẪY LỖI (SAD PATHS - ROBUSTNESS)
    # ─────────────────────────────────────────────────────────────────

    def test_tc4_sad_path_cach_ly_khong_gian(self):
        """TC4: Chứng minh khi chui vào IFrame, Bot sẽ bị "mù" với thế giới bên ngoài"""
        self.driver.get(f"{self.base_url}/iframe")
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
        
        # Đang ở trong IFrame, cố tình tìm thẻ <h3> nằm ở trang gốc bên ngoài
        try:
            self.driver.find_element(By.TAG_NAME, "h3")
            pytest.fail("FAILED: Lỗi bảo mật (Context Leak)! Bot nhìn xuyên thấu ra ngoài IFrame.")
        except NoSuchElementException:
            # Mong đợi rơi vào đây: Tìm không thấy thẻ h3 -> Báo Pass
            assert True

    def test_tc5_sad_path_nhay_coc_sibling(self):
        """TC5: Chứng minh không thể nhảy cóc giữa 2 Frame ngang hàng (Left -> Right)"""
        self.driver.get(f"{self.base_url}/nested_frames")
        
        # Bot đi từ Root -> Top -> Left
        self.driver.switch_to.frame("frame-top")
        self.driver.switch_to.frame("frame-left")
        
        # Đang ở Left, cố tình đòi nhảy thẳng sang nhà hàng xóm (Right)
        try:
            self.driver.switch_to.frame("frame-right")
            pytest.fail("FAILED: Cho phép nhảy cóc sai quy tắc DOM!")
        except NoSuchFrameException:
            # Mong đợi rơi vào đây: Hệ thống chặn lại báo lỗi -> Báo Pass
            assert True