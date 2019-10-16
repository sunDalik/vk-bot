# Example usage:
# get_msg(msg_list, 'temp')

import numpy as np
from keras.applications.xception import Xception, preprocess_input, decode_predictions
from keras.preprocessing import image
import random
import json

model = Xception(
    include_top=True,
    weights='imagenet',
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000
)

with open('img2msg/image-mapping.json', 'r') as f:
    image_mapping = json.load(f)

def get_msg(msg_list, img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    keywords = [pred[1] for pred in decode_predictions(preds, top=3)[0]]
    for k in keywords:
        if k not in image_mapping:
            continue
        msg_indexes = image_mapping[k]
        if len(msg_indexes) > 0:
            print('Predicted image as {' + ', '.join(keywords) + '}. Picked ' + k)
            i = random.choice(msg_indexes)
            if i < len(msg_list):
                return msg_list[i]

