from logger import logger
from .basic import uploadFileFromBytes, downloadFile, modifyFile

CERT_BUCKET_NAME = "certs"


def upload_cert(data: bytes) -> str:
    logger.info(f"Uploading cert to minio")
    return uploadFileFromBytes(CERT_BUCKET_NAME, data)


def download_cert(obj_name: str) -> bytes:
    logger.info(f"Getting cert from minio, name: {obj_name}")
    return downloadFile(CERT_BUCKET_NAME, obj_name)


def modify_cert(obj_name: str, data: bytes) -> str:
    logger.info(f"Modifying cert from minio, name: {obj_name}")
    return modifyFile(CERT_BUCKET_NAME, obj_name, data)
