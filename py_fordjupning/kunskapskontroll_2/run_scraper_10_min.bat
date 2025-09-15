@echo off
title log_full_time_odds
cd /d C:\Users\Isaac\Documents\GitHub\ec-data-science-24\py_fordjupning\kunskapskontroll_2
:start
echo --------------------Starting scraper scripts--------------------
python main.py
echo --------------------Restarting scraper scripts--------------------
timeout 600
goto start