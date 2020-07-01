import fractions
import datetime

class AfterHoursDailyInfo:
    def __init__(
        self,
        code,
        date,
        totalShare,
        totalTurnover,
        openPrice,
        highestPrice,
        lowestPrice,
        closePrice):
        # 代碼
        self.Code = code
        # 日期
        # 國曆年轉為西元年
        parts = date.split('/')
        date = datetime.date(int(parts[0]) + 1911, int(parts[1]), int(parts[2]))
        self.Date = date
        # 成交股數
        self.TotalShare = int(totalShare)
        # 成交金額
        self.TotalTurnover = int(totalTurnover)
        # 開盤價
        self.OpenPrice = fractions.Fraction(openPrice)
        # 最高價
        self.HighestPrice = fractions.Fraction(highestPrice)
        # 最低價
        self.LowestPrice = fractions.Fraction(lowestPrice)
        # 收盤價
        self.ClosePrice = fractions.Fraction(closePrice)
    # 物件表達式
    def __repr__(self):
        return (
            f'class AfterHoursDailyInfo {{ '
            f'Code={self.Code}, '
            f'Date={self.Date:%Y-%m-%d}, '
            f'TotalShare={self.TotalShare}, '
            f'TotalTurnover={self.TotalTurnover}, '
            f'OpenPrice={float(self.OpenPrice):.2f}, '
            f'HighestPrice={float(self.HighestPrice):.2f}, '
            f'LowestPrice={float(self.LowestPrice):.2f}, '
            f'ClosePrice={float(self.ClosePrice):.2f} '
            f'}}'
        )
