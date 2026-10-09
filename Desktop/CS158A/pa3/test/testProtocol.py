"""
test_protocol.py - tests for the TCP framing in protocol.py.

Run:  python test_protocol.py
(put this file in the same folder as protocol.py)

socket.socketpair() creates two sockets already connected to each other,
like a TCP connection between two peers but inside one program. No network,
no ports, no second machine needed. Whatever is sent on `a` arrives on `b`.
"""

import base64
import json
import os
import socket
import struct
import threading
import time

from protocol import PeerDisconnected, recv_msg, send_msg


def make_pair():
    a, b = socket.socketpair()
    b.settimeout(5)          # a buggy test fails after 5 s instead of hanging forever
    return a, b


def frame(msg):
    """Build a frame by hand, so tests can split or glue frames."""
    data = json.dumps(msg, ensure_ascii=False).encode("utf-8")
    return struct.pack("!I", len(data)) + data


# ---------------------------------------------------------------- tests

def test_single_message():
    """One message sent, the same dict comes back."""
    a, b = make_pair()
    msg = {"type": "DATA_REQUEST", "filename": "notes.pdf"}
    send_msg(a, threading.Lock(), msg)
    assert recv_msg(b) == msg
    a.close(); b.close()


def test_two_messages_stuck_together():
    """Two frames arrive in one chunk; recv_msg must split them."""
    a, b = make_pair()
    m1 = {"type": "FILE_LIST", "node_id": "A", "files": ["a.txt"]}
    m2 = {"type": "DATA_REQUEST", "filename": "a.txt"}
    a.sendall(frame(m1) + frame(m2))         # one send, two messages
    assert recv_msg(b) == m1
    assert recv_msg(b) == m2
    a.close(); b.close()


def test_message_arrives_in_pieces():
    """Header and body arrive separately with delays; recv_exact must wait."""
    a, b = make_pair()
    msg = {"type": "FILE_LIST", "node_id": "A", "files": ["x.png", "y.pdf"]}
    data = frame(msg)

    def slow_sender():
        a.sendall(data[:2]); time.sleep(0.1)     # half of the length header
        a.sendall(data[2:10]); time.sleep(0.1)   # rest of header + some body
        a.sendall(data[10:])                     # the rest

    threading.Thread(target=slow_sender).start()
    assert recv_msg(b) == msg
    a.close(); b.close()



# ---------------------------------------------------------------- runner

if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_") and callable(obj)]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"PASS  {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"FAIL  {test.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")