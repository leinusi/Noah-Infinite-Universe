from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve
import uuid
from django.db.models import Q
from django.shortcuts import render
from .models import Imgg
from django_web_app.settings import BASE_DIR
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.conf import settings
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
from .models import ViewImage
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from celery_app.tasks import uploadImg
from celery_app.tasks import ImageCreate
from django.http import HttpResponse
from django.shortcuts import render
import os

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)



def ComicView(request):#漫画文案上传部分视图
    user = request.user
    if request.method == 'POST':
        story_background = request.POST.get('story_background', '')
        user_folder3 = os.path.join(settings.MEDIA_ROOT, 'comic_text', str(user.username))

        if not os.path.exists(user_folder3):
            os.makedirs(user_folder3)

        file_path = os.path.join(user_folder3, 'story_background.txt')#生成txt文案文件

        # 分割文本并移除逗号
        segments = story_background.split(',')
        formatted_text = '\n'.join(segment.strip() for segment in segments)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_text)

        return redirect(reverse('comic', kwargs={'username': user.username}))

    # GET请求处理
    else:
        return render(request, 'blog/comic.html')
def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'posts':result }
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/comic.html'
    fields = ('content',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def my_view(request):
    # 调用Celery任务
    result = uploadImg.delay(request)
    # 获取任务的ID
    task_id = result.id
    # 获取任务的状态
    task_status = result.status
    # 获取任务的结果（如果有）
    task_result = result.get()
    # 返回响应或其他操作
    return render(request, 'blog/home.html', {'task_id': task_id, 'task_status': task_status, 'task_result': task_result})

def Imgcreate_view(request):
    # 调用Celery任务
    result = ImageCreate.delay(request)
    # 获取任务的ID
    task_id = result.id
    # 获取任务的状态
    task_status = result.status
    # 获取任务的结果（如果有）
    task_result = result.get()
    # 返回响应或其他操作
    return render(request, 'blog/result.html', {'task_id': task_id, 'task_status': task_status, 'task_result': task_result})    


def ImageCreate(request):  # 模版上传
    # 初始化
    encoded_images = []
    user = request.user

    # POST请求处理
    if request.method == 'POST':
        files = request.FILES.getlist('Chars')
        user_folder2 = os.path.join(settings.MEDIA_ROOT, 'temps', str(user.username))

        # 创建用户目录
        if not os.path.exists(user_folder2):
            os.makedirs(user_folder2)

        # 创建results子目录
        results_folder = os.path.join(settings.MEDIA_ROOT, 'results', str(user.username))
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

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

                    # 使用当前时间作为文件名
                    current_time_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
                    cv2.imwrite(os.path.join(results_folder, current_time_filename), image)  # 保存到results子目录

        return redirect(reverse('blog-ImgShow', kwargs={'username': user.username}))

    # GET请求处理
    else:
        return render(request, 'blog/post_form.html')

    
def show_images(request, username):
    if request.user.is_authenticated:
        # 定义子目录路径
        sub_dir_path = os.path.join('results', request.user.username)
        # 获取完整的文件夹路径
        dir_path = os.path.join(settings.MEDIA_ROOT, sub_dir_path)
        if os.path.exists(dir_path):
            # 获取该文件夹下的所有图片文件，并且为每个图片生成相对于MEDIA_ROOT的路径
            images = [os.path.join(sub_dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            images.reverse()  # 反转图片列表，使其按相反顺序排列
            return render(request, 'blog/user_posts.html', {'images': images})
        else:
            return HttpResponse("您的图片还未制作成功哦！请耐心等待")
    else:
        return HttpResponse("请登录来查看您的内容")
   

def image_view(request, image_id):
    # 获取指定ID的图片对象
    img_obj = get_object_or_404(ViewImage, image_id=image_id)

    # 构造图片文件的完整路径
    image_path = img_obj.image_file_path

    # 检查图片文件是否真的存在
    if not os.path.exists(image_path):
        raise Http404("Image not found")

    # 打开图片并读取内容
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # 返回图片内容作为响应
    return HttpResponse(image_data, content_type='image/png')


def uploadImg(request):#用户肖像上传
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
    
    
def get_number(request):#用来获取等待时间的函数
    # 我们要轮询的服务器的 URL
    url = 'http://region-3.seetacloud.com:12351/easyphoto/get_num'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        # 如果请求失败，返回错误信息
        return JsonResponse({'error': str(e)}, status=500)
    
    try:
        # 假设响应是 JSON 格式，并包含一个名为 'number' 的键
        data = response.json()
        number = data['number']
    except Exception as e:
        # 如果解析失败或键不存在，返回错误信息
        
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'number': number})
