
import os
import sys

def get_base():
    """Lấy đường dẫn thư mục chứa file exe hoặc file py"""
    if getattr(sys, 'frozen', False):
        # Đang chạy từ file exe
        return os.path.dirname(sys.executable)
    else:
        # Đang chạy từ file py
        return os.path.dirname(os.path.abspath(__file__))

BASE = get_base()

def get_path(relative_path):
    """Trả về đường dẫn tuyệt đối"""
    return os.path.join(BASE, relative_path).replace("\\", "/")