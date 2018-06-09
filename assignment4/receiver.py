import socket, threading
import time
import datetime
from queue import Queue

botRate = int(input("bottle neck link rate: "))
qSize = int(input("queue size: "))

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind((socket.gethostbyname(socket.gethostname()), 10080))

agQueue = []

once = 1
neOnce = 1
occList = {}

def wait():
    t = threading.Thread(target=wait)
    t.start()

def ne2ag(sock, addr, botRate):
    global run, forPck, neOnce, go
    neQueue = qList.get(addr[1])
    _go = go.get(addr[1])
    if _go:
        neQueue.get()
        forPck[addr[1]] += 1
        sock.sendto('ack'.encode('utf-8'), addr)

    timer = threading.Timer(1/botRate, ne2ag, args=[sock, addr, botRate])
    if run.get(addr[1]):
        timer.start()

def ntwrkEmul(qSize, data, addr):
    global runOnce
    neQueue = qList.get(addr[1])
    if neQueue.qsize() < qSize:
        neQueue.put(data.decode())
    else:
        pass
    #bottleneck link rate동안 ne에서 ag로!

def twoSecMsg(addr):
    global once, run, qSize
    global inPck, forPck, occList
    neQueue = qList[addr[1]]

    try:
        print(addr[1], "incoming rate: ", inPck.get(addr[1]), "/2sec")
        print("forwarding rate: ", forPck.get(addr[1]), "/2sec")
        print("avg queue occupancy: ", (occList.get(addr[1])/20)/qSize)
        inPck[addr[1]] = 0
        forPck[addr[1]] = 0
        occList[addr[1]] = 0
    except Exception as e:
        print(e)
    timer = threading.Timer(2.1, twoSecMsg, args=[addr])
    if run.get(addr[1]):
        timer.start()
    else:
        print(addr[1], ': end')

qList = {}
go = {}
inPck = {}
forPck = {}
run = {}

def avgOccupancy(addr):
    global occList, qList, run


    occ = qList.get(addr[1]).qsize()
    occList[addr[1]] = occList.get(addr[1]) + occ
    t = threading.Timer(0.1, avgOccupancy, args=[addr])
    if run.get(addr[1]):
        t.start()



def rcvMsg(sock):
    global inPck, qSize, index, qList, go, run
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            #print(addr[1])
            if data.decode() == 'enter':
                run[addr[1]] = 1
                occList[addr[1]] = 0
                inPck[addr[1]] = 0
                forPck[addr[1]] = 0
                go[addr[1]] = 0
                neQueue = Queue()
                qList[addr[1]] = neQueue
                twoSecMsg(addr)
                ne2ag(sock, addr, botRate)
                avgOccupancy(addr)
                go[addr[1]] = 1
            elif data.decode() == 'exit':
                run[addr[1]] = 0

            elif data:
                inPck[addr[1]] += 1
                ntwrkEmul(qSize, data, addr)

        except:
            continue


addr = []
runOnce = 1
wait()
t = threading.Thread(target=rcvMsg, args=(receiver,))
t.daemon = True
t.start()


