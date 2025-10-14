from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import traceback
import gspread
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc
import json

if __name__ == "__main__":
    sa = gspread.service_account(filename='service_account.json')
    sh = sa.open("corner_derivatives")
    wks = sh.worksheet("eng1_set")
    
    '''
    sh_error = sa.open("ErrorLog")
    wks_error = sh_error.worksheet("Error")
    wks_error_log = sh_error.worksheet("ErrorLog")
    '''
    
    driver = uc.Chrome(headless=True, driver_executable_path="C:/Users/Isaac/Desktop/chromedriver-win64/chromedriver.exe")
    wait_0_2 = WebDriverWait(driver, 0.2)
    wait_1 = WebDriverWait(driver, 1)
    wait_3 = WebDriverWait(driver, 3)



    def ScrapeLoop():
        x = 2 # start 2 to avoid unfinished games
        while True:
            if x == 10:
                break
            print(f"----------------- Starting main loop, x = {x} eng1")
            driver.get(f"https://corner-stats.com/premier-league/england/tournament/1-{x}")
            
            # get match_objects
            match_elements = wait_3.until(EC.presence_of_all_elements_located((By.XPATH, ".//td[@class='old-matches-td2']/a")))
            match_objects = []
            for element in match_elements:
                if "/" not in element.text: # scores have a attribute aswell
                    continue
                text = element.text.split(" ")
                date = text[0]
                match_name = " ".join(text[1:])
                match_objects.append({'match_name': match_name, 'date': date, 'url': element.get_attribute("href")})
            
            data_to_append = []
            for i, match_object in enumerate(match_objects):
                print(f"Getting stats for {match_object['match_name']}...")
                driver.get(match_object['url'])
                time.sleep(0.3)
                wait_1.until(EC.element_to_be_clickable((By.XPATH, ".//a[@href='#corners']"))).click()
                wait_1.until(EC.element_to_be_clickable((By.XPATH, ".//li[@class='match-info__other nav_other']"))).click()
                time.sleep(0.3)

                corners_result_home = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='match-info__stats-field field_other']/div/span[1]"))).text
                corners_result_home = corners_result_home.split("(")
                try:
                    corners_result_home_1st_ht = int(corners_result_home[1].replace(")", ""))
                except:
                    continue
                corners_result_home = int(corners_result_home[0])

                corners_result_away = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='match-info__stats-field field_other']/div/span[3]"))).text
                corners_result_away = corners_result_away.split("(")
                corners_result_away_1st_ht = int(corners_result_away[1].replace(")", ""))
                corners_result_away = int(corners_result_away[0])
                
                corners_result_total = corners_result_home + corners_result_away
                corners_result_total_1st_ht = corners_result_home_1st_ht + corners_result_away_1st_ht
                result = [corners_result_total, corners_result_home, corners_result_away, corners_result_total_1st_ht, corners_result_home_1st_ht, corners_result_away_1st_ht]


                close_line_ah_1 = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='tbody1']/tr/td[7]"))).text
                close_odds_ah_1 = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='tbody1']/tr/td[8]"))).text
                close_line_ah_2 = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='tbody1']/tr/td[9]"))).text
                close_odds_ah_2 = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='tbody1']/tr/td[10]"))).text
                close_odds_ah = [close_line_ah_1, close_line_ah_2, close_odds_ah_1, close_odds_ah_2]

                close_line_total = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='tbody1']/tr/td[11]"))).text
                close_odds_total_over = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='tbody1']/tr/td[12]"))).text
                close_odds_total_under = wait_1.until(EC.presence_of_element_located((By.XPATH, ".//tbody[@class='tbody1']/tr/td[13]"))).text
                close_odds_total = [close_line_total, close_odds_total_over, close_odds_total_under]

                flattened_data = [match_objects[i]['date'], match_objects[i]['match_name']] + result + close_odds_ah + close_odds_total
                data_to_append.append(flattened_data)

                print(f"Finished {match_object['match_name']} {x}")
            
            print("Finished one batch of match_objects")
            wks.append_rows(data_to_append)
            x += 1
    
    
# Instance to run
    print("---------------corner_stats Script initiated--------------------")
    ScrapeLoop()

    print("Quitting driver")
    driver.quit()