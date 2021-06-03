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
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_sock = socket.socket()
    server_sock.bind(('localhost', 15000))
    server_sock.listen()
    max_threads = int(sys.argv[2])
    threads = []
    try:
        while True:
            thread_connected = 0
            n_urls = 0

            client_sock, addr = server_sock.accept()  # read

            try:
                print('connect from', addr)
                while True:
                    data = client_sock.recv(4096)
                    if not data:
                        break
                    if thread_connected == max_threads:
                        for th in threads:
                            th.join()
                            n_urls += 1
                            print(f"{n_urls} processed")
                        threads.clear()
                        thread_connected = 0
                    threads.append(threading.Thread(target=get_text, args=(client_sock, data,)))

                    threads[thread_connected].start()

                    thread_connected += 1
            except:
                break
            finally:
                for th in threads:
                    th.join()
                    n_urls += 1
                    print(f"{n_urls} processed")
                threads.clear()
                client_sock.close()
    except:
        pass
    finally:
        server_sock.close()


if __name__ == '__main__':
    # tasks.append(server())
    # event_loop()
    server()
