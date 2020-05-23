import base64
import numpy as np
import cv2
import json

def encode_image(image_binary):
    """
    @image_binary - obrazek wczytany przez OpenCV
    """
    image_binary = cv2.cvtColor(image_binary, cv2.COLOR_RGB2BGR)
    base64_encoded_data = base64.b64encode(image_binary)
    base64_message = base64_encoded_data.decode('utf-8')

    json_image = json.dumps({"dim": [image_binary.shape[i] for i in range(image_binary.ndim)],
                           "data": base64_message})
    return(json_image)


def decode_image(image_json):
    """
    @image_json - JSON zwrócony przez encode_image()
    """
    data = json.loads(image_json)
    base64_img_bytes = data['data'].encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    img_array = [i for i in bytearray(decoded_image_data)]
    
    img_array = np.reshape(img_array, data['dim'])
    img_array = img_array.astype(np.uint8)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

    return(img_array)
