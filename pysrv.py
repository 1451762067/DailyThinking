import socket
import sqlite3
import _thread
from multiprocessing import Process

ip_port = ('127.0.0.1', 9090)
back_log = 5
buffer_size = 1024*10
time_out = 30

def thread_process(con, address):
    con.settimeout(time_out)
    while 1:
        try:
            msg = con.recv(buffer_size)
            if not msg:
                print("recv fail,con close.");
                con.close()
                return -1
            print('recv message:',msg.decode())

            print('send message:', msg.decode())
            con.send(msg)

        except Exception as e:
            print(e)
            con.close()
            return -1
    return 0

def main_thread():
    srv = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    srv.bind(ip_port)
    srv.listen(back_log) 
    srv.settimeout(time_out)

    while 1:
        try:
            con,address = srv.accept() 
        except Exception as e:
            print(e)
            continue
        try:
            _thread.start_new_thread( thread_process, (con, address) )
        except:
            print("create new thread fail")
            continue

    srv.close()

while 1:
    try:
        p = Process(group=None, target=main_thread)
        p.start()
        p.join()
        print("process end, create new process")
    except Exception as e:
        print(e)
        print("main process end")
