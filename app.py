from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
import base64
from camera import VideoCamera

app = Flask(__name__)

# Khởi tạo đối tượng camera để dùng bộ lọc faceCascade và recognizer
# Chúng ta không dùng VideoCapture của máy chủ để stream mà chỉ dùng bộ não AI
face_detector = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load dữ liệu đã huấn luyện
if os.path.exists('trainer/trainer.yml'):
    recognizer.read('trainer/trainer.yml')

# Danh sách tên khớp với ID (Huan ID 1, Ham ID 2)
names = ['None', 'Huan', 'Ham']

# Khởi tạo đối tượng để dùng hàm ghi Excel từ file camera.py
# (Giả định bạn đã có file camera.py chuẩn như mình đã viết trước đó)
logic_manager = VideoCamera()


@app.route('/')
def index():
    """Trang tự điểm danh: Người dùng tự soi cam của họ"""
    return render_template('index.html')


@app.route('/register')
def register():
    """Trang đăng ký: Người dùng tự chụp 100 ảnh gửi về máy bạn"""
    return render_template('register.html')


@app.route('/self_attendance', methods=['POST'])
def self_attendance():
    """Xử lý ảnh từ trình duyệt gửi về để điểm danh"""
    try:
        data = request.json
        image_data = data.get('image')

        # Giải mã ảnh Base64
        header, encoded = image_data.split(",", 1)
        data_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(data_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Nhận diện khuôn mặt
        faces = face_detector.detectMultiScale(gray, 1.2, 5)

        detected_name = "Unknown"
        for (x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # Nếu độ tin cậy tốt (< 75)
            if confidence < 75:
                if id < len(names):
                    detected_name = names[id]
                    # Gọi hàm ghi vào file Excel trên máy bạn
                    logic_manager.log_attendance(detected_name)

        return jsonify({"name": detected_name})
    except Exception as e:
        print(f"Lỗi điểm danh: {e}")
        return jsonify({"name": "Error"}), 500


@app.route('/upload_face', methods=['POST'])
def upload_face():
    """Xử lý ảnh đăng ký gửi về máy bạn"""
    try:
        data = request.json
        user_id = data.get('id')
        user_name = data.get('name')
        image_data = data.get('image')

        header, encoded = image_data.split(",", 1)
        data_bytes = base64.b64decode(encoded)

        path = os.path.join('dataset', str(user_name))
        if not os.path.exists(path):
            os.makedirs(path)

        count = len([f for f in os.listdir(path) if f.endswith('.jpg')]) + 1
        file_name = f"User.{user_id}.{count}.jpg"

        with open(os.path.join(path, file_name), "wb") as f:
            f.write(data_bytes)

        return jsonify({"status": "success", "count": count})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Chạy trên mọi địa chỉ để Ngrok có thể chuyển hướng vào
    app.run(host='0.0.0.0', port=5000, debug=True)