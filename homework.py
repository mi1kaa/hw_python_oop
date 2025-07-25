import datetime as dt
from collections import namedtuple

Currency = namedtuple('Currency', 'rate name')


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        if date == '':
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)
    
    def get_today_stats(self):
        sum_today = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                sum_today += record.amount
        return sum_today
    
    def get_week_stats(self):
        sum_week = 0
        date_today = dt.datetime.now().date()
        date_week_ago = today - dt.timedelta(days=7)
        for record in self.records:
            if date_week_ago <= record.date <= date_today:
                sum_week += record.amount
        return sum_week
    
    def get_today_remained(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 79.55
    EURO_RATE = 93.35
    RUB_RATE = 1

    CURRENCIES = {
        'usd': Currency(USD_RATE, 'USD'),
        'eur': Currency(EURO_RATE, 'Euro'),
        'rub': Currency(RUB_RATE, 'руб')
    }
    
    def conversion_rate(self, currency):
        return self.CURRENCIES[currency].rate
    
    def get_today_cash_remained(self, currency):
        today_remained = super().get_today_remained()
        remained = today_remained / self.conversion_rate(currency)
        currency_name = self.CURRENCIES[currency].name

        if remained == 0:
            return ('Денег нет, держись')
        elif remained > 0: 
            remained_rounded = round(remained, 2)
            return (f'На сегодня осталось {remained_rounded} {currency_name}')
        elif remained < 0:
            debt = abs(round(remained, 2))
            return (f'Денег нет, держись: твой долг - {debt} {currency_name}')


class CaloriesCalculator:
    def get_calories_remained():
        remained = super().get_today_remained()
        if remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained} кКал')
        else:
            return ('Хватит есть!')
