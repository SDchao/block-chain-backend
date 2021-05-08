import os

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA

from custom_types import ErrorMessage
from logger import logger

if not os.path.exists("user_keys"):
    os.mkdir("user_keys")


def check_id_exist(id: str):
    logger.info(f"Checking if {id} has existed")
    if os.path.exists(f"user_keys/{id}.pem"):
        return True
    return False


def generate_new_key_pair(id: str) -> str:
    """
    生产新密钥对，返回私钥的hex_md5摘要
    :param id:
    """
    if check_id_exist(id):
        logger.warning(f"{id} keypair has already generated")
        raise ErrorMessage("用户已存在")

    key = RSA.generate(1024)

    if not os.path.exists("user_keys"):
        os.mkdir("user_keys")

    with open(f"user_keys/{id}.pem", "wb") as f:
        f.write(key.export_key())

    with open(f"user_keys/{id}_pub.pem", "wb") as f:
        f.write(key.public_key().export_key())

    h = MD5.new()
    h.update(key.export_key())
    return h.hexdigest()


def user_encrypt(id: str, content: bytes) -> bytes:
    with open(f"user_keys/{id}.pem", "rb") as f:
        pri_key = RSA.import_key(f.read())

    cipher_rsa = PKCS1_OAEP.new(pri_key)
    enc_content = cipher_rsa.encrypt(content)
    return enc_content
