# CLS (Centralized locking system)
----------------------------------

This Python script for locking the access on the resource for all servers and instances that are running.
Most basic pattern is client/server model, while client sends a request and server replies to the request.

we will serve these requests using zmq with REQ/REP
we consuming servers could be spread across more computers. To provide access to LockerServer, we will use zmq.

* socket zmq.REQ will block on send unless it has successfully received a reply back.
* socket zmq.REP will block on recv unless it has received a request.

Each Request/Reply is paired and has to be successful.
![alt tag](http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/_images/reqrep.png)

# Install Requirements
----------------------
    pip install -r requirements.txt

# Run
-----
our senario that implemented:
-----------------------------
We assume that we have two urls that will open socket with it: "tcp://127.0.0.1:5555", "tcp://127.0.0.1:5556",
we can increase it by any number of urls
* run server that will open sockets with all urls in file

    pyhton Locking/run_server.py

we are sending 5 requests, first one to use 'file1' resource on "tcp://127.0.0.1:5555", this is the first request then
it can use this resource and this resource will lock for constant time.
second request to use 'file1' resource on "tcp://127.0.0.1:5555", will found this resource is locked on this url then
it will be retry locking after constant time, if the resource is released then it will locked again to this process and so on...
* run client that will send requests to any url to access any resource on it

    pythin Locking/run_client.py

