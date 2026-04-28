import cv2
import numpy as np
import os
from PIL import Image

# Đường dẫn đến dataset và nơi lưu trainer
path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
# Nhớ đường dẫn file xml phải chuẩn như bước trước nhé
detector = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")


def getImagesAndLabels(path):
    imagePaths = []
    # Quét tất cả thư mục con trong dataset
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                imagePaths.append(os.path.join(root, file))

    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        # Chuyển ảnh sang thang độ xám (Grayscale)
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        # Lấy ID từ tên file (Ví dụ: User.1.15.jpg -> lấy số 1)
        # Tùy thuộc vào cách bạn đặt tên ở file get_data.py
        try:
            filename = os.path.split(imagePath)[-1]
            id = int(filename.split(".")[1])

            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        except Exception as e:
            print(f"Lỗi khi xử lý file {imagePath}: {e}")

    return faceSamples, ids


print("\n [INFO] Đang huấn luyện dữ liệu khuôn mặt. Vui lòng chờ...")
faces, ids = getImagesAndLabels(path)

if len(faces) > 0:
    recognizer.train(faces, np.array(ids))
    # Lưu model vào thư mục trainer
    recognizer.write('trainer/trainer.yml')
    print(f"\n [INFO] Đã huấn luyện xong {len(np.unique(ids))} khuôn mặt.")
else:
    print("\n [ERROR] Không tìm thấy dữ liệu khuôn mặt để huấn luyện.")