import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

frameWeidth = 600
frameHeight = 480

cap = cv2.VideoCapture(r"C:\Users\Anna Giulia Baani\Documents\PS-AI-Final\ps-4si-AnnaGiulia-main\q2\q2.mp4")

cap.set(3, frameWeidth)
cap.set(4, frameHeight)

text = " "

while(1):

    # Pegar cada frame
    _, img = cap.read()
    img = cv2.resize(img, (800, 600))


    # ---- Converter para cinza ----
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.

    th, im_th = cv2.threshold(blur, 220, 255, cv2.THRESH_BINARY_INV)

    # Copy the thresholded image.
    im_floodfill = im_th.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv



    # ---- threshold ( Entre 180 e 255 fica todos os contornos)  ----
    #thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]

    # apply close morphology
    #kernel = np.ones((20,30), np.uint8)
    #morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # invert so rectangle is white
    #morph = 255 - morph

    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,20))
    #dilate = cv2.dilate(morph, kernel, iterations=1)








    # get largest contour and draw on copy of input
    result = img.copy()

    contours, hierarchy = cv2.findContours(im_out, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(result, contours, contourIdx=-1, color=(0,0,255))

    #contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #contours = contours[0] if len(contours) == 2 else contours[1]
    #big_contour = max(contours, key=cv2.contourArea)
    #cv2.drawContours(result, [big_contour], 0, (0,255,255), 1)


    #                                                                                           ------------CAMADA VERMELHA------------
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    blur = cv2.GaussianBlur(hsv,(5,5),3)
    blur2 = cv2.GaussianBlur(blur,(3,3),3)

    lower_red = np.array([0, 50, 20])
    upper_red = np.array([5, 255, 255])

    lower_red2 = np.array([175, 70, 20])
    upper_red2 = np.array([180, 255, 255])

    # --- Cor vermelha sendo detectada ---
    mask_vermelha = cv2.inRange(blur2, lower_red, upper_red)
    mask_vermelha2 = cv2.inRange(blur2, lower_red2, upper_red2)

    #Criando bolas para saber oque é cada vermelho----------

    #vermelho longe--
    cnts = cv2.findContours(mask_vermelha2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        cv2.drawContours(mask_vermelha2, [c], -1, (255,255,255), thickness=80)


    #vermelho perto--
    cnts = cv2.findContours(mask_vermelha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        cv2.drawContours(mask_vermelha, [c], -1, (255,255,255), thickness=75)


    # ANTES DE SOMAR DEVO CRIAR AS BOLAS--------------
    blended = cv2.addWeighted(mask_vermelha, 0.5, mask_vermelha2, 0.5, 0)
    #Depois de somar as bolhas tenho que deixalas brancas



    #Desenhar e encontrar contorno só das vermelhas
    contours2, hierarchy = cv2.findContours(blended, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(blended, contours2, contourIdx=-1, color=(0,255,255))


    #                                                                               -------------------- Fim da camada vermelha -------------
    
    
    
    threshold_area = 10000     #threshold area 
    for cnt in contours:        
        area = cv2.contourArea(cnt)         
        if area > threshold_area:
            print(len(contours2))                   



    coordinates = (650,20)
    coordinates2 = (650,40)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (0,0,0)
    thickness = 2

    text = ("Preto = " + str(len(contours)-len(contours2)))
    text2 = ("Vermelho = " + str(len(contours2)))

    result = cv2.putText(result, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
    result = cv2.putText(result, text2, coordinates2, font, fontScale, color, thickness, cv2.LINE_AA)


    # display results
    cv2.imshow("RESULT", result)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()