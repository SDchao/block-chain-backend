import sqlite3

from custom_types import ErrorMessage
from logger import logger

conn = sqlite3.connect("main.db", check_same_thread=False)
cursor = conn.cursor()

# CREATE USER INFO TABLE
cursor.execute("create table if not exists user("
               "id varchar(18) primary key, "
               "pri_key_sum varchar(32) not null,"
               "level integer default 0)")

# CREATE USER_CERT TABLE
cursor.execute("create table if not exists user_cert("
               "id varchar(18), "
               "cert_id varchar(32) unique)")

try:
    # ADD ADMIN ACCOUNT
    cursor.execute("insert into user (id, pri_key_sum, level) "
                   "values ('admin', 'e10adc3949ba59abbe56e057f20f883e', '2')")
except sqlite3.IntegrityError:
    pass
conn.commit()


def check_user_exist(id: str) -> bool:
    logger.info(f"checking if user {id} exist")
    cursor.execute("select id from user where id = ?", (id,))
    r = cursor.fetchone()
    if r:
        return True
    return False


def insert_user(id: str, pri_key_sum: str, level: int = 0):
    logger.info(f"Submitting new user to database ({id})")
    try:
        cursor.execute("insert into user (id, pri_key_sum, level) "
                       "values (?,?,?)",
                       (id, pri_key_sum, level))
        conn.commit()
    except sqlite3.IntegrityError:
        logger.warning(f"{id} has existed.")
        raise ErrorMessage("用户已存在")


def verify_id_key(id: str, pri_key_sum: str) -> int:
    logger.info(f"Verifying user {id} with pri_key_sum")
    cursor.execute("select level from user where id = ? and pri_key_sum = ?", (id, pri_key_sum))
    result_tuple = cursor.fetchone()
    if result_tuple:
        logger.info(f"User {id} verified")
        return int(result_tuple[0])
    else:
        logger.info(f"Failed to verify user {id}")
        return -1


def insert_cert(id, cert_id):
    logger.info(f"Inserting new cert {cert_id}, belongs to {id}")
    if not check_user_exist(id):
        logger.warning(f"User {id} do not exists")
        raise ErrorMessage("用户不存在")

    try:
        cursor.execute("insert into user_cert (id, cert_id) "
                       "VALUES (?,?)", (id, cert_id))
        conn.commit()
    except sqlite3.IntegrityError:
        logger.warning(f"User {id} already have cert {cert_id}")
        raise ErrorMessage("已存在该证书")
