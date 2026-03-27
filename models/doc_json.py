import json
import os


def test_read_history():
    file_path = "../datasets/history.json"

    if not os.path.exists(file_path):
        print("Lỗi: Không tìm thấy file history.json!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)


    print("--- THỐNG KÊ TỔNG ---")
    print(f"Tổng thời gian học: {data.get('tong_thoi_gian_hoc')} phút")
    print(f"Tổng thời gian nghỉ: {data.get('tong_thoi_gian_nghi')} phút")


    print("\n--- CHI TIẾT PHIÊN HỌC ---")
    for phien in data.get("danh_sach", []):
        print(f"Phiên số: {phien['phien_so']} | Ngày: {phien['ngay']} | Kết quả: {phien['ket_qua']}")


if __name__ == "__main__":
    test_read_history()