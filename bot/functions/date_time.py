from datetime import date, datetime


BOOSTED_DAYS = [
    date(year=2000, month=1, day=1),  # Confraternização Universal
    date(year=2000, month=3, day=6),  # Data Magna
    date(year=2000, month=4, day=21),  # Tiradentes
    date(year=2000, month=5, day=1),  # Dia do Trabalho
    date(year=2000, month=9, day=7),  # Independência do Brasil
    date(year=2000, month=10, day=12),  # Nossa Senhora Aparecida (Crianças)
    date(year=2000, month=11, day=2),  # Finados
    date(year=2000, month=11, day=15),  # Proclamação da República
    date(year=2000, month=12, day=8),  # Nossa Senhora da Imaculada Conceição
    date(year=2000, month=12, day=24),  # Véspera de Natal
    date(year=2000, month=12, day=25),  # Natal
    date(year=2000, month=12, day=26),  # Recesso
    date(year=2000, month=12, day=27),  # Recesso
    date(year=2000, month=12, day=28),  # Recesso
    date(year=2000, month=12, day=29),  # Recesso
    date(year=2000, month=12, day=30),  # Recesso
    date(year=2000, month=12, day=31),  # Véspera de Ano Novo
]


def is_boosted_day(now: datetime) -> bool:
    weekend = [5, 6]
    return any((
        now.weekday() in weekend,
        now.date().replace(year=2000) in BOOSTED_DAYS
    ))
