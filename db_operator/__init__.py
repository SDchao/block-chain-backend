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
                   "values ('admin', "
                   "'8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', '2')")
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


def insert_cert(id, cert_id) -> sqlite3.Connection:
    logger.info(f"Inserting new cert {cert_id}, belongs to {id}")
    if not check_user_exist(id):
        logger.warning(f"User {id} do not exists")
        raise ErrorMessage("用户不存在")

    try:
        cursor.execute("insert into user_cert (id, cert_id) "
                       "VALUES (?,?)", (id, cert_id))
        return conn
    except sqlite3.IntegrityError:
        logger.warning(f"Already have cert {cert_id}")
        raise ErrorMessage("已存在该证书")


def find_certs(id) -> list:
    logger.info(f"Finding certs belong to {id}")

    cursor.execute("select cert_id from user_cert where id=?", (id,))
    results = cursor.fetchall()

    return_val = []
    for r in results:
        return_val.append(r[0])

    return return_val


def check_cert_exist(id, cert_id) -> bool:
    logger.info(f"Checking cert {cert_id} of user {id}")

    cursor.execute("select cert_id from user_cert where id = ? and cert_id = ?", (id, cert_id))
    result = cursor.fetchone()

    return bool(result)


def remove_cert(id, cert_id):
    logger.info(f"Removing cert {cert_id} of user {id}")

    cursor.execute("delete from user_cert where id = ? and cert_id = ?", (id, cert_id))
