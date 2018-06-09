import socket, threading
import time
import datetime
from queue import Queue

botRate = 50#int(input("bottle neck link rate: "))
qSize = 10#int(input("queue size: "))

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind((socket.gethostbyname(socket.gethostname()), 10080))

agQueue = []
run = 1
once = 1
neOnce = 1
go = 0

def wait():
    t = threading.Thread(target=wait)
    t.start()


def ne2ag(sock, addr, botRate):
    global run, forPck, neOnce, go
    print('pp')
    neQueue = qList.get(addr[1])
    print('ppp')
    if go:
        neQueue.get()
        forPck += 1
        sock.sendto('ack'.encode('utf-8'), addr)
        print('sent')
    timer = threading.Timer(0.1, ne2ag, args=[sock, addr, botRate])
    if run:
        timer.start()

def ntwrkEmul(sock, botRate, qSize, data, addr):
    global runOnce
    neQueue = qList.get(addr[1])
    if neQueue.qsize() < qSize:
        neQueue.put(data.decode())
    else:
        pass
    #bottleneck link rate동안 ne에서 ag로!

def twoSecMsg(addr):
    global once, run, qSize
    global inPck, forPck
    try:
        neQueue = qList.get(addr[1])
    except Exception as e:
        print(e)

    try:
        print(addr[1], "incoming rate: ", inPck, "/2sec")
        print("forwarding rate: ", forPck, "/2sec")
        print("avg queue occupancy: ", neQueue.qsize()/qSize)
        inPck = 0
        forPck = 0
    except:
        pass
    timer = threading.Timer(2.1, twoSecMsg, args=[addr])
    if run:
        timer.start()

index = -1
qList = {}

def rcvMsg(sock):
    global inPck, qSize, go, index, qList
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            #print(addr[1])

            if data.decode() == 'enter':
                neQueue = Queue()
                print('ok')
                qList[addr[1]] = neQueue
                print('ok2')
                twoSecMsg(addr)
                ne2ag(sock, addr, botRate)
                print('ok3')
                go = 1
                print('nequeue: ', addr[1])
            elif data:
                print(addr[1], ': ', data)
                inPck += 1
                ntwrkEmul(sock, botRate, qSize, data, addr)

        except:
            continue

inPck = 0
forPck = 0
addr = []
runOnce = 1


wait()
t = threading.Thread(target=rcvMsg, args=(receiver,))
t.daemon = True
t.start()


