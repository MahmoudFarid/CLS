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
First run server that will open sockets with all urls in file

    pyhton Locking/run_server.py
    
Second run client that will send requests to any url to access any resource on it

    pythin Locking/run_client.py

