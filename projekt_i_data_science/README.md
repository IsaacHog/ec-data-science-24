# Modell för att prediktera hörnor för respektive lag i första halvleken

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

Datan som modellen är tränad på är taget från corner-stats.com 2023. Datan hämtade jag genom att scrapea hemsidans historik på de 5 stora fotbolls-ligorna. Notera att jag skapade samt hämtade datan med denna scraper 2023, därav behöver kanske dependencies uppdateras för att köra scraper scriptet igen.

I mappen "old" är filer för mitt skrotade projekt. Jag valde att gå vidare med detta projektet istället då jag ansåg att outputen från den modellen inte var intressant.