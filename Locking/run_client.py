from centeral_locking import LockerClient

"""
    This file is responsible for sending requests to a url and access the resource on it
"""

locker_cli = LockerClient(resource='file1', url="tcp://127.0.0.1:5555")
print locker_cli.send()
locker_cli1 = LockerClient(resource='file1', url="tcp://127.0.0.1:5555")
print locker_cli1.send()
locker_cli4 = LockerClient(resource='file1', url="tcp://127.0.0.1:5555")
print locker_cli4.send()
locker_cli2 = LockerClient(resource='file1', url="tcp://127.0.0.1:5556")
print locker_cli2.send()
locker_cli3 = LockerClient(resource='file1', url="tcp://127.0.0.1:5556")
print locker_cli3.send()
