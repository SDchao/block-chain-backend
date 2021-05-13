from minio import Minio
from minio.error import S3Error
import time
import hashlib
import io

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


def downloadFile(bucket_name: str, objname: str):
    response = client.get_object(bucket_name, objname)
    return response.read()


def modifyFile(bucket_name: str, data: bytes):
    for obj in client.list_objects(bucket_name):
        client.remove_object(bucket_name, obj.object_name)
    obj = io.BytesIO(data)
    hashFileName = hashlib.sha256(str(time.time()).encode()).hexdigest()
    obj_name = client.put_object(bucket_name, hashFileName, obj, len(data)).object_name
    return obj_name
