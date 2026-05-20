from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://the-internet.herokuapp.com/login"
VALID_USER = "tomsmith"
VALID_PASS = "SuperSecretPassword!"

def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)
    return driver

def login(driver, username, password):
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)

def get_flash_message(driver):
    try:
        flash = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "flash"))
        )
        return flash.text.replace("×", "").strip()
    except:
        return ""

def assert_equal(actual, expected, tc_name):
    if expected in actual:
        print(f"✅ PASS - {tc_name}")
    else:
        print(f"❌ FAIL - {tc_name}")
        print(f"   Expected: '{expected}'")
        print(f"   Actual  : '{actual}'")

# ----------------------------------------------------------------

def tc1_login_thanh_cong(driver):
    print("\n=== TC1: Đăng nhập thành công ===")
    driver.get(URL)
    login(driver, VALID_USER, VALID_PASS)
    assert_equal(driver.current_url, "/secure", "TC1 - Redirect đến trang secure")
    msg = get_flash_message(driver)
    assert_equal(msg, "You logged into a secure area!", "TC1 - Flash message thành công")

def tc2_sai_password(driver):
    print("\n=== TC2: Sai password ===")
    driver.get(URL)
    login(driver, VALID_USER, "wrongpassword")
    msg = get_flash_message(driver)
    assert_equal(msg, "Your password is invalid!", "TC2 - Thông báo sai password")
    assert_equal(driver.current_url, URL, "TC2 - Không redirect")

def tc3_sai_username(driver):
    print("\n=== TC3: Sai username ===")
    driver.get(URL)
    login(driver, "wronguser", VALID_PASS)
    msg = get_flash_message(driver)
    assert_equal(msg, "Your username is invalid!", "TC3 - Thông báo sai username")
    assert_equal(driver.current_url, URL, "TC3 - Không redirect")

def tc4_de_trong_ca_hai(driver):
    print("\n=== TC4: Để trống username và password ===")
    driver.get(URL)
    login(driver, "", "")
    msg = get_flash_message(driver)
    assert_equal(msg, "Your username is invalid!", "TC4 - Thông báo khi để trống")

def tc5_de_trong_password(driver):
    print("\n=== TC5: Để trống password ===")
    driver.get(URL)
    login(driver, VALID_USER, "")
    msg = get_flash_message(driver)
    assert_equal(msg, "Your password is invalid!", "TC5 - Thông báo khi thiếu password")

def tc6_de_trong_username(driver):
    print("\n=== TC6: Để trống username ===")
    driver.get(URL)
    login(driver, "", VALID_PASS)
    msg = get_flash_message(driver)
    assert_equal(msg, "Your username is invalid!", "TC6 - Thông báo khi thiếu username")

def tc7_logout(driver):
    print("\n=== TC7: Đăng xuất sau khi login ===")
    driver.get(URL)
    login(driver, VALID_USER, VALID_PASS)
    WebDriverWait(driver, 5).until(EC.url_contains("/secure"))
    driver.find_element(By.CSS_SELECTOR, "a.button.secondary").click()
    time.sleep(1)
    msg = get_flash_message(driver)
    assert_equal(msg, "You logged out of the secure area!", "TC7 - Flash message logout")
    assert_equal(driver.current_url, URL, "TC7 - Redirect về trang login")

def tc8_case_sensitive_username(driver):
    print("\n=== TC8: Username viết hoa (case sensitive) ===")
    driver.get(URL)
    login(driver, "TomSmith", VALID_PASS)
    msg = get_flash_message(driver)
    assert_equal(msg, "Your username is invalid!", "TC8 - Username phân biệt hoa thường")

def tc9_case_sensitive_password(driver):
    print("\n=== TC9: Password viết hoa (case sensitive) ===")
    driver.get(URL)
    login(driver, VALID_USER, "supersecretpassword!")
    msg = get_flash_message(driver)
    assert_equal(msg, "Your password is invalid!", "TC9 - Password phân biệt hoa thường")

def tc10_ky_tu_dac_biet(driver):
    print("\n=== TC10: Username chứa ký tự đặc biệt ===")
    driver.get(URL)
    login(driver, "!@#$%^&*()", VALID_PASS)
    msg = get_flash_message(driver)
    assert_equal(msg, "Your username is invalid!", "TC10 - Username ký tự đặc biệt")

# ----------------------------------------------------------------

def run_all():
    driver = setup()
    try:
        tc1_login_thanh_cong(driver)
        tc2_sai_password(driver)
        tc3_sai_username(driver)
        tc4_de_trong_ca_hai(driver)
        tc5_de_trong_password(driver)
        tc6_de_trong_username(driver)
        tc7_logout(driver)
        tc8_case_sensitive_username(driver)
        tc9_case_sensitive_password(driver)
        tc10_ky_tu_dac_biet(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("\n=== Hoàn thành tất cả test case ===")

run_all()