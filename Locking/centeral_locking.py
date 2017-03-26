import logging
import time
import threading

import zmq

from constants import TIMEOUT_FOR_LOCK_RESOURCE
from utils import get_details_from_message

logging.basicConfig(level=logging.DEBUG)


class CenteralLockerServer():
    """
        Responsible for handlicg sockets for incoming requests.
        Also handling the resource if it is locked or released.
    """
    def __init__(self, urls=["tcp://127.0.0.1:5555"]):
        self._locks = {}
        self._urls = urls
        # self.locker = Locker(max_requests, in_seconds)

    def run(self):
        """
            Server is created with a socket type "zmq.REP" and is bound to known host(s)
            - getting any message that will pass through any socket
            -- message contain the host, port and resource that want to lock it
            - lock the resource on the host
        """
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        for url in self._urls:
            socket.bind(url)
        while True:
            full_message = socket.recv_string()  # any message that will sending from LockerClient
            request_url, resource = get_details_from_message(full_message)
            self._lock(request_url, resource)
            socket.send("Request Executed")  # sending back to LockerClient

    def _lock(self, request_url, resource):
        """
            - create the lock_key that contain url with resource to can handle locking any resource
              on any host. we use url with resource as a key of locking because we have a lot of hosts
              with a lot of resources
            - if this key not in _locks, will lock it for constant time. we execute _unlock on the
              background to can handle any another request and not waiting until unlocking.
            - if the key in _locks, we will try to lock it after constant time (same time of
              executing the first process )
            :param request_url: url that we request on
            :param resource: any resource that we want to lock it on reqest_url
            :return: None
        """
        lock_key = "{0}:{1}".format(request_url, resource)
        if lock_key not in self._locks:
            self._locks[lock_key] = True
            logging.warning("This Resource {0} is locked on {1}".format(resource, request_url))
            t1 = threading.Thread(target=self._unlock, args=(request_url, resource, TIMEOUT_FOR_LOCK_RESOURCE))
            t1.start()
        else:
            logging.error("Can't use this resource now because it's locked, will try after released")
            t2 = threading.Thread(target=self._retrying_lock, args=(request_url, resource, TIMEOUT_FOR_LOCK_RESOURCE))
            t2.start()

    def _unlock(self, request_url, resource, timeout):
        """
            - create lock_key with request_url and resource and unlocking after constant time
            :param request_url: url that we request on
            :param resource: any resource that we want to lock it on reqest_url
            :param timeout: constant time of execution any process
            :return: None
        """
        lock_key = "{0}:{1}".format(request_url, resource)
        time.sleep(timeout)
        del self._locks[lock_key]
        logging.info("Unlock the resource {0} on {1}".format(resource, request_url))

    def _retrying_lock(self, request_url, resource, timeout):
        """
            - Trying to lock resource after constant time
            :param request_url: url that we request on
            :param resource: any resource that we want to lock it on reqest_url
            :param timeout: constant time of execution any process
            :return: None
        """
        time.sleep(TIMEOUT_FOR_LOCK_RESOURCE)
        self._lock(request_url, resource)


class LockerClient():
    """
        Responsible for connecting to sockets and sending message on it.
    """

    def __init__(self, resource, url="tcp://127.0.0.1:5555"):
        self.resource = resource
        self.url = url
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(url)

    def send(self):
        """
            Sending request with message to the connecting url and then wait for reply.
        """
        sneding_string = "url is: {0} and resource is: {1}".format(self.url, self.resource)
        self.socket.send(sneding_string)
        return self.socket.recv_string()
