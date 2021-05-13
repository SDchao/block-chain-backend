from .basic import uploadFileFromBytes, downloadFile, modifyFile


def upload_cert(data: bytes) -> str:
    return uploadFileFromBytes("CERTS", data)


def download_cert(obj_name: str) -> bytes:
    return downloadFile("CERTS", obj_name)


def modify_cert(obj_name: str, data: bytes) -> str:
    return modifyFile("CERTS", obj_name, data)
