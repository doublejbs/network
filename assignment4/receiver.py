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
inPck = 0
forPck = 0

def wait():
    t = threading.Thread(target=wait)
    t.start()

def ne2ag(sock, addr, botRate):
    global run, forPck, neOnce, go
    neQueue = qList.get(addr[1])
    _go = go.get(addr[1])
    if _go:
        neQueue.get()
        forPck += 1
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

def twoSecMsg():
    global once, run, qSize
    global inPck, forPck, occList

    try:
        print("incoming rate: ", inPck/20, "/2sec")
        print("forwarding rate: ", forPck/20, "/2sec")
        print("avg queue occupancy: ", (getAvgOcc()/20)/qSize)
        inPck = 0
        forPck = 0
    except Exception as e:
        print('1', e)

    timer = threading.Timer(2.1, twoSecMsg)
    if 1:
        timer.start()


qList = {}
go = {}

run = {}
addrList = []

def avgOccupancy(addr):
    global occList, qList, run
    occ = qList.get(addr[1]).qsize()
    occList[addr[1]] = occList.get(addr[1]) + occ
    t = threading.Timer(0.1, avgOccupancy, args=[addr])
    if run.get(addr[1]):
        t.start()

def getAvgOcc():
    global occList, addrList
    i = 0
    sum = 0
    try:
        while addrList[i]:
            temp = occList.get(addrList[i])
            sum = sum + temp
            i += 1
    except Exception as e:
        pass
    return sum



def rcvMsg(sock):
    global inPck, qSize, index, qList, go, run, addrList
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            #print(addr[1])
            if data.decode() == 'enter':
                addrList.append(addr[1])
                run[addr[1]] = 1
                occList[addr[1]] = 0
                go[addr[1]] = 0
                neQueue = Queue()
                qList[addr[1]] = neQueue
                ne2ag(sock, addr, botRate)
                avgOccupancy(addr)
                go[addr[1]] = 1
            elif data.decode() == 'exit':
                run[addr[1]] = 0

            elif data:
                inPck += 1
                ntwrkEmul(qSize, data, addr)

        except:
            continue


addr = []
runOnce = 1
wait()
twoSecMsg()
t = threading.Thread(target=rcvMsg, args=(receiver,))
t.daemon = True
t.start()


