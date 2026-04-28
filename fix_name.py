import os


def rename_files_in_folder(folder_path, user_id):
    # Lấy danh sách tất cả file trong thư mục
    files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

    count = 1
    for filename in files:
        # Tạo tên mới theo định dạng User.ID.STT.jpg
        new_name = f"User.{user_id}.{count}.jpg"

        # Đường dẫn cũ và mới
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        # Đổi tên
        os.rename(old_path, new_path)
        print(f"Đã đổi: {filename} -> {new_name}")
        count += 1


# --- THỰC THI ---
# Đổi tên cho thư mục Ham với ID là 2
rename_files_in_folder('dataset/Ham', 2)