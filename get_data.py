import cv2
import os

# Khởi tạo camera và bộ dò khuôn mặt
cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
# Nhập ID và Tên cho người mới
face_id = input('\n Nhập ID : ')
face_name = input('\n Nhập Tên : ')

# Tạo thư mục con nếu chưa có (Dựa trên cấu trúc bạn đã tạo)
path = f"dataset/{face_name}"
if not os.path.exists(path):
    os.makedirs(path)

print("\n [INFO] Đang khởi động camera. Hãy nhìn thẳng vào camera và chờ...")
count = 0

while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        count += 1

        # Lưu ảnh vào thư mục dataset theo định dạng: User.ID.Count.jpg
        # Lưu ý: Chúng ta lưu ảnh xám để tiết kiệm bộ nhớ và hỗ trợ thuật toán LBPH
        file_name = f"User.{face_id}.{count}.jpg"
        cv2.imwrite(f"{path}/{file_name}", gray[y:y+h,x:x+w])

        cv2.imshow('Dang thu thap du lieu...', img)

    k = cv2.waitKey(100) & 0xff # Nhấn 'ESC' để thoát sớm
    if k == 27:
        break
    elif count >= 100: # Chụp 100 tấm rồi dừng
         break

print("\n [INFO] Đã xong! Đã lưu 30 ảnh vào thư mục:", path)
cam.release()
cv2.destroyAllWindows()