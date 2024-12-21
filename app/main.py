import socket  # noqa: F401
import threading
import sys
import os
import gzip
import argparse

connected_client = []
File_dir = ''


def handle_client(client_sock):
    if client_sock not in connected_client:
        connected_client.append(client_sock)
    else:
        print('client is already in connected list')

    while True:

        request = client_sock.recv(4096).decode()
        if not request:
            break
        # debugging purposes
        print(f'{request}')
        response = parse_request(request)
        client_sock.sendall(response.encode())


def parse_headers(request):
    fields = request.split('\r\n')
    fields = fields[2:]
    headers = {}
    for field in fields:
        if ':' in field:
            key, value = field.split(":", 1)
            headers[key] = value
    return headers


def parse_request(request):
    # not optimal but a path is usally on index 1
    global File_dir
    print(request)
    print(request[1])
    print(request.split())
    print(request.split()[0])
    print(request.split()[1][6:].strip('/'))

    path = 1
    filename = request[1][6:]
    if request.split()[path] == "/" and request.split()[0] == 'GET':
        return 'HTTP/1.1 200 OK\r\n\r\n'

    elif request.split()[path].startswith(f'/echo/{filename}') and request.split()[0] == 'GET':
        value = request.split()[1][6:]
        gzip_header_present = accept_gzip(request)
        if gzip_header_present:
            return gzip_header_present
        else:
            return f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(value)}\r\n\r\n{value}'

    elif request.split()[path].startswith('/user-agent') and request.split()[0] == 'GET':
        value = request.split()[6]
        res = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(value)}\r\n\r\n{value}'
        return res

    elif request.split()[path].startswith('/files/') and request.split()[0] == 'GET':
        try:
            directory = sys.argv[2]
            file = request.split()[path][7:]
            file_path = os.path.join(directory, file)
            with open(file_path, 'r') as file:
                content = file.read()
                res = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                return res
        except FileNotFoundError:
            return f"HTTP/1.1 404 Not Found\r\n\r\n"

    elif request.split()[0].startswith("POST"):
        directory = File_dir
        print(f'directory_loc:{directory}')  # debugging
        path = request.split()[1][6:].strip('/')
        print(f'path:{path}')  # debugging
        files = " ".join(request.split()[9:])
        # read the data being sent by the post-request
        print(f'files to save:{files}')
        file_path = f'{directory}{path}'
        print(f'path: {file_path}')  # debugging
        try:
            with open(file_path, 'w') as file:
                new = files.lstrip('/').split('_')
                string = " ".join(new)
                file.write(string)
            return 'HTTP/1.1 201 Created\r\n\r\n'
        except Exception as e:
            print(f'{e}')
    else:
        return f"HTTP/1.1 404 Not Found\r\n\r\n"


def show_clients():
    for x, y in enumerate(connected_client):
        print(f'{x + 1}:{y}')


def accept_gzip(request):
    body = request.split()[1][6:]
    print(f'message:{body}')
    headers = parse_headers(request)
    if 'Accept-Encoding' in headers:
        if 'gzip' in headers['Accept-Encoding']:
            compressed = gzip.compress(body.encode())
            print(f'compressed_message={compressed}')
            print(f'decoded:{compressed.hex()}')
            print(f'length_of_compressed:{len(compressed)}')
            res = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Encoding: gzip\r\n'
                f'Content-Length: {len(compressed)}\r\n'
                '\r\n'
                f'{compressed.hex()}'
            )
            print(f"response to send: {res}")
            return res
    return None


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
