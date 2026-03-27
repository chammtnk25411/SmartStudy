class History:
    def __init__(self, HistoryId=None, Username=None, phien_so=None, ngay=None, thoi_gian=None, ket_qua=None, ten_mon=None):
        self.HistoryId = HistoryId
        self.Username = Username
        self.phien_so = phien_so
        self.ngay = ngay
        self.thoi_gian = thoi_gian
        self.ket_qua = ket_qua
        self.ten_mon = ten_mon

    def __str__(self):
        return f"{self.HistoryId}\t{self.Username}\t{self.phien_so}\t{self.ngay}\t{self.thoi_gian}\t{self.ket_qua}\t{self.ten_mon}"