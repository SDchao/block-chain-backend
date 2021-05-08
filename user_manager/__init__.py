import crypto_operator
import db_operator

from custom_types import *
from logger import logger


def register(id: str, level: int = 0):
    logger.info(f"Registering new user {id}")

    pri_key_sum = crypto_operator.generate_new_key_pair(id)
    db_operator.insert_new_user(id, pri_key_sum, level)


def exist_user(id: str) -> bool:
    logger.info(f"Checking {id} existent")

    db_exist = db_operator.check_user_exist(id)
    crp_exist = crypto_operator.check_id_exist(id)

    if db_exist != crp_exist:
        logger.error(f"User {id} has inconsistent record in db and keypair")
        logger.error(f"DB: {db_exist}")
        logger.error(f"Crypto: {crp_exist}")
        raise ErrorMessage("用户数据错误，请联系管理员")

    logger.info(f"User {id} existent: {db_exist}")

    return db_exist
