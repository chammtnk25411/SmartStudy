from models.plan import Plan
from models.plans import Plans

file_name = '../datasets/StudyPlans.json'

p1 = Plan('p1','Ôn tập đại số','Toán','15/03/2026','19:00','19:50',50,'npmai95')
p2 = Plan('p2','Luyện nghe cơ bản','Tiếng Anh','16/03/2026','20:00','20:50',50,'npmai95')
p3 = Plan('p3','Code bài Python cơ bản','Lập Trình','18/03/2026','21:00','21:50',50,'npmai95')

p4 = Plan('p4','Phân tích bài thơ','Ngữ Văn','17/03/2026','19:00','19:50',50,'đahanh69')
p5 = Plan('p5','Ôn tập lịch sử Việt Nam','Lịch Sử','18/03/2026','20:00','20:50',50,'đahanh69')
p6 = Plan('p6','Học bản đồ thế giới','Địa Lý','19/03/2026','21:00','21:50',50,'đahanh69')

p7 = Plan('p7','Giải bài tập lực học','Vật Lý','16/03/2026','19:00','19:50',50,'ntlan99')
p8 = Plan('p8','Học phản ứng hóa học','Hóa Học','17/03/2026','20:00','20:50',50,'ntlan99')
p9 = Plan('p9','Ôn tập sinh học','Sinh Học','18/03/2026','21:00','21:50',50,'ntlan99')

p10 = Plan('p10','Thực hành Word','Tin học','15/03/2026','19:00','19:50',50,'dttrinh85')
p11 = Plan('p11','Code OOP Python','Lập Trình','17/03/2026','20:00','20:50',50,'dttrinh85')
p12 = Plan('p12','Tìm hiểu AI cơ bản','AI','18/03/2026','21:00','21:50',50,'dttrinh85')

p13 = Plan('p13','Học marketing online','Marketing','16/03/2026','19:00','19:50',50,'ntchau72')
p14 = Plan('p14','Luyện giao tiếp','Kỹ năng mềm','18/03/2026','20:00','20:50',50,'ntchau72')
p15 = Plan('p15','Thiết kế banner','Thiết kế','19/03/2026','21:00','21:50',50,'ntchau72')

p16 = Plan('p16','Ôn hình học','Toán','14/03/2026','19:00','19:50',50,'pkgiang95')
p17 = Plan('p17','Giải bài tập điện','Vật Lý','17/03/2026','20:00','20:50',50,'pkgiang95')
p18 = Plan('p18','Ôn hóa hữu cơ','Hóa Học','18/03/2026','21:00','21:50',50,'pkgiang95')

p19 = Plan('p19','Ôn sinh học tế bào','Sinh Học','16/03/2026','19:00','19:50',50,'nhtrang11')
p20 = Plan('p20','Học địa lý tự nhiên','Địa Lý','17/03/2026','20:00','20:50',50,'nhtrang11')
p21 = Plan('p21','Ôn lịch sử thế giới','Lịch Sử','18/03/2026','21:00','21:50',50,'nhtrang11')

p22 = Plan('p22','Code web cơ bản','Lập Trình','15/03/2026','19:00','19:50',50,'đthai73')
p23 = Plan('p23','Tìm hiểu AI nâng cao','AI','18/03/2026','20:00','20:50',50,'đthai73')
p24 = Plan('p24','Phân tích dữ liệu','Data','19/03/2026','21:00','21:50',50,'đthai73')

p25 = Plan('p25','Soạn bài văn','Ngữ Văn','16/03/2026','19:00','19:50',50,'hglan35')
p26 = Plan('p26','Học từ vựng mới','Tiếng Anh','17/03/2026','20:00','20:50',50,'hglan35')
p27 = Plan('p27','Rèn kỹ năng mềm','Kỹ năng mềm','18/03/2026','21:00','21:50',50,'hglan35')

p28 = Plan('p28','Thiết kế logo','Thiết kế','15/03/2026','19:00','19:50',50,'hpphuong58')
p29 = Plan('p29','Học chiến lược marketing','Marketing','17/03/2026','20:00','20:50',50,'hpphuong58')
p30 = Plan('p30','Xử lý dữ liệu Excel','Data','18/03/2026','21:00','21:50',50,'hpphuong58')

p31 = Plan('p31','Ôn công thức toán','Toán','14/03/2026','19:00','19:50',50,'tthanh25')
p32 = Plan('p32','Thực hành Excel','Tin học','17/03/2026','20:00','20:50',50,'tthanh25')
p33 = Plan('p33','Học AI cơ bản','AI','18/03/2026','21:00','21:50',50,'tthanh25')

p34 = Plan('p34','Ôn lịch sử VN','Lịch Sử','15/03/2026','19:00','19:50',50,'hmphuong15')
p35 = Plan('p35','Học địa lý châu Á','Địa Lý','17/03/2026','20:00','20:50',50,'hmphuong15')
p36 = Plan('p36','Phân tích văn bản','Ngữ Văn','18/03/2026','21:00','21:50',50,'hmphuong15')

p37 = Plan('p37','Ôn hóa vô cơ','Hóa Học','16/03/2026','19:00','19:50',50,'phgiang41')
p38 = Plan('p38','Ôn sinh học','Sinh Học','17/03/2026','20:00','20:50',50,'phgiang41')
p39 = Plan('p39','Giải bài tập vật lý','Vật Lý','18/03/2026','21:00','21:50',50,'phgiang41')

p40 = Plan('p40','Học marketing căn bản','Marketing','15/03/2026','19:00','19:50',50,'ptphuong83')
p41 = Plan('p41','Thiết kế slide','Thiết kế','17/03/2026','20:00','20:50',50,'ptphuong83')
p42 = Plan('p42','Luyện kỹ năng thuyết trình','Kỹ năng mềm','18/03/2026','21:00','21:50',50,'ptphuong83')

p43 = Plan('p43','Ôn toán nâng cao','Toán','14/03/2026','19:00','19:50',50,'bhhung23')
p44 = Plan('p44','Code thuật toán','Lập Trình','17/03/2026','20:00','20:50',50,'bhhung23')
p45 = Plan('p45','Học AI thực hành','AI','18/03/2026','21:00','21:50',50,'bhhung23')

p46 = Plan('p46','Luyện phát âm','Tiếng Anh','15/03/2026','19:00','19:50',50,'hkhai63')
p47 = Plan('p47','Ôn văn học','Ngữ Văn','17/03/2026','20:00','20:50',50,'hkhai63')
p48 = Plan('p48','Ôn lịch sử','Lịch Sử','18/03/2026','21:00','21:50',50,'hkhai63')

p49 = Plan('p49','Học địa lý Việt Nam','Địa Lý','16/03/2026','19:00','19:50',50,'htlinh14')
p50 = Plan('p50','Ôn sinh học nâng cao','Sinh Học','18/03/2026','20:00','20:50',50,'htlinh14')
p51 = Plan('p51','Phân tích dữ liệu cơ bản','Data','18/03/2026','19:00','19:50',50,'pkduy26')
p52 = Plan('p52','Học Machine Learning','AI','19/03/2026','20:00','20:50',50,'pkduy26')
p53 = Plan('p53','Thực hành Python nâng cao','Lập Trình','20/03/2026','21:00','21:50',50,'pkduy26')

p54 = Plan('p54','Ôn tập hình học','Toán','17/03/2026','19:00','19:50',50,'btquan44')
p55 = Plan('p55','Giải bài tập vật lý','Vật Lý','18/03/2026','20:00','20:50',50,'btquan44')
p56 = Plan('p56','Ôn hóa hữu cơ','Hóa Học','19/03/2026','21:00','21:50',50,'btquan44')

p57 = Plan('p57','Soạn bài văn nghị luận','Ngữ Văn','16/03/2026','19:00','19:50',50,'ltduy63')
p58 = Plan('p58','Luyện viết tiếng Anh','Tiếng Anh','18/03/2026','20:00','20:50',50,'ltduy63')
p59 = Plan('p59','Rèn kỹ năng thuyết trình','Kỹ năng mềm','19/03/2026','21:00','21:50',50,'ltduy63')

p60 = Plan('p60','Học chiến lược marketing','Marketing','17/03/2026','19:00','19:50',50,'ptlan45')
p61 = Plan('p61','Thiết kế poster quảng cáo','Thiết kế','18/03/2026','20:00','20:50',50,'ptlan45')
p62 = Plan('p62','Phân tích dữ liệu khách hàng','Data','20/03/2026','21:00','21:50',50,'ptlan45')

p63 = Plan('p63','Ôn công thức toán','Toán','15/03/2026','19:00','19:50',50,'dthung72')
p64 = Plan('p64','Thực hành Excel nâng cao','Tin học','18/03/2026','20:00','20:50',50,'dthung72')
p65 = Plan('p65','Code bài tập Python','Lập Trình','19/03/2026','21:00','21:50',50,'dthung72')

p66 = Plan('p66','Ôn lịch sử thế giới','Lịch Sử','16/03/2026','19:00','19:50',50,'httrinh30')
p67 = Plan('p67','Học địa lý Việt Nam','Địa Lý','18/03/2026','20:00','20:50',50,'httrinh30')
p68 = Plan('p68','Phân tích tác phẩm văn học','Ngữ Văn','19/03/2026','21:00','21:50',50,'httrinh30')

p69 = Plan('p69','Học AI cơ bản','AI','17/03/2026','19:00','19:50',50,'vphanh83')
p70 = Plan('p70','Xử lý dữ liệu Python','Data','18/03/2026','20:00','20:50',50,'vphanh83')
p71 = Plan('p71','Code web frontend','Lập Trình','20/03/2026','21:00','21:50',50,'vphanh83')

p72 = Plan('p72','Ôn toán nâng cao','Toán','15/03/2026','19:00','19:50',50,'bhlong82')
p73 = Plan('p73','Giải bài tập vật lý','Vật Lý','18/03/2026','20:00','20:50',50,'bhlong82')
p74 = Plan('p74','Ôn hóa học cơ bản','Hóa Học','19/03/2026','21:00','21:50',50,'bhlong82')

p75 = Plan('p75','Học sinh học tế bào','Sinh Học','16/03/2026','19:00','19:50',50,'hgchau72')
p76 = Plan('p76','Ôn địa lý tự nhiên','Địa Lý','18/03/2026','20:00','20:50',50,'hgchau72')
p77 = Plan('p77','Ôn lịch sử Việt Nam','Lịch Sử','19/03/2026','21:00','21:50',50,'hgchau72')

p78 = Plan('p78','Luyện nghe tiếng Anh','Tiếng Anh','17/03/2026','19:00','19:50',50,'nkha66')
p79 = Plan('p79','Soạn bài văn','Ngữ Văn','18/03/2026','20:00','20:50',50,'nkha66')
p80 = Plan('p80','Rèn kỹ năng giao tiếp','Kỹ năng mềm','20/03/2026','21:00','21:50',50,'nkha66')

p81 = Plan('p81','Thiết kế logo','Thiết kế','16/03/2026','19:00','19:50',50,'nkngan35')
p82 = Plan('p82','Học marketing online','Marketing','18/03/2026','20:00','20:50',50,'nkngan35')
p83 = Plan('p83','Phân tích dữ liệu cơ bản','Data','19/03/2026','21:00','21:50',50,'nkngan35')

p84 = Plan('p84','Ôn toán cơ bản','Toán','15/03/2026','19:00','19:50',50,'btbao77')
p85 = Plan('p85','Luyện viết tiếng Anh','Tiếng Anh','18/03/2026','20:00','20:50',50,'btbao77')
p86 = Plan('p86','Soạn bài văn học','Ngữ Văn','19/03/2026','21:00','21:50',50,'btbao77')

p87 = Plan('p87','Code backend cơ bản','Lập Trình','17/03/2026','19:00','19:50',50,'hqbao79')
p88 = Plan('p88','Tìm hiểu AI nâng cao','AI','18/03/2026','20:00','20:50',50,'hqbao79')
p89 = Plan('p89','Xử lý dữ liệu lớn','Data','20/03/2026','21:00','21:50',50,'hqbao79')

p90 = Plan('p90','Ôn tập tổng hợp','Kỹ năng mềm','18/03/2026','19:00','19:50',50,'hqbao79')
lp = Plans()
plans = []
for i in range(1, 91):
    plans.append(globals()[f"p{i}"])
lp.add_items(plans)
lp.export_json(file_name)

