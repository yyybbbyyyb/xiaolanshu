import os
from django.core.management.base import BaseCommand
from django.conf import settings
from application.utils import upload_img_file  # 确保路径正确
from io import BytesIO

# 运行 python manage.py test_upload_img /path/to/image.png    即可测试


class Command(BaseCommand):
    help = '测试上传本地图片到阿里云OSS'

    def add_arguments(self, parser):
        parser.add_argument('image_path', type=str, help='本地图片路径')

    def handle(self, *args, **kwargs):
        image_path = kwargs['image_path']

        if not os.path.exists(image_path):
            self.stdout.write(self.style.ERROR(f'文件路径 {image_path} 不存在'))
            return

        with open(image_path, 'rb') as image_file:
            image_content = BytesIO(image_file.read())
            img_url = upload_img_file(image_content)

            if img_url:
                self.stdout.write(self.style.SUCCESS(f'图片上传成功: {img_url}'))
            else:
                self.stdout.write(self.style.ERROR('图片上传失败'))
