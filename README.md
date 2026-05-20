# DemoTongQuan - Selenium Pytest Automation Testing

## 📌 Clone project về máy

```bash
git clone <link-repository>
```

Ví dụ:

```bash
git clone git@github.com:nmtuanlx05/Testing_demo.git
```

---

## 📂 Di chuyển vào thư mục project

```bash
cd DemoTongQuan
```

---

# 🐍 Tạo môi trường ảo Python (venv)

## Ubuntu / macOS

```bash
python3 -m venv venv
```

## Windows

```bash
python -m venv venv
```

---

# ▶️ Kích hoạt môi trường ảo

## Ubuntu / macOS

```bash
source venv/bin/activate
```

## Windows

```bash
venv\Scripts\activate
```

Sau khi activate sẽ thấy:

```bash
(venv)
```

ở đầu terminal.

---

# 📦 Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

Các thư viện chính:

- selenium
- pytest
- webdriver-manager
- requests
- pytest-html
- ...

---

# 🚀 Chạy test

## Chạy toàn bộ test

```bash
pytest
```

---

## Chạy 1 file test cụ thể

Ví dụ:

```bash
pytest tests/test_dynamic_loading.py
```

---

# 📄 Generate HTML Report

```bash
pytest --html=report.html
```

Sau khi chạy sẽ tạo file:

```bash
report.html
```

Mở file bằng trình duyệt để xem report.

---

# 📁 Cấu trúc project

```bash
DemoTongQuan/
│
├── tests/
├── selenium/
├── assets/
├── requirements.txt
├── report.html
└── README.md
```

---

# ⚠️ Lưu ý

Project sử dụng:

- Python 3
- Selenium
- Pytest
- Chrome Browser

---

# 👨‍💻 Git Workflow cơ bản

## Pull code mới

```bash
git pull
```

## Add code

```bash
git add .
```

## Commit code

```bash
git commit -m "message"
```

## Push code

```bash
git push
```

---

# 🔥 Tạo requirements.txt mới (nếu cài thêm thư viện)

```bash
pip freeze > requirements.txt
```
