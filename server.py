import operator
import socket
from select import select
import threading
import requests
from bs4 import BeautifulSoup
from collections import Counter
import sys
import json
import argparse
import lxml

tasks = []
# sock: gen
to_read = {}
to_write = {}


def get_text(client_sock, url):
    url = url[:-1]
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    tag_list = [tag.name for tag in soup.find_all()]
    text = [word.text.split() for word in soup.find_all(tag_list)]
    words = []
    for tmp_words in text:
        for word in tmp_words:
            words.append(word)
    words = Counter(words)
    top_words = dict(sorted(words.items(), key=operator.itemgetter(1), reverse=True)[:int(sys.argv[4])])
    print(top_words)
    client_sock.send(json.dumps(top_words).encode())


def server():
    # server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock = socket.socket()
    server_sock.bind(('localhost', 15000))
    server_sock.listen()
    max_threads = int(sys.argv[2])

    threads = []
    try:
        while True:
            try:
                client_sock, addr = server_sock.accept()  # read
            except socket.error:
                break
            else:
                n_threads = 0
                thread_connected = 0
                print('connect from', addr)
                while True:
                    data = client_sock.recv(4096)
                    if not data:
                        break
                    if n_threads == max_threads:
                        for th in threads:
                            th.join()
                        threads.clear()
                    threads.append(threading.Thread(target=get_text, args=(client_sock, data,)))
                    n_threads += 1
                    threads[thread_connected].start()
                    print(thread_connected)
                    thread_connected = (thread_connected + 1) % max_threads
            finally:
                client_sock.close()
    finally:
        server_sock.close()


# def client(client_sock,data):
#     while True:
#         yield 'read', client_sock
#         # data = client_sock.recv(4096)  # read
#
#         if not data:
#             break
#         else:
#             yield 'write', client_sock
#             client_sock.send(data.decode().upper().encode())  # write
#
#     client_sock.close()


# def event_loop():
#     while any([tasks, to_read, to_write]):
#
#         while not tasks:
#             ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
#
#             for sock in ready_to_read:
#                 tasks.append(to_read.pop(sock))
#
#             for sock in ready_to_write:
#                 tasks.append(to_write.pop(sock))
#
#         try:
#             task = tasks.pop(0)
#             op_type, sock = next(task)
#
#             if op_type == 'read':
#                 to_read[sock] = task
#             elif op_type == 'write':
#                 to_write[sock] = task
#
#         except StopIteration:
#             pass
#

if __name__ == '__main__':
    # tasks.append(server())
    # event_loop()
    server()
