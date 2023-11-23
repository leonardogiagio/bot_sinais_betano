import telegram as t
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import re
import subprocess
import os

token = '6711575896:AAEO1bNBZ6boE6zKrJcGP7wNhnlPvODagZM'
# chat_id = t.last_chat_id(token)
chat_id = -1002011158039

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://br.betano.com/live/')


def main():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'LiveEventListContainer')))

    closePopup()

    main_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.vue-recycle-scroller__item-wrapper')))
    children_main_element = main_element.find_elements(By.CSS_SELECTOR, 'div.tw-truncate.tw-flex > span.tw-truncate')[0]
    children_main_element.click()
    time.sleep(2)

    processed_elements = set()

    count_five_in_five = 1
    count_pass_down = 0
    
    while True:
        if(count_pass_down > 0):
            qtdPassDown = 120 * count_pass_down
            passDown(qtdPassDown)

        count_pass_down = count_pass_down + 1
        
        new_items = driver.find_elements(By.CLASS_NAME, "vue-recycle-scroller__item-view")

        for item in new_items:
            if(count_five_in_five > 5):
                count_five_in_five = 1
                pageRefresh()
                closePopup()
                limparConsole()
                break

            
            print(item.text)
     
            count_five_in_five = count_five_in_five + 1
            try:
                if "(Esports)" not in item.text:                    
                    try:
                        teams = item.find_element(By.CSS_SELECTOR, '[data-qa="participants"]').text.split('\n')
                        
                        if len(teams) < 2:
                            continue
                    except Exception as e:
                        continue

                    confrontation = f'{teams[0]} x {teams[1]}'
                    if confrontation in processed_elements:
                        continue
                    competition = item.find_elements(By.CLASS_NAME, 'tw-cursor-pointer')[0].text
                    match_time_match = re.search(r'(\d+:\d+)', item.text)
                    match_time = match_time_match.group(1) if match_time_match else None
                    block_result_game = item.find_element(By.CSS_SELECTOR, 'div[data-qa="score"]')
                    
                    result_game = block_result_game.text.replace('\n', ' x ')

                    minutes_match_time = match_time.split(":")

                    if(int(minutes_match_time[0]) < 40):
                        continue

                    try:
                        item.click()
                        time.sleep(2)
                        url_link = driver.execute_script('return arguments[0].querySelector(\'a\');', item).get_attribute("href")

                    except StaleElementReferenceException:
                        continue
                    except ElementClickInterceptedException:
                        continue

                    tabs = driver.find_elements(By.CLASS_NAME, 'GTM-tab-name')
                    cards = [element for element in tabs if element.text == "Cartões"]

                    if not cards:
                        continue

                    cards[0].click()
                    time.sleep(1)

                    try:
                        block_odd_red_card = driver.find_element(By.XPATH, '//div[contains(text(), "Total de Cartões Vermelhos")]')
                        block_odd_red_card.click()

                        try:
                            odd_red_card05 = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Bet on Menos de 0.5 with odds")]')
                            odd_red_card_split = odd_red_card05.text.splitlines()
                            odd = odd_red_card_split[2]
                            if(float(odd) < 1.50):
                                continue

                        except NoSuchElementException:
                            try:
                                odd_red_card15 = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Bet on Menos de 1.5 with odds")]')
                                odd_red_card_split = odd_red_card15.text.splitlines()
                                odd = odd_red_card_split[2]
                                if(float(odd) < 1.50):
                                    continue
                            except NoSuchElementException:
                                continue

                    except NoSuchElementException:
                        continue
                

                    message = f'🚨 Alerta de Oportunidade!!! 🚨 \n\n⚽ Jogo: {confrontation} \n🏆 Competição: {competition} \n📈 Odd: {odd} \n🕐 Tempo: {match_time} \n👉 Resultado: {result_game} \n\n📲 Link: {url_link}'

                    print(message)
                    processed_elements.add(confrontation)

                    # t.send_message(token, chat_id, message)
                else:
                    pageRefresh()
                    closePopup()
                    limparConsole()
                    count_pass_down = 0
                    break
            except StaleElementReferenceException:
                continue
            

def passDown(qtdPassDown):
    # driver.execute_script("document.querySelector('.vue-recycle-scroller.direction-vertical:not(.page-mode)').scrollBy(0, 120);")
    script = f"document.querySelector('.vue-recycle-scroller.direction-vertical:not(.page-mode)').scrollBy(0, {qtdPassDown});"
    driver.execute_script(script)
    time.sleep(1)

def closePopup():
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="landing-page-modal"]/div/div[1]/button'))).click()
    except:
        print('Sem poppup')

def pageRefresh():
    driver.refresh()
    time.sleep(3)
    driver.execute_script("document.querySelector('.vue-recycle-scroller.direction-vertical:not(.page-mode)').scrollTo(0, 0);")

def limparConsole():
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

main()