import cv2
import os
import numpy as np

# Khởi tạo bộ dò khuôn mặt
face_detector = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')


def process_existing_images(input_folder, face_id, face_name):
    # Tạo thư mục trong dataset
    path = f"dataset/{face_name}"
    if not os.path.exists(path):
        os.makedirs(path)

    count = 0
    # Đọc từng file trong thư mục đầu vào
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)
            if img is None: continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                count += 1
                # Cắt và lưu khuôn mặt
                face_img = gray[y:y + h, x:x + w]
                file_save_path = f"{path}/User.{face_id}.{count}.jpg"
                cv2.imwrite(file_save_path, face_img)
                print(f"Đã xử lý xong: {filename}")

    print(f"\n[SUCCESS] Đã nạp xong {count} ảnh của {face_name} vào hệ thống.")


# --- CÁCH DÙNG ---
# Bước 1: Tạo 1 thư mục tạm (VD: 'anh_hoc_sinh') và bỏ ảnh vào đó
# Bước 2: Chạy hàm dưới đây
input_dir = 'Ham'  # Thư mục chứa ảnh gốc bạn muốn nhập vào
user_id = input("Nhập ID: ")
user_name = input("Nhập tên: ")

process_existing_images(input_dir, user_id, user_name)