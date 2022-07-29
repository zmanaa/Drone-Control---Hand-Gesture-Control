# first of all import the socket library
import socket
import socket
import cv2
import handTracking as htm

print("Hello")
# next create a socket object
s = socket.socket()
print ("Socket successfully created")

port = 6789

host = socket.gethostname()
s.bind((host, port))
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)
print ("socket is listening")


c, addr = s.accept()
print('Got connection from', addr)

# send a take off message to the client. encoding to send byte type.
c.send("TAKE_OFF_NOW".encode())


cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4,8,12,16,20]
operation = "None"

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    cv2.imshow("Image", img)

    lmList = detector.findPosition(img, draw=False)


    if len(lmList) != 0:
        fingers = []

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]- 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)


        if totalFingers == 0:
            operation = "BACKWARD"
        elif totalFingers == 1:
            operation = "FORWARD"
        elif totalFingers == 2:
            operation = "UP"
        elif totalFingers == 3:
            operation = "DOWN"
        elif totalFingers == 4:
            operation = "YAW"
        elif totalFingers == 5:
            operation = "LAND"

    # send the operation to the client. encoding to send byte type.
    c.send(str(operation).encode())

    # Close the connection with the client
    #if operation == "LAND":
        #break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

c.close()