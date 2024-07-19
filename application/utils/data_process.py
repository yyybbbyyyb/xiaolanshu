import json
import uuid
import oss2
from itertools import chain

from django.core.files.storage import get_storage_class
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest
from django.conf import settings


def parse_request_data(request: HttpRequest) -> dict:
    """
    Parse request data to dict
    :param request: HttpRequest
    :return: dict
    """
    if request.method == 'GET':
        return request.GET.dict()
    elif request.method == 'POST':
        try:
            return json.loads(request.body.decode())
        except json.JSONDecodeError:
            return {}
    else:
        return {}


UPLOAD_FOLDER_MAPPING = {
    'avatar': 'media/avatar/',
    'dish': 'media/dish/',
    'cafeteria': 'media/cafeteria/',
    'counter': 'media/counter/',
    'default': 'media/default/',
}


def upload_img_file(image, folder='default'):
    """
    上传图片
    :param folder: 上传文件夹
    :param image: 二进制图片
    :return: 图片路径
    """

    number = uuid.uuid4()
    img_name = UPLOAD_FOLDER_MAPPING[folder] + str(number) + '.jpg'
    img_url = settings.OSS_MEDIA_URL + img_name

    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_END_POINT, settings.OSS_BUCKET_NAME)

    try:
        bucket.put_object(img_name, image.read())
        return img_url
    except oss2.exceptions.OssError as e:
        print(f"上传图片失败: {e}")
        return ''
