import base64
import json
import os
import sys
from glob import glob

import cv2
import numpy as np
import requests

def decode_image_from_base64jpeg(base64_image):
    image_bytes = base64.b64decode(base64_image)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return image

def post_images_to_model(encoded_images,user_id):
    datas = json.dumps({
        "user_id"               : user_id, 
        "sd_model_checkpoint"   : "Chilloutmix-Ni-pruned-fp16-fix.safetensors",
        "resolution"            : 512,
        "val_and_checkpointing_steps" : 100,
        "max_train_steps"       : 800,
        "steps_per_photos"      : 200,
        "train_batch_size"      : 1,
        "gradient_accumulation_steps" : 4,
        "dataloader_num_workers" : 16,
        "learning_rate"         : 1e-4,
        "rank"                  : 64,
        "network_alpha"         : 64,
        "instance_images"       : encoded_images, 
    })
    r = requests.post('http://region-3.seetacloud.com:12351/easyphoto/easyphoto_train_forward', data=datas, timeout=2000)
    data = r.content.decode('utf-8')
    return data

if __name__ == '__main__':
    img_dir     = sys.argv[1]
    img_list    = glob(os.path.join(img_dir, "*.jpg")) + glob(os.path.join(img_dir, "*.JPG"))+ glob(os.path.join(img_dir, "*.png"))
    encoded_images = []
    for idx, img_path in enumerate(img_list):
        with open(img_path, 'rb') as f:
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
            encoded_images.append(encoded_image)
    outputs = post_images_to_model(encoded_images)
    outputs = json.loads(outputs)

    print(outputs)