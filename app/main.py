import socket  # noqa: F401
import threading
import sys
import os
import argparse

connected_client = []
lock = threading.Lock()
File_dir = ''


def handle_client(client_sock):
    with lock:
        if client_sock not in connected_client:
            connected_client.append(client_sock)
        else:
            print('client is already in connected list')

    while True:

        request = client_sock.recv(4096).decode()
        if not request:
            break
        # debugging purposes
        print(f'{request}\n'
              f'{request[1]} \n '
              f'{request[1][6:]}\n')
        client_sock.send(accept_gzip(request))


def parse_headers(request):
    fields = request
    fields = fields.split('\r\n')
    fields = fields[1:]
    headers = {}
    for field in fields:
        if ':' in field:
            key, value = field.split(":", 1)
            headers[key] = value
    for key, value in headers.items():
        print(f'{key}:{value}')
    return headers


def parse_request(request):
    # not optimal but a path is usally on index 1
    global File_dir
    request.split()
    print(request)
    path = 1
    if request[path] == "/" and request[0] == 'GET':
        return 'HTTP/1.1 200 OK\r\n\r\n'
    elif request[path].startswith('/echo/'):
        value = request[1][6:]
        print(value)
        res = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(value)}\r\n\r\n{value}'
        return res
    elif request[path].startswith('/user-agent') and request[0] == 'GET':
        value = request[6]
        res = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(value)}\r\n\r\n{value}'
        return res

    elif request[path].startswith('/files/') and request[0] == 'GET':
        # it's reading from their servers not my local computer fyml
        try:
            directory = sys.argv[2]
            file = request[path][7:]
            file_path = os.path.join(directory, file)

            print(f'{file_path}')
            with open(file_path, 'r') as file:
                content = file.read()
                res = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                return res
        except FileNotFoundError:
            return f"HTTP/1.1 404 Not Found\r\n\r\n"

    elif request[0].startswith("POST"):
        directory = File_dir
        print(directory)  # debugging
        path = request[1][6:].strip('/')
        print(path)  # debugging
        files = " ".join(request[9:])  # read the data being sent by the post request
        file_path = f'{directory}{path}'
        print(file_path)  # debugging
        try:
            with open(file_path, 'w') as file:
                new = files.lstrip('/').split('_')
                print(new)  # debugging
                string = " ".join(new)
                print(string)
                print(len(string))
                file.write(string)
            return 'HTTP/1.1 201 Created\r\n\r\n'
        except Exception as e:
            print(f'{e}')
    else:
        return 'HTTP/1.1 404 Not Found\r\n\r\n'


def show_clients():
    for x, y in enumerate(connected_client):
        print(f'{x + 1}:{y}')


def accept_gzip(request):
    headers = parse_headers(request)
    if headers['Accept-Encoding'] == 'gzip':
        return 'HTTP/1.1 200 OK\r\n\r\n'
    else:
        return 'No GZIP'

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    parser = argparse.ArgumentParser('a simple http server')
    parser.add_argument("-d", "--directory")
    args = parser.parse_args()

    if 'directory' in args:
        global File_dir
        File_dir = args.directory

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("listening for incoming connection ")

    while True:
        client_sock, client_addr = server_socket.accept()
        my_thread = threading.Thread(target=handle_client, args=(client_sock,))
        my_thread.start()


if __name__ == "__main__":
    main()
