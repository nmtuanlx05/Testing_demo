import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestRedirectLink:
    def setup_method(self):
        # Cấu hình chống treo RAM trên Linux Ubuntu
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        
        # Lưu URL gốc và URL đích
        self.url_origin = 'https://the-internet.herokuapp.com/redirector'
        self.url_destination = 'https://the-internet.herokuapp.com/status_codes'

    def teardown_method(self):
        time.sleep(4) # [DEMO] Chờ 4s trước khi tắt để lớp kịp nhìn
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # CÁC KỊCH BẢN KIỂM THỬ
    # ─────────────────────────────────────────────────────────────────

    def test_tc1_kiem_tra_giao_dien_goc(self):
        """TC1: Kiểm tra Giao diện trang Redirector trước khi bấm"""
        self.driver.get(self.url_origin)
        time.sleep(4) 
        
        header = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "Redirection" == header

    def test_tc2_chuyen_huong_thanh_cong_URL(self):
        """TC2: Logic - Click link 'here' và kiểm tra chuyển sang trang Status Codes"""
        self.driver.get(self.url_origin)
        time.sleep(4) 

        self.driver.find_element(By.ID, "redirect").click()
        self.wait.until(EC.url_contains("status_codes"))
        time.sleep(4) 
        
        assert self.url_destination == self.driver.current_url

    def test_tc3_click_vao_status_code_200(self):
        """TC3: Ở trang đích, click tiếp vào link '200' và kiểm tra nội dung"""
        # Cho bot đi thẳng đến trang Status Codes luôn cho nhanh
        self.driver.get(self.url_destination)
        time.sleep(4) # [DEMO] Lớp đang nhìn trang Status Codes

        # Tìm link có chữ "200" và click vào nó
        link_200 = self.driver.find_element(By.LINK_TEXT, "200")
        link_200.click()

        # Chờ URL thay đổi thêm đuôi /200
        self.wait.until(EC.url_contains("status_codes/200"))
        time.sleep(4) # [DEMO] Lớp nhìn thấy trang báo mã lỗi 200
        
        # Cào text trên trang mới để xác nhận nó hiện đúng câu báo lỗi 200
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        assert "This page returned a 200 status code." in body_text

    def test_tc4_kiem_tra_nut_back_trinh_duyet(self):
        """TC4: Logic nâng cao - Click link '301' rồi nhấn nút 'Quay lại' trên trình duyệt"""
        self.driver.get(self.url_destination)

        # Lần này cho bot click vào link "301" để test cho đa dạng
        self.driver.find_element(By.LINK_TEXT, "301").click()
        self.wait.until(EC.url_contains("status_codes/301"))
        time.sleep(4) # [DEMO] Đang ở trang chi tiết mã lỗi 301

        # Bot tự động bấm nút Mũi tên quay lại (Back) trên trình duyệt
        self.driver.back()
        time.sleep(4) # [DEMO] Nhìn xem web có lùi về trang danh sách Status Codes không

        # Xác nhận URL đã lùi về đúng trang Status Codes ban đầu
        assert self.url_destination == self.driver.current_url