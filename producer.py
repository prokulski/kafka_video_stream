from kafka import KafkaProducer
import time
import cv2

from image_encoder import encode_image, decode_image


# kafka producer
producer = KafkaProducer(bootstrap_servers='prokulski.science:9092')
topic_name = 'testing'


# video capture
cap = cv2.VideoCapture(0)

while True:
	teraz = time.time()
	rst, img = cap.read()

	if not rst:
		break

	img = cv2.resize(img, (320,200))

	data_json = encode_image(img)

	producer.send(topic_name, key=b'image', value=bytes(data_json, encoding='utf-8'))
	producer.flush()

	cv2.imshow("Surce", img)

	print((time.time() - teraz)*1000)

	if cv2.waitKey(1) == 27:
		break



cv2.destroyAllWindows()
