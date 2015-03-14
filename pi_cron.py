import schedule
import threading 
from time import sleep
from datetime import datetime
from subprocess import call

REPEATED_TIMES = 6

class Uploader(threading.Thread):
	def __init__(self, file_name):
		threading.Thread.__init__(self)
		self.image_path = file_name
	def run(self):
		print "start uploading " + self.image_path
		sleep(2) # sleep for 2 secs
		print "done uploading " + self.image_path 
		
def capture_image():
	print "capturing ..."
	file_name =  generate_file_name()
	call(["fswebcam", "-r", '640x480' , '--no-banner', '/home/pi/webcam/' + file_name + '.jpg', ])
	return file_name

def upload_image(image_path):
	print "uploading image"
	uploader = Uploader(image_path)
	uploader.start()
	uploader.join()

def capture_and_upload():
	img_path = capture_image()
	upload_image(img_path)

def generate_file_name():
	return "img_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".jpg"

if __name__ == "__main__":
	schedule.every(10).seconds.do(capture_and_upload)
	executed_times = 0
	while True:
		schedule.run_pending()