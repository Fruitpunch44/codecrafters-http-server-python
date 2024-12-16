import socket  # noqa: F401
import threading
import sys
import os

connected_client = []
lock = threading.Lock()


def handle_client(client_sock):
    with lock:
        if client_sock not in connected_client:
            connected_client.append(client_sock)
        else:
            print('client is already in connected list')

    while True:
        try:
            request = client_sock.recv(4096).decode().split()
            if not request:
                break
            # debugging purposes
            print(f'{request}\n'
                  f'{request[1]} \n '
                  f'{request[1][6:]}\n')
            files=request[1][6:]
            new = files.lstrip('/').split('_')
            print(new)
            response = parse_request(request)
            client_sock.send(response.encode())
        except Exception as e:
            print(f'{e}')
            client_sock.close()


def parse_request(request):
    # not optimal but a path is usally on index 1
    path = 1
    if request[path] == "/":
        return 'HTTP/1.1 200 OK\r\n\r\n'
    elif request[path].startswith('/echo/'):
        value = request[1][6:]
        print(value)
        res = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(value)}\r\n\r\n{value}'
        return res
    elif request[path].startswith('/user-agent'):
        value = request[6]
        res = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(value)}\r\n\r\n{value}'
        return res

    elif request[path].startswith('/files/'):
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
        except Exception as e:
            return f"HTTP/1.1 404 Not Found\r\n\r\n"

    elif request[0].startswith("POST"):
        directory = sys.argv[2]
        files = request[1][6:]
        file_path = os.path.join(directory, files)

        with open(file_path, 'w') as file:
            new = files.lstrip('/').split('_')
            print(new)
            content = file.write(new)
            print(content)
            return 'HTTP/1.1 201 Created\r\n\r\n'
    else:
        return 'HTTP/1.1 404 Not Found\r\n\r\n'


def show_clients():
    for x, y in enumerate(connected_client):
        print(f'{x + 1}:{y}')


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("listening for incoming connection ")

    while True:
        client_sock, client_addr = server_socket.accept()
        my_thread = threading.Thread(target=handle_client, args=(client_sock,))
        my_thread.start()


if __name__ == "__main__":
    main()
