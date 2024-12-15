import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    print("listening for incomming connection ")

    while True:
        client_sock, client_addr = server_socket.accept()
        print(f'{client_sock} connected to port')

        request = client_sock.recv(4096).decode().split(" ")
        # debugging purposes
        print(f'{request}')
        response = b'HTTP/1.1 200 OK\r\n\r\n'

        # exit loop if no request is gotten
        if not request:
            break

        if request[1]!= "/":
            client_sock.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        elif request[1] == "/":
            client_sock.sendall(response)
        elif request[1] == '/echo/':
            client_sock.sendall(response)

        else:
            print("invalid format")


if __name__ == "__main__":
    main()
