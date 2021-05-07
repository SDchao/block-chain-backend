import sqlite3

from logger import logger

conn = sqlite3.connect("main.db", check_same_thread=False)
cursor = conn.cursor()

# CREATE USER INFO TABLE
cursor.execute("create table if not exists user("
               "id varchar(18) primary key, "
               "pri_key_sum varchar(32) not null,"
               "level integer default 0)")
try:
    cursor.execute("insert into user (id, pri_key_sum, level) "
                   "values ('admin', 'e10adc3949ba59abbe56e057f20f883e', '2')")
except sqlite3.IntegrityError:
    pass
conn.commit()


def insert_new_user(id, pri_key_sum):
    logger.info(f"Submitting new user to database ({id})")
    cursor.execute("insert into user (id, pri_key_sum) "
                   "values (?,?)",
                   (id, pri_key_sum))
    conn.commit()


def verify_id_key(id, pri_key_sum):
    logger.info(f"Checking user {id} with password")
    cursor.execute("select level from user where id = ? and pri_key_sum = ?", (id, pri_key_sum))
    result_tuple = cursor.fetchone()
    logger.info(f"Result: {result_tuple}")
    if result_tuple:
        return result_tuple[0]
    else:
        return -1
