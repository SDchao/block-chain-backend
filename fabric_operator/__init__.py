from custom_types import *
from subprocess import getoutput
from config import *
from logger import logger


def put_state(key: str, value: str):
    logger.info(f"Putting state: {key} : {value}")
    cmd = MODIFY + f'\'{"function":"changeStuInfo","Args":["{key}","{value}"]}\''
    result = getoutput(cmd)
    if result.index('Chaincode invoke successful') < 0:
        raise ErrorMessage(result)


def get_state(key: str) -> str:
    logger.info(f"Getting state: {key}")
    cmd = QUERY + f'\'{"Args":["queryStuInfo","{key}"]}\''
    result = getoutput(cmd)
    if result.index('Error') > 0:
        raise ErrorMessage(result)
    else:
        return result


if __name__ == '__main__':
    put_state("test", "123test123")
    assert get_state("test") == "123test123"
