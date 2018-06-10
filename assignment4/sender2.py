import socket, threading
import time

#receiver의 ip와 init send rate를 입력받습니다.
ip = input("enter receiver ip: ")
initSendRate = int(input("enter initial sending rate: "))

#socket을 생성합니다.
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.bind((socket.gethostbyname(socket.gethostname()), 0))
ackCount = 0
once = 1

j=0

#1000byte 짜리 text를 생성합니다.
text = '11111'
while j<199:
    text = '11111' + text
    j += 1

#receiver로 부터 ack을 받을 때마다 ackCount를 증가시킵니다.
def rcvMsg(sock):
    global ackCount
    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            ackCount += 1

#2초마다 출력되는 메시지 함수입니다.
def twoSecMsg():
    global once
    if once:
        time.sleep(2)
        once = 0
    global pckCount, ackCount

    print("sending rate: ", pckCount/2, "/2sec")
    print("goodput: ", ackCount/2, "/2sec")
    print("goodput ratio: ", ackCount/pckCount)
    pckCount = 0
    ackCount = 0
    timer = threading.Timer(2.1, twoSecMsg)
    if 1:
        timer.start()


#receiver에게 packet을 전송하는 함수입니다.
def sendMsg(sock):
    global allPck, pckCount, text
    sender.sendto(text.encode('utf-8'), (ip, 10080))
    #packet을 전송할 때마다 pckCount를 증가시킵니다.
    pckCount += 1
    timer = threading.Timer(1/initSendRate, sendMsg, args=[sock])
    if 1:
        timer.start()






pckCount = 0

t = threading.Thread(target=rcvMsg, args=(sender,))
t.daemon = True
t.start()

#처음 접속시 enter 메시지를 보냅니다.
sender.sendto('enter'.encode('utf-8'), (ip, 10080))

sendMsg(sender)
twoSecMsg()










