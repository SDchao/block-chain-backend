from custom_types import *
from subprocess import getoutput
from config import *


def put_state(key: str, value: str):
    cmd = MODIFY + f'\'{"function":"changeStuInfo","Args":["{key}","{value}"]}\''
    result = getoutput(cmd)
    if result.index('Chaincode invoke successful') < 0:
        raise ErrorMessage(result)


def get_state(key: str) -> str:
    cmd = QUERY + f'\'{"Args":["queryStuInfo","{key}"]}\''
    result = getoutput(cmd)
    if result.index('Error') > 0:
        raise ErrorMessage(result)
    else:
        return result
