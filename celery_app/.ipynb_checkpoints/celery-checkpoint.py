# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import os
from .train_post import decode_image_from_base64jpeg
from .train_post import post_images_to_model
from .template_post import post_template_to_model
from glob import glob
import base64
import sys
from glob import glob
import cv2
import numpy as np
import requests
import json
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# 创建Celery实例
app = Celery('myproject')

# 从Django设置中加载Celery配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现Celery任务
app.autodiscover_tasks()
