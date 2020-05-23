from kafka import KafkaConsumer
from datetime import datetime as dt
import time
import cv2

from image_encoder import encode_image, decode_image
import matplotlib.pyplot as plt


topic_name = 'testing'
listner = KafkaConsumer(topic_name,
	group_id='read_images',
	bootstrap_servers='prokulski.science:9092')


i = 0

for msg in listner:
	teraz = time.time()
	i += 1
	
	if msg.key == b'image':
		img = decode_image(msg.value)
		cv2.imshow("Dest", img)
	else:
		ts = dt.fromtimestamp(int(msg.timestamp)/1000)
		print(i, ts.strftime("%H:%M:%S @ %Y-%m-%d"))
		print(f"Key = '{msg.key}'\nValue = '{msg.value}'\n")

	print((time.time() - teraz)*1000)

	if cv2.waitKey(1) == 27:
		break



cv2.destroyAllWindows()
