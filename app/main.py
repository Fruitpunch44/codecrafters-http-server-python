# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    IP = '127.0.0.1'
    PORT = 4221

    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)'''
    server_socket=socket.create_server((IP,4221),reuse_port=True)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)

    print(f'{IP} waiting for connections on PORT {PORT}')

    while True:
        client_soc, client_addr = server_socket.accept()
        print(f'connected to {PORT} ON {client_addr}')
        response = 'HTTP/1.1 200 OK\r\n\r\n'
        client_soc.send(response.encode())

        response = client_soc.recv(1024).decode()
        if not response:
            print('no response gotten')
            break


if __name__ == "__main__":
    main()
