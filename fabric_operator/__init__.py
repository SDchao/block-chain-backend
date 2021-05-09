from subprocess import getoutput

from config import *
from custom_types import *
from logger import logger


def put_state(key: str, value: str):
    logger.info(f"Putting state: {key} : {value}")
    cmd = SHELL_MODIFY_PATH + "'{" + f'"Args":["Modify","{key}","{value}"]' + "}'"
    result = getoutput(cmd)
    if result.find('Chaincode invoke successful') < 0:
        raise ErrorMessage(result)


def get_state(key: str) -> str:
    logger.info(f"Getting state: {key}")
    cmd = SHELL_QUERY_PATH + "'{" + f'"Args":["Query","{key}"]' + "}'"
    result = getoutput(cmd)
    if result.find('Error') >= 0:
        raise ErrorMessage(result)
    else:
        return result
