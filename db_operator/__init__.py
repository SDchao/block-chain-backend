import sqlite3

from logger import logger

conn = sqlite3.connect("main.db", check_same_thread=False)
cursor = conn.cursor()

# CREATE USER INFO TABLE
cursor.execute("create table if not exists user("
               "id varchar(18) primary key, "
               "pri_key_sum varchar(32) not null,"
               "level integer default 0)")

cursor.execute("create table if not exists user_hash("
               "id varchar(18), "
               "cert_hash varchar(32) not null, "
               "unique (id, cert_hash))")

try:
    cursor.execute("insert into user (id, pri_key_sum, level) "
                   "values ('admin', 'e10adc3949ba59abbe56e057f20f883e', '2')")
except sqlite3.IntegrityError:
    pass
conn.commit()


def insert_new_user(id, pri_key_sum):
    logger.info(f"Submitting new user to database ({id})")
    try:
        cursor.execute("insert into user (id, pri_key_sum) "
                       "values (?,?)",
                       (id, pri_key_sum))
        conn.commit()
    except sqlite3.IntegrityError:
        logger.info(f"{id} has existed.")
        raise UserWarning("用户已存在")


def verify_id_key(id, pri_key_sum):
    logger.info(f"Verifying user {id} with pri_key_sum")
    cursor.execute("select level from user where id = ? and pri_key_sum = ?", (id, pri_key_sum))
    result_tuple = cursor.fetchone()
    if result_tuple:
        logger.info(f"User {id} verified")
        return result_tuple[0]
    else:
        logger.info(f"Failed to verify user {id}")
        return -1


def insert_new_cert_hash(id, cert_hash):
    logger.info(f"Inserting new cert_hash record {cert_hash}, belongs to {id}")
    cursor.execute("select id from user where id = ?", (id))
    result = cursor.fetchone()
    if not result:
        logger.warning(f"User {id} do not exists")
        raise UserWarning("用户不存在")

    try:
        cursor.execute("insert into user_hash (id, cert_hash) "
                       "VALUES (?,?)", (id, cert_hash))
    except sqlite3.IntegrityError:
        logger.warning(f"User {id} already have cert {cert_hash}")
        raise UserWarning("已存在该证书")
