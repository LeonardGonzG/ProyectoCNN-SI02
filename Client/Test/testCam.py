import numpy as np
import cv2
import base64

pathImg= './ImgROI/'
"""
#go to the setting find ip cam username and password if it is not empty use
#first one
#cap = cv2.VideoCapture('http://username:password@ip:port/video')
cap = cv2.VideoCapture('http://192.168.1.3:4747/video')


while(cap.isOpened()):
    ret, frame = cap.read()

    #do some stuff
    #gray  = cv2.cvtColor(frame, cv2.COLOR)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

"""
"""
cam = cv2.VideoCapture('http://192.168.1.3:4747/video')

cv2.namedWindow("test")

img_counter = 0
c_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC Key pressed
        print('Se ha oprimido la tecla escape...')
        break
    if k%256 == 99:
        # C Key pressed
        print("Se ha oprimido la tecla c",  c_counter, " veces")
        c_counter += 1
    elif k%256 == 101:
        # E Key pressed
        img_name = "id_{}.tiff".format(img_counter)
        cv2.imwrite(str(pathImg)+img_name, frame)

        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
"""
"""#Codificar imagen en base64
image = open('./ImgROI/id_0.tiff', 'rb')
image_read = image.read()
image_64_encode = base64.encodestring(image_read)

print(image_64_encode)
#instalar simpljson
image_64_decode = base64.decodestring(image_64_encode)
image_result = open('./ImgROI/id_0_decode.tiff', 'wb')
image_result.write(image_64_decode)"""

nameWindow="Calculadora"
showROI = 1


def nothing(x):
    pass
def constructorVentana():
    cv2.namedWindow(nameWindow)
    cv2.createTrackbar("min",nameWindow,0,500,nothing)
    cv2.createTrackbar("max", nameWindow, 100, 500, nothing)
    cv2.createTrackbar("kernel", nameWindow, 1, 100, nothing)
    cv2.createTrackbar("areaMin", nameWindow, 32000, 40000, nothing)
    cv2.createTrackbar("areaMax", nameWindow, 32000, 40000, nothing)

def calcularAreas(figuras):
    areas=[]
    for figuraActual in figuras:
        areas.append(cv2.contourArea(figuraActual))
    return areas


def detectarForma(imagen, imgClient):
    #Reducir dimensiones de la imagen de 3D a 2D
    #Conversión a escala de grises
    imagenGris=cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Imagen Gris", imagenGris)
    # Hallar los bordes
    #Utilizando la derivada (Canny)
    min=cv2.getTrackbarPos("min",nameWindow)
    max=cv2.getTrackbarPos("max",nameWindow)
    bordes=cv2.Canny(imagenGris,min,max)
    cv2.imshow("Bordes",bordes)

    #Operaciones morfológicas
    tamañoKernel=cv2.getTrackbarPos("kernel",nameWindow)

    kernel=np.ones((tamañoKernel,tamañoKernel),np.uint8)
    bordes=cv2.dilate(bordes,kernel)
    cv2.imshow("Bordes reforzados ",bordes)

   # figuras, jerarquia=cv2.findContours(bordes,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    figuras, jerarquia = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas=calcularAreas(figuras)

    areaMinima=cv2.getTrackbarPos("areaMin",nameWindow)
    areaMax = cv2.getTrackbarPos("areaMax",nameWindow)
    i=0
    for figuraActual in figuras:
        vertices = cv2.approxPolyDP(figuraActual, 0.05 * cv2.arcLength(figuraActual, True), True)
        # print(vertices[0][0])
        # print(areas[i])
        if(len(vertices)==4):
            if(areas[i]>=areaMinima and areas[i]<=areaMax):
                imgClient = vertices
                mensaje = "ROI detectado"
                cv2.putText(imagen, mensaje, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.drawContours(imagen, [figuraActual], 0, (0, 0, 255), 2)
    return (imagen, imgClient)

camara=cv2.VideoCapture('http://192.168.1.5:4747/video')
#camara=cv2.VideoCapture(0)
constructorVentana()

img_counter = 0
c_counter = 0

while True:
    _,imagen=camara.read()

    k = cv2.waitKey(1)
    imgClient = []
    imageP =[]
    imageOut = imagen[20:,]

    if k % 256 == 101:
        showROI+=1

    if showROI %2 ==0:
        imagen = detectarForma(imageOut, imgClient)
        imageP= imagen[0]
        cv2.imshow("Imagen Camara", imageP)
        imgClient = imagen[1]
    else:
        cv2.imshow("Imagen Camara", imageOut)

    # c Key pressed
    if k % 256 == 99:
        try:
          x, y, w, h = cv2.boundingRect(imgClient)
          cutImg= imageP[y:y + h, x:x + w]
          cv2.imshow("Imagen Cortada", cutImg)
        except:
            print("Falla al capturar imagen")

    # Para el programa
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

camara.release()
cv2.destroyAllWindows()
