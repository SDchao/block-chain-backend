import hashlib
import io
import time

from minio import Minio

client = Minio("127.0.0.1:9002",
               "AKIAIOSFODNN7EXAMPLE",
               "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
               secure=False)


def uploadFileFromBytes(bucket_name: str, data: bytes):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    obj = io.BytesIO(data)
    hashFileName = hashlib.sha256(str(time.time()).encode()).hexdigest()
    obj_name = client.put_object(bucket_name, hashFileName, obj, len(data)).object_name
    return obj_name


def downloadFile(bucket_name: str, obj_name: str):
    response = client.get_object(bucket_name, obj_name)
    return response.read()


def modifyFile(bucket_name: str, obj_name: str, data: bytes):
    client.remove_object(bucket_name, obj_name)
    return uploadFileFromBytes(bucket_name, data)
