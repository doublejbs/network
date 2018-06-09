import socket, threading
import time
import datetime

ip = socket.gethostbyname(socket.gethostname()) #input("enter receiver ip: ")
initSendRate = 10 #int(input("enter initial sending rate: "))

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.bind((socket.gethostbyname(socket.gethostname()), 0))
ackCount = 0
once = 1

def rcvMsg(sock):
    global ackCount
    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            ackCount += 1

def twoSecMsg():
    global once
    if once:
        time.sleep(2)
        once = 0
    global pckCount, ackCount
    #print('temp: ', datetime.datetime.now())
    print("sending rate: ", pckCount, "/2sec")
    print("goodput: ", ackCount, "/2sec")
    print("goodput ratio: ", ackCount/pckCount)
    pckCount = 0
    ackCount = 0
    timer = threading.Timer(2.1, twoSecMsg)
    if allPck < 100:
        timer.start()

def sendMsg(sock):
    global allPck, pckCount
    sender.sendto('ok'.encode('utf-8'), (ip, 10080))
    #print('pkt', pckCount, datetime.datetime.now())
    allPck += 1
    pckCount += 1
    timer = threading.Timer(1/initSendRate, sendMsg, args=[sock])
    if allPck < 100:
        timer.start()

run = 0
allPck = 0
initTime = time.time()

pckCount = 0

t = threading.Thread(target=rcvMsg, args=(sender,))
t.daemon = True
t.start()

sender.sendto('enter'.encode('utf-8'), (ip, 10080))

sendMsg(sender)
twoSecMsg()










