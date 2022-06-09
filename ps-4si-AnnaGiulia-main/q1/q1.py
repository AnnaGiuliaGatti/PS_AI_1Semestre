import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

frameWeidth = 600
frameHeight = 480

cap = cv2.VideoCapture("q1A.mp4")

cap.set(3, frameWeidth)
cap.set(4, frameHeight)

text = " "

while(1):

    # Pegar cada frame
    _, frame = cap.read()
    frame = cv2.resize(frame, (600, 400))

    # converter BGR para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # definir as ranges de azul e vermelho HSV
    lower_blue = np.array([80, 50, 45])
    upper_blue = np.array([120, 255, 255])
    lower_red = np.array([-20, 100, 100])
    upper_red = np.array([13, 255, 255])


    # --- Cor vermelha sendo detectada ---
    mask_vermelha = cv2.inRange(hsv, lower_red, upper_red)
    res_vermelha = cv2.bitwise_and(frame,frame, mask= mask_vermelha)

    # --- Cor azul sendo detectada ---
    mask_azul = cv2.inRange(hsv, lower_blue, upper_blue)
    res_azul = cv2.bitwise_and(frame,frame, mask= mask_azul)




    #Para o azul
    gray = cv2.cvtColor(res_azul, cv2.COLOR_RGB2GRAY)
    #Achar Contour
    cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    #Countour com area maxima
    c = max(cnts, key=cv2.contourArea)
    bluex, bluey, bluew, blueh = cv2.boundingRect(c)



    #Para o vermelho
    gray = cv2.cvtColor(res_vermelha, cv2.COLOR_RGB2GRAY)
    #Achar Contour
    cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    #Countour com area maxima
    c = max(cnts, key=cv2.contourArea)
    redx, redy, redw, redh = cv2.boundingRect(c)
    cv2.rectangle(frame, (redx, redy), (redx+redw, redy+redh), (0, 255, 0), thickness = 2)


    coordinates = (240,50)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (255,255,0)
    thickness = 2

    if redx == 150 and blueh >= 125:
        print ("Tocou")
        text = "COLISAO DETECTADA"

    if redx == 76 :
        print ("Ultrapassou")
        text = "PASSOU BARREIRA"

    frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)




    cv2.imshow('frame',frame)
    cv2.imshow('res_vermelha',res_vermelha)
    cv2.imshow('res_azul',res_azul)

    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()