import json
import os
import random
from datetime import datetime, timedelta


def generate_mock_history():
    users = ["npmai95", "đahanh69", "ntlan99", "dttrinh85", "ntchau72",
             "pkgiang95", "nhtrang11", "đthai73", "hglan35", "hpphuong58"]
    subjects = ["Toán", "Tiếng Anh", "Lập Trình", "Ngữ Văn", "Vật Lý", "Hóa Học", "Data", "AI"]
    statuses = ["Hoàn thành", "Hoàn thành", "Hoàn thành", "Kết thúc sớm"]  # Tỉ lệ hoàn thành cao hơn

    history_data = {"datasets": []}
    today = datetime.now()

    session_counter = 1

    print("Đang tạo dữ liệu giả lập cho 7 ngày qua...")
    for days_ago in range(7, -1, -1):
        current_date = today - timedelta(days=days_ago)
        date_str_short = current_date.strftime("%d%m%Y")
        daily_users = random.sample(users, k=random.randint(4, 10))

        for u in daily_users:
            for _ in range(random.randint(1, 3)):
                h = random.randint(0, 2)
                m = random.randint(0, 59)
                if h == 0 and m < 30: m = random.randint(30, 59)  # Bắt học ít nhất 30p
                s = random.randint(0, 59)

                duration_str = f"{h}h {m}m {s}s"
                start_hour = random.randint(8, 22)
                start_min = random.randint(0, 59)
                date_time_str = f"{current_date.strftime('%d/%m/%Y')} {start_hour:02d}:{start_min:02d}"

                history_id = f"{u}_{date_str_short}_phien{session_counter}"

                session = {
                    "HistoryId": history_id,
                    "Username": u,
                    "Session": session_counter,
                    "Date": date_time_str,
                    "Duration": duration_str,
                    "Result": random.choice(statuses),
                    "Subject": random.choice(subjects)
                }

                history_data["datasets"].append(session)
                session_counter += 1
    history_data["datasets"].append({
        "HistoryId": "hanh11_hack_phien1",
        "Username": "hanh11",
        "Session": 99,
        "Date": today.strftime("%d/%m/%Y 10:00"),
        "Duration": "0h 0m 2s",
        "Result": "Kết thúc sớm",
        "Subject": "Tự học"
    })
    file_path = "../datasets/history.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4, ensure_ascii=False)

    print(f" Đã tạo thành công {len(history_data['datasets'])} phiên học giả vào file {file_path}!")


if __name__ == "__main__":
    generate_mock_history()