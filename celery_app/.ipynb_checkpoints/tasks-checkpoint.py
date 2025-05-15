# tasks.py
from __future__ import absolute_import, unicode_literals
from celery_app.celery import app
import os
from celery import Celery
import uuid
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
from django.shortcuts import redirect
from django.shortcuts import render, redirect, reverse
from django.conf import settings
import os
import uuid
import base64
import json
import cv2

@app.task
def uploadImg(request):
    # 用户肖像上传
    if request.method == 'POST':
        # 如果是POST请求，处理上传的文件
        files = request.FILES.getlist('Imgg')

        # 获取当前用户
        user = request.user
        # 创建用户文件夹
        user_folder = os.path.join(settings.MEDIA_ROOT,'photo', str(user.username))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        # # 确保目标文件夹存在，如果不存在则创建它
        # photos_dir = os.path.join(settings.BASE_DIR, 'media', 'photos')
        # if not os.path.exists(photos_dir):
        #     os.makedirs(photos_dir)
        
        for idx, f in enumerate(files):
            # 使用安全的文件名，例如UUID
            safe_filename = str(uuid.uuid4()) + os.path.splitext(f.name)[1]
            destination = os.path.join(user_folder, safe_filename)
            
            with open(destination, 'wb+') as destination_file:
                for chunk in f.chunks():
                    destination_file.write(chunk)

                # 直接执行图片处理逻辑，而不是通过标志文件
        img_dir = user_folder
        img_list = glob(os.path.join(img_dir, "*.jpg")) + glob(os.path.join(img_dir, "*.JPG")) + glob(os.path.join(img_dir, "*.png"))
        encoded_images = []
        for idx, img_path in enumerate(img_list):
             with open(img_path, 'rb') as f:
                    encoded_image = base64.b64encode(f.read()).decode('utf-8')
                    encoded_images.append(encoded_image)

        user_id = str(request.user.username)
        outputs = post_images_to_model(encoded_images,str(user.username))
        outputs = json.loads(outputs)

        print(outputs)

        # 处理完上传后，可以执行重定向或其他操作
        return redirect('blog-ImgCreate')
    else:
        # 如果是GET请求，渲染表单或其他操作
        return render(request, 'blog/home.html')

    
    

@app.task
def ImageCreate(request):
    # 模版上传
    # 初始化
    encoded_images = []
    user = request.user
    
    # POST请求处理
    if request.method == 'POST':
        files = request.FILES.getlist('Chars')
        user_folder2 = os.path.join(settings.MEDIA_ROOT, 'temps', str(user.username))
        
        # 创建目录
        if not os.path.exists(user_folder2):
            os.makedirs(user_folder2)
        
        for idx, f in enumerate(files):
            # 使用安全的文件名，例如UUID
            safe_filename = str(uuid.uuid4()) + os.path.splitext(f.name)[1]
            destination = os.path.join(user_folder2, safe_filename)
            
            # 写文件
            with open(destination, 'wb+') as destination_file:
                for chunk in f.chunks():
                    destination_file.write(chunk)
                
                # 如果是第一个文件，进行编码
                if f == files[0]:
                    destination_file.seek(0)
                    encoded_image = base64.b64encode(destination_file.read()).decode('utf-8')
                    outputs = post_template_to_model(str(user.username), encoded_image)
                    outputs = json.loads(outputs)
                    image = decode_image_from_base64jpeg(outputs["outputs"][0])
                    cv2.imwrite(os.path.join(user_folder2, str(idx) + ".jpg"), image)
                    
        return redirect(reverse('blog-ImgShow', kwargs={'username': user.username}))

    # GET请求处理
    else:
        return render(request, 'blog/post_form.html')
