from models.motivations import Motivations
from models.motivation import Motivation

file_name = "../datasets/motivations.json"

m1 = Motivation("m1", "Hôm nay cố gắng hơn hôm qua",'hanh11')
m2 = Motivation("m2", "Học từng chút mỗi ngày", 'hanh11')
m3 = Motivation("m3", "Kỷ luật tạo nên thành công",'hanh11')
m4 = Motivation("m4", "Đừng bỏ cuộc",'npmai95')
m5 = Motivation("m5", "Tập trung để đạt mục tiêu",'npmai95')
m6 = Motivation("m6", "Tập để đạt mục tiêu",'npmai95')
m7= Motivation('m7','Học, học nữa, học mãi','pkgiang95')
m10=Motivation('m8','annskj','cham')

lm = Motivations()
for m in [m1, m2, m3, m4, m5,m7,m10]:
    lm.add_item(m)
lm.export_json(file_name)