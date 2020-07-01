import fractions

class Propotion:
    # 建構子
    def __init__(self, sort, code, name, percent):
        # 排序
        # 轉換為整數，以利後續排序使用
        self.Sort = int(sort)
        # 證券代碼
        self.Code = code
        # 證券名稱
        self.Name = name
        # 市值佔比
        # 不建議使用 float 進行浮點數保存，後續可能會造成浮點數計算誤差，
        # 使用 Fraction 保存才能有效降低浮點數計算結果的誤差
        self.Percent = fractions.Fraction(percent[:-1])
    # 物件表達式
    def __repr__(self):
        return (
            f'class Propotion {{ '
            f'Sort={self.Sort}, '
            f'Code={self.Code}, '
            f'Name={self.Name}, '
            f'Percent={float(self.Percent):.4f}% '
            f'}}'
        )