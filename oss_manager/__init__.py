from .basic import uploadFileFromBytes, downloadFile, modifyFile

CERT_BUCKET_NAME = "certs"


def upload_cert(data: bytes) -> str:
    return uploadFileFromBytes(CERT_BUCKET_NAME, data)


def download_cert(obj_name: str) -> bytes:
    return downloadFile(CERT_BUCKET_NAME, obj_name)


def modify_cert(obj_name: str, data: bytes) -> str:
    return modifyFile(CERT_BUCKET_NAME, obj_name, data)
