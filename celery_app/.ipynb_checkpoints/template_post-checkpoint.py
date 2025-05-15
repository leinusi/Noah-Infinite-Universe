
import base64
import json
import os
import sys
from glob import glob
import random

import cv2
import numpy as np
import requests

def decode_image_from_base64jpeg(base64_image):
    image_bytes = base64.b64decode(base64_image)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return image

def post_template_to_model(user_id, encoded_image):
    datas = json.dumps({
        "user_ids": user_id,
        "sd_model_checkpoint": "Chilloutmix-Ni-pruned-fp16-fix.safetensors",
        "init_image": encoded_image,
        "first_diffusion_steps": 50,
        "first_denoising_strength": 0.45,
        "second_diffusion_steps": 20,
        "second_denoising_strength": 0.35,
        "seed": 12345,
        "crop_face_preprocess": True,
        "before_face_fusion_ratio": 0.5,
        "after_face_fusion_ratio": 0.5,
        "apply_face_fusion_before": True,
        "apply_face_fusion_after": True,
        "color_shift_middle": True,
        "color_shift_last": True,
        "super_resolution": True,
        "background_restore": False,
        "tabs": 1
    })
    r = requests.post('http://region-3.seetacloud.com:12351/easyphoto/easyphoto_infer_forward', data=datas, timeout=1500)
    data = r.content.decode('utf-8')
    return data

if __name__ == '__main__':
    img_dir = sys.argv[1]
    img_list = glob(os.path.join(img_dir, "*.jpg")) + glob(os.path.join(img_dir, "*.JPG")) + glob(os.path.join(img_dir, "*.png"))
    encoded_images = []
    for idx, img_path in enumerate(img_list):
        with open(img_path, 'rb') as f:
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
            outputs = post_template_to_model(user_id, encoded_image)
            outputs = json.loads(outputs)
            image = decode_image_from_base64jpeg(outputs["outputs"][0])
            
            # 生成一个随机数作为文件名
            random_filename = str(random.randint(1000000, 9999999)) + ".jpg"
            cv2.imwrite(random_filename, image)