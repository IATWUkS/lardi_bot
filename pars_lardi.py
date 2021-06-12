import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import db_bot
import data

LOGIN = data.LOGIN
PASSWORD = data.PASSWORD


def get_html(URL):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    browser.get('https://lardi-trans.com/ru/accounts/login/')
    browser.find_element_by_css_selector('#loginData').send_keys(LOGIN)
    browser.find_element_by_css_selector('#password').send_keys(
        PASSWORD)
    browser.find_element_by_css_selector('#loginButton').click()
    time.sleep(10)
    cockie = browser.get_cookies()
    cockies = cockie[0]['value'] + ';' + cockie[1]['name'] + '=' + cockie[1]['value'] + ';' + cockie[2]['name'] + '=' + cockie[2]['value'] + ';' + cockie[3]['name'] + '=' + cockie[3]['value'] + ';' + cockie[4]['name'] + '=' + cockie[4]['value'] + ';' + cockie[5]['name'] + '=' + cockie[5]['value'] + ';' + cockie[6]['name'] + '=' + cockie[6]['value'] + ';' + cockie[7]['name'] + '=' + cockie[7]['value'] + ';' + cockie[8]['name'] + '=' + cockie[8]['value'] + ';' + cockie[9]['name'] + '=' + cockie[9]['value'] + ';' + cockie[10]['name'] + '=' + cockie[10]['value'] + ';' + cockie[11]['name'] + '=' + cockie[11]['value'] + ';' + cockie[12]['name'] + '=' + cockie[12]['value'] + ';' + cockie[13]['name'] + '=' + cockie[13]['value'] + ';' + cockie[14]['name'] + '=' + cockie[14]['value'] + ';' + cockie[15]['name'] + '=' + cockie[15]['value'] + ';' + cockie[16]['name'] + '=' + cockie[16]['value'] + ';'
    HEADERS = {
        'cookie': cockies,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    answer = requests.get(URL, headers=HEADERS)
    return answer.text


def get_cargo(URL_list, tg_id):
    list_write = []
    all_list_write = []
    for URL in URL_list:
        try:
            page = get_html(URL)
            soup = BeautifulSoup(page, "html.parser")
            name = soup.find('h1').text
            cargo = soup.find('table', class_='t mygtTable ui_table_lardi predlTable')
            all_cargo_info = cargo.findAll('tr')
            for inf in all_cargo_info:
                full_info_span = inf.findAll('td')
                for inf in full_info_span:
                    try:
                        list_write.append(inf.find('span').text)
                    except:
                        pass
                if str(list_write) != '[]':
                    check = db_bot.get_cargo(list_write[5])
                    if check is None or check['cargo'] != list_write[5]:
                        db_bot.insert_carge_info(list_write[0], list_write[1], list_write[2], list_write[3],
                                                 list_write[4],
                                                 list_write[5], list_write[6], list_write[7], name, URL, tg_id)
                        all_list_write.append(URL)
                list_write.clear()
        except:
            pass
    return all_list_write


def get_cargo_search(URL_list, tg_id):
    all_list_write = []
    for URL in URL_list:
            page = get_html(URL)
            soup = BeautifulSoup(page, "html.parser")
            cargo = soup.find('div', class_='ps_search-result_data')
            all_cargo_info = cargo.findAll('div', class_='ps_search-result_data-item')
            for inf in all_cargo_info:
                url = 'https://lardi-trans.com/gruz/view/' + str(inf).split('data-ps-id="')[1].split('"')[0]
                country = inf.find('span', class_='ps_data_direction').text.replace('\n', '')
                date = inf.find('span', class_='ps_data_load-date').text.replace('\n', '')
                transport = inf.find('span', class_='ps_data_transport').text.replace('\n', '')
                from_is = inf.find('span', class_='ps_data_town').text.replace('\n', '')
                to_is = inf.find('span', class_='ps_data_town').text.replace('\n', '')
                cargo = inf.find('div', class_='ps_data ps_search-result_data-cargo ps_data-cargo').text.replace('\n',
                                                                                                                 '')
                pay = inf.find('span', class_='ps_data_payment_info').text.replace('\n', '')
                contacts = inf.find('div', class_='ps_proposal_user_name-container').text.replace('\n', '')
                check = db_bot.get_cargo_search(url)
                if check is None or check['url'] != url:
                    try:
                        db_bot.insert_carge_info_search(country, date, transport, from_is, to_is, cargo, pay, contacts,
                                                        url, tg_id)
                        all_list_write.append(url)
                    except:
                        pass
    return all_list_write