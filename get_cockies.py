import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import data

LOGIN = data.LOGIN
PASSWORD = data.PASSWORD


def get_cockies():
    options = Options()
    # options.add_argument('headless')
    options.add_argument('user-data-dir=C:\\Users\\IATWUkS\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://lardi-trans.com/ru/accounts/login/')
    try:
        browser.find_element_by_css_selector('#loginData').send_keys(LOGIN)
    except:
        pass
    try:
        browser.find_element_by_css_selector('#password').send_keys(
            PASSWORD)
        time.sleep(5)
        browser.find_element_by_css_selector('#loginButton').click()
    except:
        pass
    time.sleep(5)
    cockie = browser.get_cookies()
    cockies = cockie[0]['value'] + ';' + cockie[1]['name'] + '=' + cockie[1]['value'] + ';' + cockie[2][
        'name'] + '=' + \
              cockie[2]['value'] + ';' + cockie[3]['name'] + '=' + cockie[3]['value'] + ';' + cockie[4][
                  'name'] + '=' + \
              cockie[4]['value'] + ';' + cockie[5]['name'] + '=' + cockie[5]['value'] + ';' + cockie[6][
                  'name'] + '=' + \
              cockie[6]['value'] + ';' + cockie[7]['name'] + '=' + cockie[7]['value'] + ';' + cockie[8][
                  'name'] + '=' + \
              cockie[8]['value'] + ';' + cockie[9]['name'] + '=' + cockie[9]['value'] + ';' + cockie[10][
                  'name'] + '=' + \
              cockie[10]['value'] + ';' + cockie[11]['name'] + '=' + cockie[11]['value'] + ';' + cockie[12][
                  'name'] + '=' + cockie[12]['value'] + ';' + cockie[13]['name'] + '=' + cockie[13]['value'] + ';' + \
              cockie[14]['name'] + '=' + cockie[14]['value'] + ';' + cockie[15]['name'] + '=' + cockie[15][
                  'value'] + ';' + cockie[16]['name'] + '=' + cockie[16]['value'] + ';'
    with open('cock.txt', 'w') as f:
        f.write(cockies)
    browser.close()


while True:
    get_cockies()
    time.sleep(1800)
