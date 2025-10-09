@echo off
title log_pre_ko_odds
cd /d C:\Users\Isaac\Documents\GitHub\ec-data-science-24\projekt_i_data_science
:start
echo --------------------Starting scraper scripts--------------------
python main.py
echo --------------------Restarting scraper scripts--------------------
timeout 1800
goto start