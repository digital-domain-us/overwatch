import socket
import select


class RobotSRV(object):
    def __init__(self):
        self.header_length = 10
        self.ip = "192.168.1.165"
        self.port = 8000
        self.server_socket = self.create_socket()
        self.socket_list = []
        self.clients = {}

    def create_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP, PORT))
        server_socket.listen()
        return server_socket

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': self.client_socket.recv(message_length)}
        except:
            return False

    def start_server(self):
        self.sockets_list = [self.server_socket]
        print('Listening for connections on {self.ip}:{self.port}...')
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    self.client_socket, client_address = self.server_socket.accept()
                    user = receive_message(self.client_socket)
                    if user is False:
                        continue
                    self.sockets_list.append(self.client_socket)
                    self.clients[self.client_socket] = user
                    # print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                else:
                    message = receive_message(notified_socket)
                    if message is False:
                        print(
                            'Closed connection from: {}'.format(self.clients[notified_socket]['data'].decode('utf-8')))
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        continue
                    user = self.clients[notified_socket]
                    # print('Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                    for self.client_socket in self.clients:
                        if self.client_socket != notified_socket:
                            self.client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]