import socket
import threading
 
from config import CONNECT_TIMEOUT, NODE_ID, TCP_PORT
from logger import RECEIVED, SENT, log_error, log_event, log_msg
from peers import Connection, peer_table
from protocol import PeerDisconnected, recv_msg, send_msg

# don't allow 2 threads writing and changing peer table at the same time
_table_change_lock = threading.Lock()


# send a message to a peer and log it
# Return False if sending failed
def send_to(conn,msg,detail=""):
    if conn.closed:
        return False
    
    try:
        # convert dict -> JSON + add 4 bytes header -> send to socket
        send_msg(conn.sock, conn.send_lock, msg)
    except OSError as e:
        log_error(conn.addr, f"send {msg.get('type')} failed: {e}")
        return False
    log_msg("Sent", conn.addr, msg["type"], detail)
    return True


# server starts tcp server
def start_tcp_server():
    """Open the listening socket and start the welcoming (accept) thread
    Call this before broadcasting PEER_REQUEST
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("", TCP_PORT))
    server_sock.listen()
    threading.Thread(target=_accept_loop, args=(server_sock,), daemon=True).start()
    return server_sock


def _accept_loop(server_sock):
    while True:
        try:
            sock, addr = server_sock.accept()
        except OSError:
            break                                 # server socket closed: shutting down
        # We don't know who this is yet: the peer's first FILE_LIST tells us.
        conn = Connection(sock, addr, outbound=False)
        _start_connection(conn)

# client side

def is_connected(node_id):
    return peer_table.has(node_id)
 
def connect_to_peer(ip,port,node_id):
    """Open a TCP connection to a peer that answered our PEER_REQUEST."""
    
    # no 2 connections
    if node_id == NODE_ID or peer_table.has(node_id):
        return 
    
    try:
        sock = socket.create_connection((ip, port), timeout=CONNECT_TIMEOUT)
    except OSError as e:
        log_error((ip, port), f"connect failed: {e}")
        return
    sock.settimeout(None) 
    conn = Connection(sock, (ip, port), outbound=True, node_id=node_id)
    if not _register(conn):
        conn.close()
        return
    _start_connection(conn)

def _register(conn):
    """ Put a connection with a known node_id to peer table
    """
    with _table_change_lock:
        # replaced: None - no old connection is removed
        #           Connection - one old connection is removed to make room for conn
        
        # accepted: True - keep and use this connection
        #           False - not keep 
        
        # make sure there is no (A->B) and (B->A)
        accepted, replaced = peer_table.register(conn)
        if replaced is not None:
            replaced.close()
            log_event(f"DUPLICATE {conn!r}: keeping this one, closing {replaced.addr[0]}:{replaced.addr[1]}")
        elif accepted:
            log_event(f"PEER ADDED {conn!r}")
        else:
            log_event(f"DUPLICATE {conn!r}: already connected, closing this one")
    return accepted


def _start_connection(conn):
    """Start the receive loop, then send our FILE_LIST right away."""
    import files                                  # see the note at the top of this file
    threading.Thread(target=_receive_loop, args=(conn,), daemon=True).start()
    try:
        files.send_file_list(conn)
    except Exception as e:
        log_error(conn.addr, f"send_file_list: {e}")
 
 
def _receive_loop(conn):
    """One per connection: read messages until the peer disconnects."""
    import files                                  # see the note at the top of this file
    try:
        while True:
            try:
                msg = recv_msg(conn.sock)
            except ValueError as e:
                # Bytes arrived but are not a valid message. The stream can no
                # longer be trusted, so treat it as a disconnection.
                log_error(conn.addr, f"invalid message: {e}")
                break
 
            log_msg(RECEIVED, conn.addr, msg["type"])
 
            # Server side: learn who the peer is from its first message.
            if conn.node_id is None:
                peer_id = msg.get("node_id")
                if isinstance(peer_id, str) and peer_id != NODE_ID:
                    conn.node_id = peer_id
                    if not _register(conn):
                        break                     # duplicate: close this one
 
            # Call the right function for this message type.
            try:
                if msg["type"] == "FILE_LIST":
                    files.handle_file_list(conn, msg)
                elif msg["type"] == "DATA_REQUEST":
                    files.handle_data_request(conn, msg)
                elif msg["type"] == "FILE_DATA":
                    files.handle_file_data(conn, msg)
                else:
                    log_error(conn.addr, f"unknown message type {msg['type']}")
            except Exception as e:                # one bad message must not kill the loop
                log_error(conn.addr, f"{msg['type']} handler: {e}")
    except PeerDisconnected:
        pass                                      # recv returned b"" or connection reset
    finally:
        _cleanup(conn)
 
 
def _cleanup(conn):
    """Remove the peer, drop its file list, close the socket, log it."""
    import files                                  # see the note at the top of this file
    with _table_change_lock:
        removed = peer_table.remove(conn)         # its files go with it
        conn.close()
        if removed:
            log_event(f"PEER REMOVED {conn!r} (connection closed)")
    if removed:
        try:
            files.on_peer_disconnected(conn)
        except Exception as e:
            log_error(conn.addr, f"on_peer_disconnected: {e}")
 
        

        