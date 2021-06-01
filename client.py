import socket


def load(file_name):
    f = open(file_name, 'r')
    # urls = f.read().split('\n')
    client_sock = socket.socket()
    client_sock.connect(('localhost', 15000))
    # print(urls)
    # for url in urls:
    #     client_sock.send(url.encode())
    while True:
        data=f.readline().encode()
        if not data:
            break
        client_sock.send(data)
        data = client_sock.recv(4096)
        if not data:
            break
        print(data)
    client_sock.close()

if __name__ == '__main__':
    load("urls.txt")
