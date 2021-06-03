import socket
import sys
import threading


def send_url(client_sock, url):
    # print(url)
    client_sock.send(url.encode())
    # print(url)


def load(file_name):
    m = int(sys.argv[1])
    # print(m)
    f = open(file_name, 'r')
    # urls = set(f.read().split('\n'))
    # print(urls)
    client_sock = socket.socket()
    client_sock.connect(('localhost', 15000))
    try:

        # threads = [threading.Thread(target=send_url, args=(client_sock, f'{urls.pop()}',))
        #            for i in range(m)]
        threads = []
        for i in range(m):
            url = f.readline()
            threads.append(threading.Thread(target=send_url, args=(client_sock, url,)))
        # print(threads)

        for th in threads:
            th.start()
        for th in threads:
            print(th)
            th.join()

    except:
        pass
    finally:
        for i in range(m):
            url = client_sock.recv(4096)
            if not url:
                break
            print(url.decode('unicode-escape'))
        client_sock.close()


if __name__ == '__main__':
    load(sys.argv[2])
