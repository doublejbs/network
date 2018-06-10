import socket, threading
import time
import datetime
from queue import Queue

#bottlenec rate와 queue size를 입력받습니다.
botRate = int(input("bottle neck link rate: "))
qSize = int(input("queue size: "))

#socket을 생성합니다.
receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind((socket.gethostbyname(socket.gethostname()), 10080))


occList = {}
inPck = 0 #incoming packet을 count합니다.
forPck = 0 #forwarding packet을 count합니다.


def wait():
    t = threading.Thread(target=wait)
    t.start()

#network emulator모듈에서 bottleneck실행 후 Ack generator 모듈로 forwarding하는 함수 입니다.
def ne2ag(sock, addr, botRate):
    global run, forPck, go
    #sender에 해당하는 queue를 받아옵니다.
    neQueue = qList.get(addr[1])
    _go = go.get(addr[1])
    #forwarding 후 sender에게 ack을 보냅니다.
    if _go:
        neQueue.get()
        forPck += 1
        sock.sendto('ack'.encode('utf-8'), addr)

    timer = threading.Timer(1/botRate, ne2ag, args=[sock, addr, botRate])
    if run.get(addr[1]):
        timer.start()

#network emulator에서 packet을 queue에 추가하는 함수입니다.
def ntwrkEmul(qSize, data, addr):

    neQueue = qList.get(addr[1])
    #queue가 다 찼으면 drop 시킵니다.
    if neQueue.qsize() < qSize:
        neQueue.put(data.decode())
    else:
        pass


#2초마다 출력하는 메시지 함수입니다.
def twoSecMsg():
    global run, qSize
    global inPck, forPck, occList

    try:
        print("incoming rate: ", inPck/2, "/2sec")
        print("forwarding rate: ", forPck/2, "/2sec")
        print("avg queue occupancy: ", (getAvgOcc()/len(addrList)/20)/qSize)
        inPck = 0
        forPck = 0
    except Exception as e:
        print(e)

    timer = threading.Timer(2.1, twoSecMsg)
    if 1:
        timer.start()


qList = {}
go = {}

run = {}
addrList = []

#각 sender마다 queue에서의 occupancy의 값을 0.1초마다 추가합니다.
def avgOccupancy(addr):
    global occList, qList, run
    occ = qList.get(addr[1]).qsize()
    occList[addr[1]] = occList.get(addr[1]) + occ
    t = threading.Timer(0.1, avgOccupancy, args=[addr])
    if run.get(addr[1]):
        t.start()

#queue의 평균 occupancy값을 구하는 함수입니다.
def getAvgOcc():
    global occList, addrList
    i = 0
    sum = 0
    try:
        while addrList[i]:
            temp = occList.get(addrList[i])
            sum = sum + temp
            occList[addrList[i]] = 0
            i += 1

    except Exception as e:
        pass
    return sum


#packet을 받을 때의 함수입니다.
def rcvMsg(sock):
    global inPck, qSize, index, qList, go, run, addrList
    while True:
        try:
            data, addr = sock.recvfrom(1024)

            #sender가 처음 접속시 enter 메시지를 받고, sender를 리스트에 추가합니다.
            #sender마다 queue를 생성합니다.
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

            #처음 접속이후 packet을 받을 때마다 incoming pakcet을 증가시키고 ntwrkEmul함수를 실행합니다.
            elif data:
                inPck += 1
                ntwrkEmul(qSize, data, addr)
        except:
            continue


addr = []

wait()
twoSecMsg()
t = threading.Thread(target=rcvMsg, args=(receiver,))
t.daemon = True
t.start()


