import cv2
import numpy as np
cap = cv2.VideoCapture('http://192.168.1.1:4747/video')

azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

while True:
  ret,frame = cap.read()

  if ret==True:
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(frameHSV,azulBajo,azulAlto)

    contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contornos, -1, (255,0,0), 3)
    for c in contornos:
      vertices = cv2.approxPolyDP(c, 0.05 * cv2.arcLength(c, True), True)

      if (len(vertices) == 4):
        #imgClient = vertices
        mensaje = "ROI detectado"
        cv2.putText(frame, mensaje, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.drawContours(frame, [c], 0, (0, 0, 255), 2)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      break
cap.release()
cv2.destroyAllWindows()