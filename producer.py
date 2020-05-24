from kafka import KafkaProducer

from datetime import datetime as dt
import time
import cv2

from image_encoder import encode_image, decode_image


topic_name = 'testing'
kafka_server = 'prokulski.science:9092'

# kafka producer
producer = KafkaProducer(bootstrap_servers=kafka_server)

# video capture
cap = cv2.VideoCapture(0)


while True:
	# grab image
	rst, img = cap.read()

	if not rst:
		break

	# resize image
	img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))

	# add timestamp to image
	ts = dt.fromtimestamp(time.time())
	img = cv2.putText(img, ts.strftime("%H:%M:%S @ %Y-%m-%d"), (0, 11), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

	# encode to JSON
	data_json = encode_image(img)

	# send to kafka
	producer.send(topic_name, key=b'image', value=bytes(data_json, encoding='utf-8'))
	producer.flush()

	# show preview
	cv2.imshow("Source", img)


	# exit on ESC
	if cv2.waitKey(1) == 27:
		break


cv2.destroyAllWindows()
