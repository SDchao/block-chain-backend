import io
import os

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

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
    with open(f"user_keys/{id}_pub.pem", "rb") as f:
        key = RSA.import_key(f.read())

    session_key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(content)

    return enc_session_key + cipher_aes.nonce + tag + ciphertext


def user_decrypt(id: str, content: bytes) -> bytes:
    with open(f"user_keys/{id}.pem", "rb") as f:
        key = RSA.import_key(f.read())

    f = io.BytesIO(content)
    enc_session_key, nonce, tag, ciphertext = \
        [f.read(x) for x in (key.size_in_bytes(), 16, 16, -1)]

    cipher_rsa = PKCS1_OAEP.new(key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    dec_content = cipher_aes.decrypt_and_verify(ciphertext, tag)

    return dec_content


if __name__ == '__main__':
    r = b'I LOVE YOU'
    assert r == user_decrypt(340503, user_encrypt('340503', r))