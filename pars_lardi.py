import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import db_bot
import data

LOGIN = data.LOGIN
PASSWORD = data.PASSWORD


def get_html(URL):
    cockies = ''
    with open('cock.txt', 'r') as f:
        cockies = f.readline()
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
            num = 1
            page = get_html(URL)
            soup = BeautifulSoup(page, "html.parser")
            name = soup.find('h1').text
            cargo = soup.find('table', class_='t mygtTable ui_table_lardi predlTable')
            st = str(cargo)
            all_cargo_info = cargo.findAll('tr')
            number = ''
            for inf_tr in all_cargo_info:
                full_info_span = inf_tr.findAll('td')
                try:
                    number = inf_tr.find('div', class_='uiFirmContScroolBlock').find('span').text
                except:
                    pass
                for inf in full_info_span:
                    try:
                        list_write.append(inf.find('span').text)
                    except:
                        pass
                if str(list_write) != '[]':
                    id_gruz = st.split('predlRowGruz')[num].split('"')[0]
                    num += 1
                    check = db_bot.get_cargo(id_gruz)
                    if check is None or check['id_gruz'] != id_gruz:
                        db_bot.insert_carge_info(list_write[0], list_write[1], list_write[2], list_write[3],
                                                 list_write[4],
                                                 list_write[5], list_write[6], list_write[7] + '\n' + str(number), name, URL, tg_id, URL, id_gruz)
                        all_list_write.append(URL)
                list_write.clear()
        except:
            pass
    return all_list_write


def get_cargo_search(URL_list, tg_id):
    all_list_write = []
    for URL in URL_list:
        try:
            page = get_html(URL)
            soup = BeautifulSoup(page, "html.parser")
            cargo = soup.find('div', class_='ps_search-result_data')
            all_cargo_info = cargo.findAll('div', class_='ps_search-result_data-item')
            for inf in all_cargo_info:
                url = 'https://lardi-trans.com/' + URL.split('/')[3] + '/view/' + str(inf).split('data-ps-id="')[1].split('"')[0]
                country = inf.find('span', class_='ps_data_direction').text.replace('\n', '')
                date = inf.find('span', class_='ps_data_load-date').text.replace('\n', '')
                transport = inf.find('span', class_='ps_data_transport').text.replace('\n', '')
                from_is = inf.find('span', class_='ps_data_town').text.replace('\n', '')
                to_is = inf.find('div', class_='ps_data ps_search-result_data-where ps_data-where').text.replace('\n', '')
                cargo = inf.find('div', class_='ps_data ps_search-result_data-cargo ps_data-cargo').text.replace('\n',
                                                                                                                 '')
                pay = inf.find('span', class_='ps_data_payment_info').text.replace('\n', '')
                contacts_1 = inf.find('div', class_='ps_proposal_user_name-container').text.replace('\n', '')
                contacts_2 = inf.find('ul', class_='ps_proposal_user_contacts_list').text.replace('\n', '')
                contacts_ed = contacts_2.split('+')
                contacts_full = ''
                for end in contacts_ed:
                    contacts_full = contacts_full + end + '\n'
                contacts = contacts_1 + contacts_full
                check = db_bot.get_cargo_search(url)
                if check is None or check['url'] != url:
                    try:
                        db_bot.insert_carge_info_search(country, date, transport, from_is, to_is, cargo, pay, contacts,
                                                        url, tg_id, URL)
                        all_list_write.append(url)
                    except:
                        pass
        except:
            print('Ошибка ссылки.')
    return all_list_write


get_cargo(['https://lardi-trans.ru/user/10768525929/gruztrans/'], '4214213')