import fractions

class OptionsDailyInfo:
    # 建構子
    def __init__(
        self,
        ContractMonthWeek,
        StrikePrice,
        CallPut,
        Open,
        High,
        Low,
        Close,
        Change,
        Percent,
        VolumeAfterHours,
        VolumeRegular,
        VolumeTotal,
        OpenInterest,
        BestBid,
        BestAsk,
        HistoricalHigh,
        HistoricalLow
        ):

        self.ContractYear = int(ContractMonthWeek[0:4])
        self.ContractMonth = int(ContractMonthWeek[4:6])
        self.ContractWeek = int(3) if len(ContractMonthWeek)==6 else int(ContractMonthWeek[-1])
        self.StrikePrice = int(StrikePrice)
        self.CallPut = CallPut

        self.Open = -1 if Open == '-' else fractions.Fraction(Open)
        self.High =  -1 if High == '-' else fractions.Fraction(High)
        self.Low =  -1 if Low == '-' else fractions.Fraction(Low)
        self.Close =  -1 if Close == '-' else fractions.Fraction(Close)

        # self.Settlement = fractions.Fraction(Settlement)
        self.Change = 0 if Change == '-' or  (Change[0] != '▲' and Change[0] != '▼') else fractions.Fraction(Change[1:])
        self.Percent= 0 if Percent == '-' or (Percent[0] != '▲' and Percent[0] != '▼') else  fractions.Fraction(Percent[1:-1].replace(",", ""))

        self.VolumeAfterHours = int(VolumeAfterHours)
        self.VolumeRegular = int(VolumeRegular)
        self.VolumeTotal = int(VolumeTotal)
        self.OpenInterest = int(OpenInterest)

        self.BestBid = -1 if BestBid == '-' else fractions.Fraction(BestBid)
        self.BestAsk = -1 if BestAsk == '-' else fractions.Fraction(BestAsk)
        self.HistoricalHigh = -1 if HistoricalHigh == '-' else fractions.Fraction(HistoricalHigh)
        self.HistoricalLow = -1 if HistoricalLow == '-' else fractions.Fraction(HistoricalLow)

        # 市值佔比
        # 不建議使用 float 進行浮點數保存，後續可能會造成浮點數計算誤差，
        # 使用 Fraction 保存才能有效降低浮點數計算結果的誤差
    # 物件表達式
    def __repr__(self):
        return (
            f'class OptionsDailyInfo {{ '
            f'ContractYear={self.ContractYear}, '
            f'ContractMonth={self.ContractMonth}, '
            f'ContractWeek={self.ContractWeek}, '
            f'StrikePrice={self.StrikePrice}, '
            f'CallPut={self.CallPut}, '
            f'Open={float(self.Open):.2f}, '
            f'High={float(self.High):.2f}, '
            f'Low={self.Low}, '
            f'Close={float(self.Close):.2f}, '
            f'Change={float(self.Change):.2f}, '
            f'Percent={float(self.Percent):.2f}, '
            f'VolumeAfterHours={self.VolumeAfterHours}, '
            f'VolumeRegular={self.VolumeRegular}, '
            f'VolumeTotal={self.VolumeTotal}, '
            f'OpenInterest={self.OpenInterest}, '
            f'BestBid={float(self.BestBid):.2f}, '
            f'BestAsk={float(self.BestAsk):.2f}, '
            f'HistoricalHigh={float(self.HistoricalHigh):.2f}, '
            f'HistoricalLow={float(self.HistoricalLow):.2f}'
            f'}}'
        )