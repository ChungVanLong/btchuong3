import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Thông tin email
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Thư mục chứa backup
DB_FOLDER = "database"
BACKUP_FOLDER = "backup"

def backup_database():
    try:
        for filename in os.listdir(DB_FOLDER):
            if filename.endswith(".sql") or filename.endswith(".sqlite3"):
                file_path = os.path.join(DB_FOLDER, filename)
                backup_path = os.path.join(BACKUP_FOLDER, filename)
                shutil.copy(file_path, backup_path)

        print(f"Backup thành công lúc {time.strftime('%H:%M:%S')}")
        send_email("Backup thành công", "Các file cơ sở dữ liệu đã được backup thành công.")
    except Exception as e:
        print(f"Lỗi backup: {e}")
        send_email("Backup thất bại", f"Có lỗi xảy ra khi backup: {e}")

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"Đã gửi email thành công đến {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"Lỗi gửi email: {e}")

# Lên lịch chạy lúc 00:00 hàng ngày
schedule.every().day.at("00:00").do(backup_database)
print("Đã lên lịch backup database vào 00:00 mỗi ngày. Đang chạy...")

while True:
    schedule.run_pending()
    time.sleep(60)
