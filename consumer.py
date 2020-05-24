from kafka import KafkaConsumer
from datetime import datetime as dt
import time
import cv2

from image_encoder import encode_image, decode_image
import matplotlib.pyplot as plt


topic_name = 'testing'
group_id = 'read_images'
kafka_server = 'prokulski.science:9092'

listner = KafkaConsumer(topic_name,
    group_id=group_id,
    bootstrap_servers=kafka_server)

print(listner)

# wait for message
for msg in listner:

    ts = dt.fromtimestamp(int(msg.timestamp)/1000)
    print(ts.strftime("%H:%M:%S @ %Y-%m-%d"))

    # if message key is "image"?
    if msg.key == b'image':
        # deocde JSON to image
        img = decode_image(msg.value)
        # show image
        cv2.imshow("Dest", img)
    else:
        # other key - just show message
        print(f"Key = '{msg.key}'\nValue = '{msg.value}'\n")

    # wait for ESC in preview window
    if cv2.waitKey(1) == 27:
        break


cv2.destroyAllWindows()
