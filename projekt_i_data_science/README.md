Detta projekt använder maskininlärning för att förutsäga antalet hörnor för respektive lag i första halvleken av en fotbollsmatch. Modellen är tränad med hjälp av historiska data och använder sju specifika features relaterade till odds och linjer från spelmarknaden.

features = [
    'close_line_total',
    'close_odds_total_over',
    'close_odds_total_under',
    'close_odds_ah_1',
    'close_odds_ah_2',
    'close_line_ah_1',
    'close_line_ah_2'
]
