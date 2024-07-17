from datetime import date, datetime, timedelta
from typing import List


def is_boosted_day(now: datetime) -> bool:
    weekend = [5, 6]
    return any((
        now.weekday() in weekend,
        compare_month_day_with_list(now, BOOSTED_DAYS)
    ))


def compare_month_day_with_list(target_date: date, date_list: List[date]):
    for d in date_list:
        if target_date.month == d.month and target_date.day == d.day:
            return True
    return False


def get_programmer_day() -> date:
    current_year = date.today().year
    programmer_date = date(current_year, 1, 1) + timedelta(days=255)

    return programmer_date


BOOSTED_DAYS = [
    date(year=2000, month=1, day=1),    # Confraternização Universal
    date(year=2000, month=3, day=6),    # Data Magna
    date(year=2000, month=3, day=8),    # Dia da Mulher
    date(year=2000, month=3, day=10),   # Dia do Mario
    date(year=2000, month=4, day=21),   # Tiradentes
    date(year=2000, month=4, day=25),   # Dia do Corno
    date(year=2000, month=5, day=1),    # Dia do Trabalho
    date(year=2000, month=5, day=4),    # Dia da Força (SW)
    date(year=2000, month=5, day=9),    # Dia do Goku
    date(year=2000, month=6, day=15),   # Dia do Homem
    date(year=2000, month=6, day=24),   # São João
    date(year=2000, month=7, day=16),   # Nossa Senhora do Carmo
    date(year=2000, month=9, day=7),    # Independência do Brasil
    get_programmer_day(),               # Dia do Programador
    date(year=2000, month=10, day=12),  # Nossa Senhora Aparecida (Crianças)
    date(year=2000, month=11, day=2),   # Finados
    date(year=2000, month=11, day=15),  # Proclamação da República
    date(year=2000, month=12, day=8),   # Nossa Senhora da Imaculada Conceição
    date(year=2000, month=12, day=24),  # Véspera de Natal
    date(year=2000, month=12, day=25),  # Natal
    date(year=2000, month=12, day=26),  # Recesso
    date(year=2000, month=12, day=27),  # Recesso
    date(year=2000, month=12, day=28),  # Recesso
    date(year=2000, month=12, day=29),  # Recesso
    date(year=2000, month=12, day=30),  # Recesso
    date(year=2000, month=12, day=31),  # Véspera de Ano Novo
]


if __name__ == '__main__':
    now = datetime.now()
    print(f'{now} is Boosted Day?', is_boosted_day(now))