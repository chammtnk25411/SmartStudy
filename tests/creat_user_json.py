from models.user import User
from models.users import Users

u = Users()

admin = User(0,"Admin","admin","admin@gmail.com","123456","admin")

u1 = User(1,"Ngô Phương Mai","npmai95","ngophuongmai@gmail.com","558748","user")
u2 = User(2,"Đỗ Anh Hạnh","đahanh69","doanhhanh@gmail.com","760306","user")
u3 = User(3,"Nguyễn Tuấn Lan","ntlan99","nguyentuanlan@gmail.com","585812","user")
u4 = User(4,"Dương Thanh Trinh","dttrinh85","duongthanhtrinh@gmail.com","286645","user")
u5 = User(5,"Nguyễn Thanh Châu","ntchau72","nguyenthanhchau@gmail.com","066422","user")
u6 = User(6,"Phan Khánh Giang","pkgiang95","phankhanhgiang@gmail.com","939324","user")
u7 = User(7,"Ngô Hoài Trang","nhtrang11","ngohoaitrang@gmail.com","712773","user")
u8 = User(8,"Đỗ Tuấn Hải","đthai73","dotuanhai@gmail.com","205136","user")
u9 = User(9,"Hồ Gia Lan","hglan35","hogialan@gmail.com","417144","user")
u10 = User(10,"Hoàng Phương Phương","hpphuong58","hoangphuongphuong@gmail.com","709374","user")

u11 = User(11,"Trần Thị Hạnh","tthanh25","tranthihanh@gmail.com","490644","user")
u12 = User(12,"Hoàng Minh Phương","hmphuong15","hoangminhphuong@gmail.com","533274","user")
u13 = User(13,"Phan Hữu Giang","phgiang41","phanhuugiang@gmail.com","280780","user")
u14 = User(14,"Phạm Thanh Phương","ptphuong83","phamthanhphuong@gmail.com","254389","user")
u15 = User(15,"Bùi Hữu Hùng","bhhung23","buihuuhung@gmail.com","855659","user")
u16 = User(16,"Huỳnh Khánh Hải","hkhai63","huynhkhanhhai@gmail.com","324413","user")
u17 = User(17,"Hoàng Thị Linh","htlinh14","hoangthilinh@gmail.com","542790","user")
u18 = User(18,"Phạm Khánh Duy","pkduy26","phamkhanhduy@gmail.com","132452","user")
u19 = User(19,"Bùi Thị Quân","btquan44","buithiquan@gmail.com","770023","user")
u20 = User(20,"Lê Thị Duy","ltduy63","lethiduy@gmail.com","835232","user")

u21 = User(21,"Phạm Thị Lan","ptlan45","phamthilan@gmail.com","484012","user")
u22 = User(22,"Dương Thị Hùng","dthung72","duongthihung@gmail.com","539520","user")
u23 = User(23,"Huỳnh Thị Trinh","httrinh30","huynhthitrinh@gmail.com","366588","user")
u24 = User(24,"Võ Phương Hạnh","vphanh83","vophuonghanh@gmail.com","104617","user")
u25 = User(25,"Bùi Hoài Long","bhlong82","buihoailong@gmail.com","191374","user")
u26 = User(26,"Huỳnh Gia Châu","hgchau72","huynhgiachau@gmail.com","409815","user")
u27 = User(27,"Nguyễn Khánh Hà","nkha66","nguyenkhanhha@gmail.com","380146","user")
u28 = User(28,"Nguyễn Khánh Ngân","nkngan35","nguyenkhanhngan@gmail.com","823971","user")
u29 = User(29,"Bùi Thị Bảo","btbao77","buithibao@gmail.com","965355","user")
u30 = User(30,"Huỳnh Quang Bảo","hqbao79","huynhquangbao@gmail.com","224553","user")

u.add_items([admin,
u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,
u11,u12,u13,u14,u15,u16,u17,u18,u19,u20,
u21,u22,u23,u24,u25,u26,u27,u28,u29,u30
])

print("Danh sách User:")
u.print_items()

print("Xuất User ra Json:")
u.export_json("../datasets/user.json")