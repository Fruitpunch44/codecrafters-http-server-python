import socket  # noqa: F401
import threading
import sys

connected_client = []


def handle_client(client_sock):
    if client_sock not in connected_client:
        connected_client.append(client_sock)
    else:
        print('client is already in connected list')

    while True:
        request = client_sock.recv(4096).decode().split()
        if not request:
            break
        # debugging purposes
        print(f' {request}\n{request[1]} \n {request[1][6:]}')
        response = parse_request(request)
        client_sock.send(response.encode())
    show_clients()


def parse_request(request):
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

    elif request[path].startswith('/files'):
        file_path=r'C:\Users\Olu-Ade\HTTP CODE CRAFTERS\codecrafters-http-server-python\app\files\hello.txt'
        with open(file_path, 'r') as file:
            content = file.read()
            res = (f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\n"
                   f"Content-Length: {len(content)}\r\n\r\n{content}").encode()
            return res

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
        print(f'{client_sock} connected to port')


if __name__ == "__main__":
    main()
