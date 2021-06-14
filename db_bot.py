import pymysql
from pymysql.cursors import DictCursor


def get_conn():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='lardi',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    return connection


def insert_carge_info(country, date, transport, from_tr, to, cargo, pay, contacts, name, url, tg_id, global_url):
    connection = get_conn()
    sql = 'INSERT INTO cargo_info(country, date, transport, from_is, to_is, cargo, pay, contacts, name, url, tg_id, global_url) VALUES ("%s", "%s", "%s", ' \
          '"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
              country, date, transport, from_tr, to, cargo, pay, contacts, name, url, tg_id, global_url)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()


def insert_carge_info_search(country, date, transport, from_tr, to, cargo, pay, contacts, url, tg_id, global_url):
    connection = get_conn()
    sql = 'INSERT INTO cargo_search_info(country, date, transport, from_is, to_is, cargo, pay, contacts, url, tg_id, global_url) VALUES ("%s", "%s", "%s", ' \
          '"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
              country, date, transport, from_tr, to, cargo, pay, contacts, url, tg_id, global_url)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()


def get_cargo_info_search(cargo):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM cargo_search_info WHERE url = "%s"' % cargo
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        return None


def get_cargo_info_by_id(id):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM cargo_info WHERE id = %s' % id
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        return None


def get_cargo_info_by_id_search(id):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM cargo_search_info WHERE id = %s' % id
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        return None


def get_cargo_info(URL):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM cargo_info WHERE URL = "%s"' % URL
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        return None


def get_cargo_search(URL):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT url FROM cargo_search_info WHERE url = "%s"' % URL
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        return None


def get_cargo(cargo):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT cargo FROM cargo_info WHERE cargo = "%s"' % cargo
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        return None


def insert_cargo_url(URL, tg_id, name):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'INSERT INTO url_pars_cargo(url, tg_id, name) VALUES ("%s", "%s", "%s")' % (URL, tg_id, name)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def insert_cargo_url_search(URL, tg_id, name):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'INSERT INTO ulr_pars_cargo_search(url, tg_id, name) VALUES ("%s", "%s", "%s")' % (URL, tg_id, name)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def get_cargo_url(tg_id):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM url_pars_cargo WHERE tg_id = "%s"' % tg_id
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        print(data)
        return data
    except:
        return None


def get_cargo_url_search(tg_id):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM ulr_pars_cargo_search WHERE tg_id = "%s"' % tg_id
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data
    except:
        return None


def get_cargo_url_search_url(url):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM ulr_pars_cargo_search WHERE url = "%s"' % url
        cursor.execute(sql)
        data = cursor.fetchone()
        connection.close()
        return data
    except:
        return None


def get_cargo_url_data(url):
    connection = get_conn()
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM url_pars_cargo WHERE url = "%s"' % url
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data
    except:
        return None


def delete_cargo_url(id_url):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'DELETE FROM url_pars_cargo WHERE id = %s' % id_url
    cursor.execute(sql)
    connection.commit()
    connection.close()


def delete_cargo_url_search(id_url):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'DELETE FROM ulr_pars_cargo_search WHERE id = %s' % id_url
    cursor.execute(sql)
    connection.commit()
    connection.close()


def get_id_tg_check(ids_tg):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'SELECT ids_tg FROM ids_tg WHERE ids_tg = "%s"' % ids_tg
    cursor.execute(sql)
    data = cursor.fetchone()
    connection.close()
    return data


def get_id_tg_info(ids_tg):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'SELECT * FROM ids_tg WHERE ids_tg = "%s"' % ids_tg
    cursor.execute(sql)
    data = cursor.fetchone()
    connection.close()
    return data


def update_status(status, tg_id):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'UPDATE ids_tg SET status_monit = "%s" WHERE ids_tg = "%s"' % (status, tg_id)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def update_status_two(status, tg_id):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'UPDATE ids_tg SET status_monit_two = "%s" WHERE ids_tg = "%s"' % (status, tg_id)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def get_id_tg():
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'SELECT ids_tg FROM ids_tg'
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()
    return data


def insert_id_tg(ids_tg):
    connection = get_conn()
    cursor = connection.cursor()
    sql = 'INSERT INTO ids_tg(ids_tg) VALUES ("%s")' % ids_tg
    cursor.execute(sql)
    connection.commit()
    connection.close()
