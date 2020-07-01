import fractions

class AfterHoursInfo:
    def __init__(
        self,
        code,
        name,
        totalShare,
        totalTurnover,
        openPrice,
        highestPrice,
        lowestPrice,
        closePrice):
        # 代碼
        self.Code = code
        # 名稱
        self.Name = name
        # 成交股數
        self.TotalShare = self.checkNumber(totalShare)
        if self.TotalShare is not None:
            self.TotalShare = int(totalShare)
        # 成交金額
        self.TotalTurnover = self.checkNumber(totalTurnover)
        if self.TotalTurnover is not None:
            self.TotalTurnover = int(totalTurnover)
        # 開盤價
        self.OpenPrice = self.checkNumber(openPrice)
        if self.OpenPrice is not None:
            self.OpenPrice = fractions.Fraction(openPrice)
        # 最高價
        self.HighestPrice = self.checkNumber(highestPrice)
        if self.HighestPrice is not None:
            self.HighestPrice = fractions.Fraction(highestPrice)
        # 最低價
        self.LowestPrice = self.checkNumber(lowestPrice)
        if self.LowestPrice is not None:
            self.LowestPrice = fractions.Fraction(lowestPrice)
        # 收盤價
        self.ClosePrice = self.checkNumber(closePrice)
        if self.ClosePrice is not None:
            self.ClosePrice = fractions.Fraction(closePrice)
    # 物件表達式
    def __repr__(self):
        totalShare = self.TotalShare
        if totalShare is not None:
            totalShare = f'{totalShare}'
        totalTurnover = self.TotalTurnover
        if totalTurnover is not None:
            totalTurnover = f'{totalTurnover}'
        openPrice = self.OpenPrice
        if openPrice is not None:
            openPrice = f'{float(openPrice):.2f}'
        highestPrice = self.HighestPrice
        if highestPrice is not None:
            highestPrice = f'{float(highestPrice):.2f}'
        lowestPrice = self.LowestPrice
        if lowestPrice is not None:
            lowestPrice = f'{float(lowestPrice):.2f}'
        closePrice = self.ClosePrice
        if closePrice is not None:
            closePrice = f'{float(closePrice):.2f}'
        return (
            f'class AfterHoursInfo {{ '
            f'Code={self.Code}, '
            f'Name={self.Name}, '
            f'TotalShare={totalShare}, '
            f'TotalTurnover={totalTurnover}, '
            f'OpenPrice={openPrice}, '
            f'HighestPrice={highestPrice}, '
            f'LowestPrice={lowestPrice}, '
            f'ClosePrice={closePrice} '
            f'}}'
        )
    # 檢查數值是否有效
    def checkNumber(self, value):
        if value == '--':
            return None
        else:
            return value