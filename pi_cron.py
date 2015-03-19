import schedule
import threading
import os
import sys
import locale
from time import sleep
from datetime import datetime
from subprocess import call
from daemon import Daemon

from dropbox import client, rest, session

class Uploader(threading.Thread):
	def __init__(self, local_file_name, remote_file_name, dropbox_client):
		threading.Thread.__init__(self)
		self.dropbox_client = dropbox_client
		self.image_path = local_file_name
		self.remote_file_name = remote_file_name

	def run(self):
		print "start uploading " + self.image_path
		self.dropbox_client.do_put(self.image_path, self.remote_file_name)
		print "done uploading " + self.image_path 
		
class DBClient():
	TOKEN_FILE = "token_store.txt"
	def __init__(self):
		self.api_client = None
		self.current_path = '/'
		try:
			serialized_token = open(self.TOKEN_FILE).read()
			if serialized_token.startswith('oauth2:'):
				access_token = serialized_token[len('oauth2:'):]
				self.api_client = client.DropboxClient(access_token)
				print "[loaded OAuth 2 access token]"
			else:
				print "Malformed access token in %r." % (self.TOKEN_FILE,)
		except IOError:
			pass # don't worry if it's not there

	def do_put(self, from_path, to_path):
		"""
		Copy local file to Dropbox

        Examples:
        Dropbox> put ~/test.txt dropbox-copy-test.txt
		"""
		from_file = open(os.path.expanduser(from_path), "rb")
		encoding = locale.getdefaultlocale()[1] or 'ascii'
		full_path = (self.current_path + "/" + to_path).decode(encoding)
		self.api_client.put_file(full_path, from_file)

class PiHandler(Daemon):
	def run(self):
		self.db_client = DBClient()
		self.is_running = True
		schedule.every(10).seconds.do(self.capture_and_upload)
		while True:
			schedule.run_pending()

	def capture_and_upload(self):
		img_path, image_file = self.capture_image()
		self.upload_image(self.db_client, img_path, image_file)
		print "capture and upload ..."

	def capture_image(self):
		print "capturing ..."
		file_name =  self.generate_file_name()
		call(["fswebcam", "-r", '640x480' , '--no-banner', '/home/pi/webcam/' + file_name, ])
		file_path = '/home/pi/webcam/' + file_name
		return file_path, file_name

	def upload_image(self, dropbox_client, image_path, remote_file_name):
		print "uploading image"
		uploader = Uploader(image_path, remote_file_name, dropbox_client)
		uploader.start()
		uploader.join()
	
	def generate_file_name(self):
		return "img_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".jpg"

if __name__ == "__main__":
	# pi_handler = PiHandler()
	# pi_handler.start()
	daemon = PiHandler('/tmp/daemon-pi-camera.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)