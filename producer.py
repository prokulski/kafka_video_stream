from kafka import KafkaProducer
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
	img = cv2.resize(img, (320,200))

	# encode to JSON
	data_json = encode_image(img)

	# send to kafka
	producer.send(topic_name, key=b'image', value=bytes(data_json, encoding='utf-8'))
	producer.flush()

	# show preview
	cv2.imshow("Surce", img)


	# exit on ESC
	if cv2.waitKey(1) == 27:
		break


cv2.destroyAllWindows()
