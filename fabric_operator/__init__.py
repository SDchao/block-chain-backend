import io
from subprocess import getoutput
import re
import binascii
import json

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
        f = io.StringIO(result)
        err_msg = ""
        for line in f.readlines():
            if line.find("Error") >= 0:
                err_msg += line
        err_msg = err_msg[:-1]
        raise ErrorMessage(err_msg)
    else:
        return result


def get_history(key: str):
    logger.info(f"Getting history: {key}")
    cmd = SHELL_GET_HISTORY_PATH + "'{" + f'"Args":["GetHistory","{key}"]' + "}'"
    result = getoutput(cmd)
    result = result.replace('\\', '')
    result = re.findall(r'{.+?}', result)
    if not result:
        raise ErrorMessage("No history info found!")
    final_res = []
    for element in result:
        element = json.loads(element)
        element["timestamp"] = element['timestamp']['seconds']
        element['value'] = binascii.a2b_base64(element['value']).decode()
        final_res.append(element)
        logger.info(f'history info: {element}')
    return final_res
