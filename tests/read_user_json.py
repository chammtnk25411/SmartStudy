from models.users import Users

u = Users()

u.import_json("../datasets/user.json")

print("Danh sách User:")
u.print_items()
print("Tổng số user:", len(u.list))