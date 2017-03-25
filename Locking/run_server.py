from centeral_locking import CenteralLockerServer

"""
    This file is responsible for open sockets to all urls and waiting any message
    that will pass thought it
"""


def run_server():
    urls = ["tcp://127.0.0.1:5555", "tcp://127.0.0.1:5556"]
    server = CenteralLockerServer(urls=urls)
    server.run()


if __name__ == '__main__':
    run_server()
